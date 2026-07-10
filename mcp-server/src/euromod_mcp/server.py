"""MCP tool surface for the EUROMOD legislation database."""

from __future__ import annotations

import os
from dataclasses import asdict
from datetime import date
from typing import Literal

import psycopg
from mcp.server.fastmcp import FastMCP

from .encoder import QueryEncoder
from .search import get_chunk as fetch_chunk
from .search import search

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://jrc:jrc@localhost:5434/legislation",
)
BGE_M3_MODEL_ID = 1

mcp = FastMCP("EUROMOD legislation", json_response=True)
encoder = QueryEncoder()


def _connect() -> psycopg.Connection:
    return psycopg.connect(
        DATABASE_URL,
        options="-c default_transaction_read_only=on -c statement_timeout=30000",
    )


def _parse_as_of(value: str | None) -> date | None:
    if value is None:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("as_of must use ISO format YYYY-MM-DD") from exc


@mcp.tool()
def search_legislation(
    query: str,
    mode: Literal["hybrid", "full_text", "vector"] = "hybrid",
    country: str | None = None,
    as_of: str | None = None,
    languages: list[str] | None = None,
    limit: int = 8,
) -> dict:
    """Search citable fiscal legislation chunks.

    Use English queries freely: BGE-M3 performs multilingual vector retrieval.
    Filters are applied before ranking. Hybrid mode merges full-text and vector
    ranks with reciprocal rank fusion. Each result reports both component ranks
    and contributions so the model can explain why it was retrieved. Omit
    languages to search every stored language; pass ["en"] to search English
    translations only, or a country's official language for authoritative text.
    """
    query_vector = encoder.encode_literal(query) if mode in {"hybrid", "vector"} else None
    with _connect() as conn:
        hits = search(
            conn,
            query=query,
            mode=mode,
            query_vector=query_vector,
            country=country,
            as_of=_parse_as_of(as_of),
            languages=languages,
            model_id=BGE_M3_MODEL_ID,
            limit=limit,
        )
    return {
        "query": query,
        "mode": mode,
        "filters": {"country": country, "as_of": as_of, "languages": languages},
        "model_id": BGE_M3_MODEL_ID if query_vector else None,
        "ranking": "RRF(k=60) over full-text and vector ranks" if mode == "hybrid" else mode,
        "result_count": len(hits),
        "results": [asdict(hit) for hit in hits],
    }


@mcp.tool()
def get_legislation_chunk(chunk_id: str) -> dict:
    """Get an exact citable chunk and provenance by its database UUID."""
    with _connect() as conn:
        hit = fetch_chunk(conn, chunk_id)
    if hit is None:
        raise ValueError(f"Chunk not found: {chunk_id}")
    return asdict(hit)


def main() -> None:
    """Run the local stdio MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
