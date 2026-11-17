"""Web search on official domains (Tavily), with the process-wide quota latch.

Discovery only: a result's URL may name an instrument to ingest, its text is
never evidence. The scout (discovery, guidance search) and the RAG chat both
go through `web_search`.
"""

from __future__ import annotations

#: Set once the web-search provider has refused for good in this process —
#: Tavily answers HTTP 432 when the plan's usage limit is spent. Both eval runs
#: of 2026-09-09 (212 cases) hit it on every single query and the only trace
#: was a per-item error string: the scout ran blind for a whole evaluation and
#: nobody saw. Remember it, say it once, and stop paying a round trip per query.
_web_search_unavailable: str | None = None


QUOTA_EXHAUSTED = (
    "web search unavailable: the Tavily plan's usage limit is exhausted "
    "(HTTP 432) — discovery runs on the model's own instrument ids and "
    "the corpus lookup only until the quota resets or TAVILY_API_KEY changes"
)


class WebSearchUnavailable(RuntimeError):
    """Web search is off for the rest of this process (Tavily quota spent)."""


def unavailable() -> str | None:
    """Why web search is off for the rest of this process, or None."""
    return _web_search_unavailable


def web_search(api_key: str, query: str, domains: list[str]) -> list[dict]:
    """Tavily search on `domains`, with the one process-wide quota latch.

    HTTP 432 (plan limit spent) is recognised by status code, sets the latch
    and raises WebSearchUnavailable; every later call raises it at once. Other
    failures raise as they are. The scout and the RAG chat both call this —
    until 16 Nov 2026 each had its own latch and sniffed "432" in the
    exception text (code audit 4).
    """
    global _web_search_unavailable
    import httpx  # dependency of pydantic-ai

    if _web_search_unavailable:
        raise WebSearchUnavailable(_web_search_unavailable)
    try:
        return _tavily_search(api_key, query, domains)
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 432:
            _web_search_unavailable = QUOTA_EXHAUSTED
            raise WebSearchUnavailable(QUOTA_EXHAUSTED) from exc
        raise


def _tavily_search(api_key: str, query: str, domains: list[str]) -> list[dict]:
    import httpx  # dependency of pydantic-ai

    response = httpx.post(
        "https://api.tavily.com/search",
        json={
            "api_key": api_key,
            "query": query,
            "include_domains": domains,
            "max_results": 5,
        },
        timeout=30.0,
    )
    response.raise_for_status()
    return response.json().get("results", [])
