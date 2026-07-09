"""Build vector embeddings for retrieval chunks."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from hashlib import sha256
from typing import Protocol
from uuid import UUID

from psycopg import Connection
from psycopg.rows import dict_row


BGE_M3_MODEL = "BAAI/bge-m3"
BGE_M3_DIM = 1024
EMBEDDING_BACKENDS = ("torch", "openvino")


@dataclass(frozen=True, slots=True)
class ChunkForEmbedding:
    """A chunk row and the text that should be embedded."""

    id: UUID
    input_text: str
    input_hash: str


@dataclass(frozen=True, slots=True)
class EmbeddingBuildStats:
    """Counts returned by an embedding build run."""

    scanned: int = 0
    embedded: int = 0
    skipped: int = 0


class EmbeddingBackend(Protocol):
    """Minimal interface used by the database embedding builder."""

    def encode(self, inputs: Sequence[str]) -> list[list[float]]:
        """Return one 1024-dimensional embedding per input string."""


class SentenceTransformerBackend:
    """Local sentence-transformers backend for BGE-M3."""

    def __init__(self, model_path: str = BGE_M3_MODEL, device: str | None = None, backend: str = "torch") -> None:
        """Load a local or Hugging Face model path lazily."""
        if backend not in EMBEDDING_BACKENDS:
            msg = f"Unsupported embedding backend: {backend}"
            raise ValueError(msg)
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:  # pragma: no cover - exercised by operator environment
            msg = "Install embedding dependencies with: uv sync --extra embeddings"
            raise RuntimeError(msg) from exc

        self.model = SentenceTransformer(model_path, device=device, backend=backend)

    def encode(self, inputs: Sequence[str]) -> list[list[float]]:
        """Encode passage inputs as normalized BGE-M3 embeddings."""
        vectors = self.model.encode(
            list(inputs),
            batch_size=len(inputs),
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return [vector.astype(float).tolist() for vector in vectors]


def build_embeddings(
    conn: Connection,
    backend: EmbeddingBackend,
    *,
    model_id: int = 1,
    batch_size: int = 16,
    limit: int | None = None,
    dry_run: bool = False,
) -> EmbeddingBuildStats:
    """Embed chunks missing a fresh row for the requested model."""
    if not dry_run:
        ensure_bge_m3_model(conn, model_id=model_id)

    stats = EmbeddingBuildStats()
    batch: list[ChunkForEmbedding] = []

    for chunk in iter_chunks_needing_embeddings(conn, model_id=model_id, limit=limit):
        stats = EmbeddingBuildStats(stats.scanned + 1, stats.embedded, stats.skipped)
        batch.append(chunk)
        if len(batch) >= batch_size:
            embedded = _embed_batch(conn, backend, batch, model_id=model_id, dry_run=dry_run)
            stats = EmbeddingBuildStats(stats.scanned, stats.embedded + embedded, stats.skipped)
            batch = []

    if batch:
        embedded = _embed_batch(conn, backend, batch, model_id=model_id, dry_run=dry_run)
        stats = EmbeddingBuildStats(stats.scanned, stats.embedded + embedded, stats.skipped)

    return stats


def iter_chunks_needing_embeddings(
    conn: Connection,
    *,
    model_id: int = 1,
    limit: int | None = None,
) -> Iterable[ChunkForEmbedding]:
    """Yield chunks whose embedding row is missing or stale."""
    yielded = 0
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """
            SELECT c.id, c.context_header, c.content, e.input_hash
            FROM chunks c
            LEFT JOIN embeddings e ON e.chunk_id = c.id AND e.model_id = %s
            ORDER BY c.id
            """,
            (model_id,),
        )
        for row in cur:
            input_text = embedding_input(row["context_header"], row["content"])
            input_hash = embedding_input_hash(input_text)
            if row["input_hash"] == input_hash:
                continue
            yield ChunkForEmbedding(id=row["id"], input_text=input_text, input_hash=input_hash)
            yielded += 1
            if limit is not None and yielded >= limit:
                return


def ensure_bge_m3_model(conn: Connection, *, model_id: int = 1) -> None:
    """Ensure the BGE-M3 model registry row exists."""
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO embedding_models
              (id, name, provider, native_dim, stored_dim, normalize, is_default, config)
            VALUES (%s, 'bge-m3', 'self-hosted', %s, %s, true, true, '{"context": 8192}'::jsonb)
            ON CONFLICT (id) DO NOTHING
            """,
            (model_id, BGE_M3_DIM, BGE_M3_DIM),
        )


def embedding_input(context_header: str, content: str) -> str:
    """Return the canonical text passed to the embedding model."""
    return f"{context_header}\n{content}"


def embedding_input_hash(input_text: str) -> str:
    """Hash the exact model input for stale-vector detection."""
    return sha256(input_text.encode("utf-8")).hexdigest()


def halfvec_literal(vector: Sequence[float]) -> str:
    """Serialize a vector for insertion into PostgreSQL halfvec."""
    if len(vector) != BGE_M3_DIM:
        msg = f"Expected {BGE_M3_DIM} dimensions, got {len(vector)}"
        raise ValueError(msg)
    return "[" + ",".join(f"{float(value):.8g}" for value in vector) + "]"


def _embed_batch(
    conn: Connection,
    backend: EmbeddingBackend,
    batch: Sequence[ChunkForEmbedding],
    *,
    model_id: int,
    dry_run: bool,
) -> int:
    """Encode and persist a batch of chunks."""
    if dry_run:
        return len(batch)

    vectors = backend.encode([chunk.input_text for chunk in batch])
    if len(vectors) != len(batch):
        msg = f"Backend returned {len(vectors)} vectors for {len(batch)} inputs"
        raise ValueError(msg)

    with conn.transaction():
        with conn.cursor() as cur:
            for chunk, vector in zip(batch, vectors, strict=True):
                cur.execute(
                    """
                    INSERT INTO embeddings (chunk_id, model_id, embedding, input_hash)
                    VALUES (%s, %s, %s::halfvec, %s)
                    ON CONFLICT (chunk_id, model_id) DO UPDATE
                    SET embedding = EXCLUDED.embedding,
                        input_hash = EXCLUDED.input_hash,
                        embedded_at = now()
                    """,
                    (chunk.id, model_id, halfvec_literal(vector), chunk.input_hash),
                )
    return len(batch)