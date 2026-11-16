"""Reading a contributed document's bytes: a URL (a browser when a portal
wants one) or a file, and the identity derived from them."""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
from uuid import UUID

from nomotheca_ingest.core import extract
from nomotheca_ingest.core.browser import with_browser
from nomotheca_ingest.core.errors import RefusalError
from nomotheca_ingest.core.snapshots import USER_AGENT
from nomotheca_ingest.core.text import sha256_hex


@dataclass(frozen=True, slots=True)
class SourceDocument:
    """One contributed document's bytes, and where they came from.

    The other half of the pair: what was read, as against what the reviewer
    said about it. Identity is derived from the bytes and the origin, so it is
    settled before anything is archived and cannot drift from the content it
    names.
    """

    raw: bytes
    content_type: str
    #: The URL fetched, or a file:// URI for an upload.
    origin: str
    #: Canonical URL, or file:<sha256> — see `national_id_for`.
    national_id: str
    #: fetch_snapshots.id, once the bytes have been archived. None until then,
    #: because archive-first means nothing is parsed before this is known.
    snapshot_id: UUID | None = None

    @property
    def content_hash(self) -> str:
        """The sha256 that decides "already present" and keys the version."""
        return content_hash(self.raw)

    def archived_as(self, snapshot_id: UUID) -> "SourceDocument":
        """The same document, now with the snapshot that proves it was archived."""
        return replace(self, snapshot_id=snapshot_id)


def canonical_url(url: str) -> str:
    """One URL per document: lowercased scheme and host, no fragment.

    BOFiP links the same page with different anchors and Legifrance with a
    trailing slash; without this they would become several instruments of the
    same text, each with its own chunks competing in retrieval.
    """
    parts = urlsplit(url.strip())
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, parts.query, ""))


def content_hash(raw: bytes) -> str:
    """The sha256 that decides "already present" and keys the version."""
    return sha256_hex(raw)


def national_id_for(raw: bytes, url: str | None = None) -> str:
    """Stable identity of a contributed document.

    A URL identifies the document wherever it was fetched from; an upload has
    only its bytes, so it is keyed by them.
    """
    return canonical_url(url) if url else f"file:{content_hash(raw)}"


#: The browser fetch_in_browser presents itself as.
BROWSER_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"


def _expects_pdf(url: str) -> bool:
    return urlsplit(url).path.lower().endswith(".pdf")


def fetch_in_browser(url: str, timeout_ms: int = 60000) -> bytes | None:
    """A PDF that answers a plain HTTP client with an HTML page, opened in Firefox.

    sante.gouv.fr serves its Bulletin officiel PDFs (instructions DSS/2B/…,
    the BMAF and the family-benefit ceilings) to a browser and a
    «Vérification de sécurité» page to httpx; opened in Firefox the same URL
    starts the download with no interaction. Optional (the ``browser``
    extra: Playwright + ``playwright install firefox``, see `core.browser`); None when it is
    absent, when no download starts, or when what arrives is not a PDF —
    a page that wants a human is left to the human.
    """

    def download(browser) -> bytes:
        context = browser.new_context(user_agent=BROWSER_USER_AGENT, accept_downloads=True)
        page = context.new_page()
        with page.expect_download(timeout=timeout_ms) as started:
            try:
                page.goto(url, timeout=timeout_ms)
            except Exception:
                pass  # Firefox aborts the navigation when the download starts
        path = started.value.path()
        return Path(path).read_bytes() if path else b""

    raw = with_browser("firefox", download)
    return raw if raw and raw.startswith(b"%PDF") else None


def read_input(url: str | None, file_path: str | None) -> SourceDocument:
    """Read a contributed document's bytes, however the reviewer named it.

    Fetching happens here, in Python — never in the UI, which passes a URL or
    a path and nothing else. The returned document is not yet archived; its
    `snapshot_id` is filled in by `archived_as` once it is.
    """
    if bool(url) == bool(file_path):
        msg = "Contribute exactly one of a URL or a file path"
        raise RefusalError(msg)
    if url:
        import httpx

        with httpx.Client(
            timeout=60.0,
            follow_redirects=True,
            headers={"User-Agent": USER_AGENT},
        ) as client:
            response = client.get(url)
        response.raise_for_status()
        raw = response.content
        content_type = response.headers.get("content-type")
        origin = str(response.url)
        if _expects_pdf(url) and not raw.startswith(b"%PDF"):
            fetched = fetch_in_browser(url)
            if fetched is None:
                # Never the page in its place: the AGS 2025 rate PDF answered
                # with the press-release listing, ingested as the release.
                msg = f"{url} answers with an HTML page, not the PDF; download it and contribute the file"
                raise RefusalError(msg)
            raw, content_type = fetched, "application/pdf"
        return SourceDocument(
            raw=raw,
            content_type=extract.content_type_for(url, content_type, raw),
            origin=origin,
            national_id=national_id_for(raw, url),
        )
    path = Path(file_path)
    raw = path.read_bytes()
    return SourceDocument(
        raw=raw,
        content_type=extract.content_type_for(path.name, None, raw),
        origin=path.resolve().as_uri(),
        national_id=national_id_for(raw, None),
    )


def suggest(url: str | None = None, file_path: str | None = None) -> dict[str, str | None]:
    """Title and validity-date suggestions for an input, loading nothing.

    Cheap enough for the UI to call while the reviewer is still typing: it
    reads the document, never the database.
    """
    document = read_input(url, file_path)
    extracted = extract.extract(document.raw, document.content_type)
    fallback = Path(urlsplit(document.origin).path).name or None
    title = extracted.suggested_title or fallback
    valid_from = extract.suggested_valid_from(title, url or document.origin)
    return {
        "title": title,
        "valid_from": valid_from.isoformat() if valid_from else None,
        "content_type": document.content_type,
    }
