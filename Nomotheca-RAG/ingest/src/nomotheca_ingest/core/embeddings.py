"""The embedding build: chunks lacking a fresh vector, encoded and stored.

The model and its hardware are `core.embedding_backend`.
"""

from __future__ import annotations

import os
import sys
import time
from collections.abc import Callable, Iterable, Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date
from uuid import UUID

import psycopg
from psycopg import Connection
from psycopg.conninfo import make_conninfo
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

# The model/hardware half, re-exported: other packages (the worker's encode
# lane) import the backend from here.
from nomotheca_ingest.core.embedding_backend import (  # noqa: F401
    AUTO_DEVICE,
    BGE_M3_DIM,
    BGE_M3_MODEL,
    CUDA_BF16_MIN_CAPABILITY,
    CUDA_FP16_MIN_CAPABILITY,
    CUDA_INSTALL_HINT,
    DEFAULT_MAX_SEQ_LENGTH,
    EMBEDDING_BACKENDS,
    PRECISIONS,
    TORCH_WRAPPER_DEVICE,
    EmbeddingBackend,
    SentenceTransformerBackend,
    arch_list_supports,
    cuda_dtype_for,
    cuda_oom_errors,
    describe_backend,
    is_cuda_device,
    processor_kwargs_for,
    raise_for_unsupported_cuda_arch,
    resolve_torch_device,
    sentence_transformer_load_kwargs,
    torch_module,
)
from nomotheca_ingest.core.embedding_models import DEFAULT_MODEL, EmbeddingModelSpec, get_model
from nomotheca_ingest.core.progress import BatchStats, ProgressCallback, emit
from nomotheca_ingest.core.text import sha256_hex


@dataclass(frozen=True, slots=True)
class ChunkForEmbedding:
    """A chunk row and the text that should be embedded."""

    id: UUID
    input_text: str
    input_hash: str



# ---------------------------------------------------------------------------
# One build at a time
# ---------------------------------------------------------------------------

#: pg advisory lock key held by every non-dry-run embeddings build.
EMBEDDING_BUILD_LOCK_KEY = 0x656D6264  # "embd"

#: Seconds between two tries of the lock while another build holds it.
EMBEDDING_LOCK_POLL_SECONDS = 5.0

#: The connection holding the lock in this process, while one does.
_embedding_lock_conn: psycopg.Connection | None = None

#: Told when the build starts waiting for the lock and when it gets it:
#: ``on_wait(phase, detail)`` with phase "waiting" or "starting".
LockWaitCallback = Callable[[str, str], None]


def embedding_lock_application_name() -> str:
    """How this build's lock connection names itself in ``pg_stat_activity``,
    so a waiting build can say who it waits for: the worker job it runs under
    (``WORKER_JOB_ID``; a scout build inherits its workflow/eval job's), else
    the host process."""
    job = os.environ.get("WORKER_JOB_ID")
    where = f"job #{job}" if job else f"pid {os.getpid()} on {os.uname().nodename}"
    return f"embeddings build ({where})"[:63]  # NAMEDATALEN - 1


def _embedding_lock_holder(conn: psycopg.Connection) -> str:
    """Describe the session holding the build lock (empty when none does)."""
    row = conn.execute(
        """
        SELECT a.application_name, host(a.client_addr), a.backend_start
          FROM pg_locks l
          JOIN pg_stat_activity a ON a.pid = l.pid
         WHERE l.locktype = 'advisory' AND l.granted
           AND l.classid = 0 AND l.objid = %s AND l.objsubid = 1
        """,
        (EMBEDDING_BUILD_LOCK_KEY,),
    ).fetchone()
    if row is None:
        return ""
    name, addr, since = row
    who = name or f"a connection from {addr or 'an unknown host'}"
    return f"{who}, since {since:%H:%M:%S %Z}" if since else who


