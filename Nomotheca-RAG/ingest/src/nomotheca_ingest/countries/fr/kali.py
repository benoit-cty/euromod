"""KALI — the DILA base of collective agreements — as a fetchable FR source.

Collective agreements are evidence like a law where they set a rate (ADR 0006):
the AGIRC-ARRCO contributions (ANI du 17 novembre 2017, art. 37: CEG 2,15 % /
2,70 %, CET 0,35 %), APEC, the cadres' prévoyance are stated nowhere else. The
Tricoteuses mirror the rest of the FR adapter reads carries JORF and LEGI only,
and DILA publishes KALI solely as dumps — one global tarball plus a daily
increment — so a document is read from a local copy kept in step with them.

The copy holds the dump tree as published (`article/KALI/ARTI/…/KALIARTI….xml`,
`texte/{version,struct}/…`, `section_ta/…`); `sync` downloads the latest global
dump once, then applies every increment newer than the last one applied. It
lives under ``NOMOTHECA_KALI_DIR`` (the worker mounts a volume there), about
1.8 GB extracted. The conteneur tree (a whole convention, hundreds of texts) is
deliberately left out: ingesting one is not a gap-fill.

What is archived per document is the XML converted to the same dict shape the
Tricoteuses JSON has for LEGI/JORF — `@attr`, `#text`, repeated children as a
list, CONTENU/NOTA kept as their inner HTML — so `parse_dila_json` reads KALI
unchanged and `reparse` replays it like any other snapshot.
"""

from __future__ import annotations

import contextlib
import fcntl
import json
import os
import re
import shutil
import tarfile
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

import httpx

if TYPE_CHECKING:
    from nomotheca_ingest.core.ir import Snapshot, SourceRef
    from nomotheca_ingest.core.snapshots import SnapshotClient

KALI_DUMP_BASE = "https://echanges.dila.gouv.fr/OPENDATA/KALI/"

#: The ids a KALI document is fetched by. KALICONT (a whole convention) is not one.
KALI_ID = re.compile(r"\bKALI(?:TEXT|ARTI|SCTA)\d{12}\b")

#: Dump subtrees kept locally; the conteneur tree is never ingested.
KEPT_TREES = ("article/", "texte/", "section_ta/")

#: Elements whose content is HTML, kept as an inner-markup string like Tricoteuses.
HTML_ELEMENTS = frozenset({"CONTENU"})

GLOBAL_DUMP = re.compile(r"Freemium_kali_global_(\d{8}-\d{6})\.tar\.gz")
INCREMENT_DUMP = re.compile(r"KALI_(\d{8}-\d{6})\.tar\.gz")

#: A gap-fill checks for new increments at most this often.
SYNC_INTERVAL = timedelta(hours=12)


def default_root() -> Path:
    """Where the local KALI copy lives: NOMOTHECA_KALI_DIR, else the user cache."""
    configured = os.environ.get("NOMOTHECA_KALI_DIR")
    if configured:
        return Path(configured)
    return Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "nomotheca" / "kali"


def tree_paths(source_id: str) -> list[str]:
    """The dump-relative XML paths one KALI id is stored under (a text has two)."""
    match = KALI_ID.fullmatch(source_id)
    if not match:
        msg = f"not a KALI document id: {source_id!r}"
        raise ValueError(msg)
    kind = source_id[4:8]
    pairs = "/".join(source_id[8 + index : 10 + index] for index in range(0, 10, 2))
    leaf = f"KALI/{kind}/{pairs}/{source_id}.xml"
    if kind == "TEXT":
        return [f"texte/version/{leaf}", f"texte/struct/{leaf}"]
    if kind == "SCTA":
        return [f"section_ta/{leaf}"]
    return [f"article/{leaf}"]


def element_to_dict(element: ET.Element) -> Any:
    """Convert one DILA XML element to the Tricoteuses JSON shape."""
    if element.tag in HTML_ELEMENTS:
        inner = (element.text or "") + "".join(
            ET.tostring(child, encoding="unicode") for child in element
        )
        return inner.strip()
    node: dict[str, Any] = {f"@{key}": value for key, value in element.attrib.items()}
    for child in element:
        value = element_to_dict(child)
        if child.tag in node:
            if not isinstance(node[child.tag], list):
                node[child.tag] = [node[child.tag]]
            node[child.tag].append(value)
        else:
            node[child.tag] = value
    text = (element.text or "").strip()
    if not node:
        return text or None
    if text:
        node["#text"] = text
    return node


def document_json(xml_documents: list[bytes]) -> bytes:
    """Merge a document's XML files (a text's version + struct) into one JSON payload.

    The keys are merged at the root, as Tricoteuses does for a JORF text: the
    version file brings META (with TITREFULL), the struct file brings STRUCT.
    """
    merged: dict[str, Any] = {}
    for payload in xml_documents:
        root = ET.fromstring(payload)
        converted = element_to_dict(root) or {}
        for key, value in converted.items():
            if key == "META" and isinstance(merged.get("META"), dict):
                _merge_meta(merged["META"], value)
            else:
                merged.setdefault(key, value)
    return json.dumps(merged, ensure_ascii=False, sort_keys=True).encode("utf-8")


def _merge_meta(into: dict[str, Any], other: dict[str, Any]) -> None:
    for key, value in other.items():
        if isinstance(into.get(key), dict) and isinstance(value, dict):
            _merge_meta(into[key], value)
        else:
            into.setdefault(key, value)


