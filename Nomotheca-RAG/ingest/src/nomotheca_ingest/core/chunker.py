"""Chunk legal text into retrieval-sized slices with stable offsets."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ChunkIR:
    """A retrieval chunk derived from one language text."""

    seq: int
    char_start: int
    char_end: int
    content: str
    context_header: str


def chunk_text(content: str, context_header: str, max_chars: int = 6_000) -> list[ChunkIR]:
    """Split text into newline-aware chunks while preserving character offsets.

    An empty text (an abrogated article, a heading-only unit) has no chunk:
    a (0, 0) chunk breaks `chunks_check` and fails the whole act's load (the
    scout's ingests of loi 84-53 and of several KALI conventions in the 5 Nov run).
    """
    if not content:
        return []
    if len(content) <= max_chars:
        return [ChunkIR(seq=0, char_start=0, char_end=len(content), content=content, context_header=context_header)]

    chunks: list[ChunkIR] = []
    start = 0
    seq = 1
    while start < len(content):
        end = min(start + max_chars, len(content))
        if end < len(content):
            split_at = content.rfind("\n", start, end)
            if split_at > start:
                end = split_at
        chunks.append(ChunkIR(seq=seq, char_start=start, char_end=end, content=content[start:end], context_header=context_header))
        start = end
        while start < len(content) and content[start] == "\n":
            start += 1
        seq += 1
    return chunks