@contextmanager
def embedding_build_lock(conninfo: str, on_wait: LockWaitCallback | None = None) -> Iterator[None]:
    """Hold the one-build-at-a-time lock for the duration of the block.

    Whoever starts a build (an embed job, the scout's cache-miss build inside
    a workflow/eval job, a hand-run build, a library caller): two BGE-M3
    copies overflow the GPU next to the worker's encode lane, and both would
    embed the same backlog. Re-entrant within a process — the CLI takes it
    before loading the model, `build_embeddings` takes it again.

    While it waits it says so — on stderr, and through ``on_wait`` naming the
    holder, so the worker's job row reads "waiting" rather than "running". It
    polls rather than blocking in ``pg_advisory_lock`` so a change of holder
    is reported too. Released when the block ends (its connection closes).
    """
    global _embedding_lock_conn  # noqa: PLW0603 - one lock per process
    if _embedding_lock_conn is not None:
        yield
        return
    conn = psycopg.connect(conninfo, autocommit=True, application_name=embedding_lock_application_name())
    try:
        reported = None
        waited = False
        while not conn.execute("SELECT pg_try_advisory_lock(%s)", (EMBEDDING_BUILD_LOCK_KEY,)).fetchone()[0]:
            holder = _embedding_lock_holder(conn)
            if holder != reported:
                detail = f"waiting for the GPU: another embeddings build holds it — {holder or 'just released'}"
                print(detail + "…", file=sys.stderr, flush=True)
                if on_wait is not None:
                    on_wait("waiting", detail)
                reported = holder
            waited = True
            time.sleep(EMBEDDING_LOCK_POLL_SECONDS)
        if waited:
            print("embeddings build lock acquired", file=sys.stderr, flush=True)
            if on_wait is not None:
                on_wait("starting", "lock acquired, loading model")
        _embedding_lock_conn = conn
        yield
    finally:
        _embedding_lock_conn = None
        conn.close()


def _conninfo(conn: Connection) -> str:
    """Connection string reaching the same database as ``conn`` (password included)."""
    return make_conninfo(conn.info.dsn, password=conn.info.password)


def build_embeddings(
    conn: Connection,
    backend: EmbeddingBackend,
    *,
    model_id: int = 1,
    batch_size: int = 16,
    limit: int | None = None,
    dry_run: bool = False,
    progress: ProgressCallback | None = None,
    commit_each_batch: bool = False,
    authentic_only: bool = False,
    langs: Sequence[str] | None = None,
    in_force_on: Sequence[date] | None = None,
    lock: bool = True,
) -> BatchStats:
    """Embed chunks missing a fresh row for the requested model.

    A real build (not a dry run) holds `embedding_build_lock` throughout,
    so two builds never share the GPU; ``lock=False`` is for tests only.

    With commit_each_batch, every embedded batch is committed as it lands so a
    killed or timed-out run keeps the vectors already computed — embedding is
    minutes of CPU work, and the input-hash check makes re-runs resume cleanly.

    `authentic_only` / `langs` / `in_force_on` narrow the build to what
    evidence retrieval searches (the law's own text, in the country's
    language, on the dates asked): a candidate model under evaluation does not
    need the ~16k machine-translated chunks nor every superseded version.
    """
    scope = {"authentic_only": authentic_only, "langs": langs, "in_force_on": in_force_on}
    run = lambda: _build(  # noqa: E731
        conn, backend, model_id=model_id, batch_size=batch_size, limit=limit, dry_run=dry_run,
        progress=progress, commit_each_batch=commit_each_batch, **scope,
    )
    if dry_run or not lock:
        return run()

    def on_wait(phase: str, detail: str) -> None:
        emit(progress, phase, BatchStats(), detail=detail)

    with embedding_build_lock(_conninfo(conn), on_wait):
        return run()