@dataclass(slots=True)
class KaliStore:
    """The local copy of the KALI dumps, and how it is kept current."""

    root: Path = field(default_factory=default_root)
    base_url: str = KALI_DUMP_BASE
    timeout_seconds: float = 600.0

    @property
    def tree(self) -> Path:
        return self.root / "global"

    @property
    def state_path(self) -> Path:
        return self.root / "state.json"

    def state(self) -> dict[str, str]:
        try:
            return json.loads(self.state_path.read_text())
        except (OSError, ValueError):
            return {}

    def read(self, source_id: str) -> tuple[list[bytes], str]:
        """The XML files for an id, and the dump they were last written by."""
        self.ensure_current()
        with self._locked(fcntl.LOCK_SH):  # never mid-sync of a parallel job
            files = []
            for relative in tree_paths(source_id):
                path = self.tree / relative
                if not path.exists():
                    msg = f"{source_id} is not in the KALI dumps (looked for {relative})"
                    raise FileNotFoundError(msg)
                files.append(path.read_bytes())
            return files, self.state().get("applied", "")

    @contextlib.contextmanager
    def _locked(self, mode: int):
        """A file lock on the copy: shared to read, exclusive to sync (the
        worker runs ingest jobs in parallel; each is its own process)."""
        self.root.mkdir(parents=True, exist_ok=True)
        with open(self.root / ".lock", "a") as handle:
            fcntl.flock(handle, mode)
            try:
                yield
            finally:
                fcntl.flock(handle, fcntl.LOCK_UN)

    def _fresh(self) -> bool:
        checked = self.state().get("checked_at")
        return bool(
            checked
            and self.tree.exists()
            and datetime.now(timezone.utc) - datetime.fromisoformat(checked) < SYNC_INTERVAL
        )

    def ensure_current(self) -> None:
        """Sync unless the copy was checked recently."""
        if self._fresh():
            return
        with self._locked(fcntl.LOCK_EX):
            if not self._fresh():  # a parallel job may have synced while we waited
                self._sync_unlocked()

    def sync(self) -> dict[str, Any]:
        """Bring the copy up to date (``cli kali-sync``), under the exclusive lock."""
        with self._locked(fcntl.LOCK_EX):
            return self._sync_unlocked()

    def _sync_unlocked(self) -> dict[str, Any]:
        """Bring the copy up to date: the global dump once, then each newer increment."""
        listing = self._listing()
        state = self.state()
        report: dict[str, Any] = {"global": None, "increments": []}
        if not self.tree.exists() or not state.get("global"):
            dumps = sorted(GLOBAL_DUMP.findall(listing))
            if not dumps:
                raise RuntimeError(f"no KALI global dump listed at {self.base_url}")
            stamp = dumps[-1]
            self._apply(f"Freemium_kali_global_{stamp}.tar.gz")
            state = {"global": stamp, "applied": stamp}
            report["global"] = stamp
        for stamp in sorted(set(INCREMENT_DUMP.findall(listing))):
            if stamp > state.get("applied", ""):
                self._apply(f"KALI_{stamp}.tar.gz")
                state["applied"] = stamp
                report["increments"].append(stamp)
        state["checked_at"] = datetime.now(timezone.utc).isoformat()
        self.root.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(json.dumps(state))
        return report

    def _listing(self) -> str:
        with httpx.Client(timeout=60.0, follow_redirects=True) as client:
            response = client.get(self.base_url)
            response.raise_for_status()
            return response.text

    def _apply(self, name: str) -> None:
        """Download one dump and write its kept members over the local tree."""
        self.root.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=self.root, suffix=".tar.gz") as handle:
            with httpx.stream("GET", self.base_url + name, timeout=self.timeout_seconds, follow_redirects=True) as response:
                response.raise_for_status()
                for block in response.iter_bytes(1 << 20):
                    handle.write(block)
            handle.flush()
            with tarfile.open(handle.name, "r:gz") as archive:
                for member in archive:
                    relative = _kept_relative(member.name)
                    if relative is None:
                        if member.isfile() and "suppression" in member.name:
                            self._delete_listed(archive.extractfile(member).read())
                        continue
                    if not member.isfile():
                        continue
                    target = self.tree / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with archive.extractfile(member) as source, open(target, "wb") as out:
                        shutil.copyfileobj(source, out)

    def _delete_listed(self, payload: bytes) -> None:
        """Apply an increment's deletion list (one dump-relative path per line)."""
        for line in payload.decode("utf-8", "replace").splitlines():
            relative = _kept_relative(line.strip())
            if relative:
                (self.tree / relative).with_suffix(".xml").unlink(missing_ok=True)


def _kept_relative(member: str) -> str | None:
    """The path under kali/global/ of a dump member we keep, else None."""
    _, marker, rest = member.partition("kali/global/")
    if not marker or not rest.startswith(KEPT_TREES):
        return None
    return rest


def kali_url(source_id: str, applied: str) -> str:
    """The snapshot URL: the dump tree path, pinned to the last dump applied."""
    return f"{KALI_DUMP_BASE}{tree_paths(source_id)[0]}#{applied}"


def fetch_kali(ref: SourceRef, http: SnapshotClient, store: KaliStore | None = None) -> Snapshot:
    """Read a KALI document from the local dump copy and archive it as DILA JSON."""
    store = store or KaliStore()
    files, applied = store.read(ref.source_id)
    return http.archive(ref, kali_url(ref.source_id, applied), document_json(files), "application/json")
