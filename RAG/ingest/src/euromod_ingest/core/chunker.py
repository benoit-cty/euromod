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
    """Split text into newline-aware chunks while preserving character offsets."""
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