def _build(
    conn: Connection,
    backend: EmbeddingBackend,
    *,
    model_id: int,
    batch_size: int,
    limit: int | None,
    dry_run: bool,
    progress: ProgressCallback | None,
    commit_each_batch: bool,
    authentic_only: bool,
    langs: Sequence[str] | None,
    in_force_on: Sequence[date] | None,
) -> BatchStats:
    if not dry_run:
        ensure_embedding_model(conn, get_model(model_id))
        if commit_each_batch:
            conn.commit()  # the model row must survive even if the first batch doesn't

    stats = BatchStats()
    batch: list[ChunkForEmbedding] = []

    chunks = iter_chunks_needing_embeddings(
        conn,
        model_id=model_id,
        limit=limit,
        authentic_only=authentic_only,
        langs=langs,
        in_force_on=in_force_on,
    )
    for chunk in chunks:
        stats = stats.plus(scanned=1)
        batch.append(chunk)
        emit(progress, "candidate", stats, batch_size=len(batch))
        if len(batch) >= batch_size:
            emit(progress, "encoding", stats, batch_size=len(batch))
            embedded, skipped = _embed_batch(conn, backend, batch, model_id=model_id, dry_run=dry_run)
            if commit_each_batch and not dry_run:
                conn.commit()
            stats = stats.plus(done=embedded, skipped=skipped)
            emit(progress, "embedded", stats, batch_size=embedded)
            batch = []

    if batch:
        emit(progress, "encoding", stats, batch_size=len(batch))
        embedded, skipped = _embed_batch(conn, backend, batch, model_id=model_id, dry_run=dry_run)
        stats = stats.plus(done=embedded, skipped=skipped)
        emit(progress, "embedded", stats, batch_size=embedded)

    emit(progress, "done", stats)

    return stats


_SCOPE_FILTER = """
  AND (NOT %(authentic_only)s OR t.authenticity <> 'machine_translation')
  AND (%(langs)s::text[] IS NULL OR t.lang = ANY(%(langs)s::text[]))
  AND (%(in_force_on)s::date[] IS NULL OR EXISTS (
        SELECT 1 FROM legal_unit_versions v, unnest(%(in_force_on)s::date[]) AS d(day)
        WHERE v.id = t.version_id AND v.validity @> d.day))
"""


def _scope_params(
    model_id: int,
    authentic_only: bool,
    langs: Sequence[str] | None,
    in_force_on: Sequence[date] | None = None,
) -> dict[str, object]:
    return {
        "model_id": model_id,
        "authentic_only": authentic_only,
        "langs": list(langs) if langs else None,
        "in_force_on": list(in_force_on) if in_force_on else None,
    }


def iter_chunks_needing_embeddings(
    conn: Connection,
    *,
    model_id: int = 1,
    limit: int | None = None,
    authentic_only: bool = False,
    langs: Sequence[str] | None = None,
    in_force_on: Sequence[date] | None = None,
) -> Iterable[ChunkForEmbedding]:
    """Yield chunks whose embedding row is missing or stale."""
    yielded = 0
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            f"""
            SELECT c.id, c.context_header, c.content, e.input_hash
            FROM chunks c
            JOIN unit_texts t ON t.id = c.unit_text_id
            LEFT JOIN embeddings e ON e.chunk_id = c.id AND e.model_id = %(model_id)s
            WHERE true {_SCOPE_FILTER}
            ORDER BY c.id
            """,
            _scope_params(model_id, authentic_only, langs, in_force_on),
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


def count_chunks_needing_embeddings(
    conn: Connection,
    *,
    model_id: int = 1,
    limit: int | None = None,
    authentic_only: bool = False,
    langs: Sequence[str] | None = None,
    in_force_on: Sequence[date] | None = None,
) -> int:
    """Count the chunks `iter_chunks_needing_embeddings` would yield.

    SQL twin of the iterator's staleness check: sha256(context_header + "\\n" +
    content) compared against the stored input_hash, so a progress display can
    know the total before the scan starts.
    """
    with conn.cursor() as cur:
        cur.execute(
            f"""
            SELECT count(*)
            FROM chunks c
            JOIN unit_texts t ON t.id = c.unit_text_id
            LEFT JOIN embeddings e ON e.chunk_id = c.id AND e.model_id = %(model_id)s
            WHERE e.input_hash IS DISTINCT FROM
                  encode(sha256(convert_to(c.context_header || chr(10) || c.content, 'UTF8')), 'hex')
            {_SCOPE_FILTER}
            """,
            _scope_params(model_id, authentic_only, langs, in_force_on),
        )
        total = int(cur.fetchone()[0])
    return min(total, limit) if limit is not None else total


def hnsw_index_sql(model_id: int) -> str:
    """The partial HNSW index every embedding model gets (schema.sql's rule).

    `model_id` is an int from the registry, never user input.
    """
    model_id = int(model_id)
    return (
        f"CREATE INDEX IF NOT EXISTS emb_hnsw_m{model_id} ON embeddings "
        "USING hnsw (embedding halfvec_cosine_ops) WITH (m = 16, ef_construction = 200) "
        f"WHERE model_id = {model_id}"
    )


def ensure_embedding_model(conn: Connection, spec: EmbeddingModelSpec) -> None:
    """Ensure the model's `embedding_models` row and partial HNSW index exist.

    An existing row is left alone: `is_default` is an operator's decision and
    the seeded BGE-M3 row predates the registry's config keys. Until 16 Nov
    2026 only the row was inserted, so models 2, 5, 6 and 8 had no index
    (code audit D16).
    """
    row = spec.registry_row()
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO embedding_models
              (id, name, provider, native_dim, stored_dim, normalize, is_default, config)
            VALUES (%s, %s, %s, %s, %s, true, %s, %s)
            ON CONFLICT (id) DO NOTHING
            """,
            (
                row["id"],
                row["name"],
                row["provider"],
                row["native_dim"],
                row["stored_dim"],
                spec.id == DEFAULT_MODEL.id,
                Jsonb(row["config"]),
            ),
        )
        cur.execute(hnsw_index_sql(spec.id))


def embedding_input(context_header: str, content: str) -> str:
    """Return the canonical text passed to the embedding model."""
    return f"{context_header}\n{content}"


def embedding_input_hash(input_text: str) -> str:
    """Hash the exact model input for stale-vector detection."""
    return sha256_hex(input_text)


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
) -> tuple[int, int]:
    """Encode and persist a batch of chunks, returning (embedded, skipped).

    The candidate list is read before encoding, which takes minutes, so a
    concurrent ingest can retire a chunk id in between: `write_chunks` upserts
    a text's chunks on (unit_text_id, seq) and deletes the seqs a shorter text
    no longer produces. Inserting against `chunks` instead of blind-inserting
    the id drops those vanished chunks rather than failing the run on the
    foreign key; changed chunks keep their id and are re-embedded by the next
    build once their input_hash differs.
    """
    if dry_run:
        return len(batch), 0

    vectors = backend.encode([chunk.input_text for chunk in batch])
    if len(vectors) != len(batch):
        msg = f"Backend returned {len(vectors)} vectors for {len(batch)} inputs"
        raise ValueError(msg)

    embedded = 0
    with conn.transaction():
        with conn.cursor() as cur:
            for chunk, vector in zip(batch, vectors, strict=True):
                cur.execute(
                    """
                    INSERT INTO embeddings (chunk_id, model_id, embedding, input_hash)
                    SELECT c.id, %s, %s::halfvec, %s
                    FROM chunks c
                    WHERE c.id = %s
                    ON CONFLICT (chunk_id, model_id) DO UPDATE
                    SET embedding = EXCLUDED.embedding,
                        input_hash = EXCLUDED.input_hash,
                        embedded_at = now()
                    """,
                    (model_id, halfvec_literal(vector), chunk.input_hash, chunk.id),
                )
                embedded += cur.rowcount
    return embedded, len(batch) - embedded