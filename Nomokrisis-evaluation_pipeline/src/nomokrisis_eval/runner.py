"""Run the agentic workflow over the golden set and score each case.

Reuses nomoscope_workflow end-to-end (same retrieval, prompts, critique, Phoenix
tracing) with `enqueue=False`, so evaluation runs never touch the human review
queue: the ReviewItem comes back to the runner, is scored, and is stored with
its result.

A run is crash-safe and lives in the database alone (ADR 0004): the eval.runs
row (`status='running'`) and the frozen case list (eval.run_cases) are written
before the first case, and every scored case is upserted into eval.results the
moment it lands. An interrupted run is therefore resumable — see `resume_run`,
which reloads the manifest, the frozen list and what is already scored from
those tables and skips the latter.
"""

from __future__ import annotations

import re
import time
import uuid
from collections.abc import Callable
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from datetime import date, datetime, timezone

import psycopg

from nomoscope_workflow import AGENT_VERSION, paramdb
from nomoscope_workflow.config import WorkflowConfig, load_config as load_workflow_config
from nomoscope_workflow.impact import trace_impact
from nomoscope_workflow.pipeline import run_parameter
from nomoscope_workflow.prompts import PROMPT_VERSION
from nomoscope_workflow.schema import ParameterRecord, ReviewItem
from nomoscope_workflow.tracing import setup_tracing

from . import eval_version
from . import db as evaldb
from .config import EvalConfig, git_commit
from .golden_store import golden_set_hash, load_cases
from .parameter_store import db_constants, load_case_record
from .schema import CaseResult, GoldenCase, RunManifest
from .scoring import score_item

def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _constants_for(
    conn: psycopg.Connection, cases: list[GoldenCase]
) -> Callable[[GoldenCase], dict[str, object] | None]:
    """$-constants for a case, read at that case's own as_of (cached per date)."""
    cache: dict[tuple[str, date], dict[str, object]] = {}

    def lookup(case: GoldenCase) -> dict[str, object] | None:
        key = (case.country.upper(), case.as_of)
        if key not in cache:
            cache[key] = db_constants(conn, key[0], key[1])
        return cache[key]

    for case in cases:  # read up front, on the main thread
        lookup(case)
    return lookup


def list_runs(conn: psycopg.Connection, limit: int | None = None) -> list[dict]:
    """Every run in eval.runs, newest first, with done/total progress."""
    return evaldb.list_runs(conn, limit=limit)


def latest_incomplete_run(conn: psycopg.Connection) -> dict | None:
    for run in list_runs(conn):
        if not run["complete"] and run["total"]:
            return run
    return None


# --------------------------------------------------------------------------- #
# Running
# --------------------------------------------------------------------------- #


def _resolved_model_name(model: str) -> str | None:
    """The model name the provider layer will actually call (None for mock/).

    For azure_openai/ this is the deployment. It is what Phoenix records on the
    LLM spans, so the manifest can be checked against the traces — and against
    the other run's manifest — before two runs are compared as two models."""
    if model.partition("/")[0] == "mock":
        return None
    try:
        from nomoscope_workflow.llm import get_model

        return str(get_model(model).model_name)
    except Exception as exc:  # missing key/endpoint: the run itself will fail loudly
        return f"unresolved: {type(exc).__name__}"


def critique_model_for(cfg: EvalConfig, model: str) -> str:
    """The model that will run the critique step: the pinned judge when
    EVAL_CRITIQUE_MODEL is set, else the model under test grading itself."""
    return cfg.critique_model or model


def start_run(
    conn: psycopg.Connection,
    cfg: EvalConfig,
    cases: list[GoldenCase],
    as_of: date,
    model: str,
    notes: str | None = None,
    blind_before: date | None = None,
) -> RunManifest:
    """Allocate a run id, insert the eval.runs row (`status='running'`,
    `submitted_by` = current_user, `dataset_version` = the golden set hash of
    exactly these cases) and freeze the case list into eval.run_cases."""
    provider, _, model_name = model.partition("/")
    run_id = f"eval-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-{_slug(model_name or provider)}-{uuid.uuid4().hex[:6]}"
    manifest = RunManifest(
        run_id=run_id,
        created_at=datetime.now(timezone.utc),
        status="running",
        as_of=as_of,
        model=model,
        model_provider=provider,
        model_name=model_name or provider,
        critique_model=critique_model_for(cfg, model),
        resolved_model=_resolved_model_name(model),
        resolved_critique_model=_resolved_model_name(critique_model_for(cfg, model)),
        prompt_version=PROMPT_VERSION,
        agent_version=AGENT_VERSION,
        eval_version=eval_version(),
        dataset_version=golden_set_hash(cases),
        git_commit=git_commit(),
        countries=sorted({c.country for c in cases}),
        notes=notes,
        blind_before=blind_before,
    )
    run_pk = evaldb.insert_run(conn, manifest)
    evaldb.freeze_run_cases(conn, run_pk, cases)
    loaded = evaldb.load_run(conn, run_id)
    return loaded[1] if loaded else manifest


def resume_run(
    conn: psycopg.Connection, run_id: str
) -> tuple[RunManifest, list[GoldenCase], list[CaseResult]]:
    """Reload an interrupted run from the tables: its manifest, its frozen case
    list, and what it already scored. Raises LookupError if it cannot be resumed."""
    loaded = evaldb.load_run(conn, run_id)
    if loaded is None:
        raise LookupError(f"no evaluation run {run_id} in eval.runs")
    run_pk, manifest = loaded
    cases = evaldb.load_run_cases(conn, run_pk)
    if not cases:
        raise LookupError(
            f"run {run_id} predates resumable runs (no rows in eval.run_cases) — start a new run"
        )
    return manifest, cases, evaldb.load_results(conn, run_pk)


def golden_set_drift(conn: psycopg.Connection, manifest: RunManifest) -> str | None:
    """Today's verified golden-set hash when it differs from the one the run
    froze, else None. A resumed run replays its frozen case list either way;
    this only says the golden set moved since. A benchmark run's cases come
    from the params DB, not the golden set, so it never drifts."""
    if manifest.blind_before is not None:
        return None
    current = golden_set_hash(load_cases(conn, verified_only=True))
    return current if current != manifest.dataset_version else None


def _workflow_config(cfg: EvalConfig, manifest: RunManifest) -> WorkflowConfig:
    wf_cfg = load_workflow_config()
    wf_cfg.model = manifest.model
    # Older manifests (before the judge could be pinned) have no critique_model;
    # they graded themselves, so replaying them must keep doing that.
    wf_cfg.critique_model = manifest.critique_model or manifest.model
    wf_cfg.phoenix_project = cfg.phoenix_project
    return wf_cfg


def _error_result(case: GoldenCase, exc: BaseException) -> CaseResult:
    return CaseResult(
        case_id=case.id,
        country=case.country,
        language=case.language,
        difficulty=case.difficulty,
        hazards=list(case.hazards),
        source_class=case.source_class,
        routing_expected=case.expected.routing.value,
        corpus_available=case.corpus_available,
        readiness=case.readiness,
        error=f"{exc.__class__.__name__}: {exc}",
    )


def execute_run(
    conn: psycopg.Connection,
    cfg: EvalConfig,
    manifest: RunManifest,
    cases: list[GoldenCase],
    done_results: list[CaseResult] | None = None,
    on_case_start: Callable[[int, int, GoldenCase], None] | None = None,
    on_case_done: Callable[[int, int, GoldenCase, CaseResult], None] | None = None,
    run_case: Callable[[WorkflowConfig, object, ParameterRecord, GoldenCase, date], ReviewItem] | None = None,
    concurrency: int = 1,
) -> list[CaseResult]:
    """Score every case not already in `done_results`, persisting as it goes.

    Each result is upserted into eval.results (with the ReviewItem) the moment
    the case is scored, so a Ctrl-C (or a crash) loses at most the cases in
    flight; the run is flipped to `complete` at the end. A crash — an exception
    that is not a case's own error result — marks it `failed` and re-raises; a
    Ctrl-C leaves it `running`. Either way `resume` picks it up. `run_case`
    exists for tests — it replaces the workflow call and nothing else.

    `concurrency` cases run their workflow at once, each in its own thread:
    a case is almost all LLM latency (a reasoning model on OpenRouter spends
    ~25 s per call, ~6 calls per case), and `run_parameter` opens its own
    connections, so cases do not share state. Everything touching `conn` —
    loading the record, scoring, upserting, the callbacks — stays on this
    thread. Results land in completion order, not case order; the scout's
    GPU work is serialised by the embeddings-build advisory lock.
    """
    loaded = evaldb.load_run(conn, manifest.run_id)
    if loaded is None:
        raise LookupError(f"run {manifest.run_id} is not in eval.runs — start_run first")
    run_pk = loaded[0]
    evaldb.set_run_status(conn, run_pk, "running")
    try:
        results = _score_pending(
            conn, cfg, manifest, run_pk, cases, done_results,
            on_case_start, on_case_done, run_case, concurrency,
        )
    except Exception:
        try:
            conn.rollback()
            evaldb.set_run_status(conn, run_pk, "failed")
            manifest.status = "failed"
        except Exception:  # noqa: BLE001 - the original error is the one to raise
            pass
        raise
    evaldb.set_run_status(conn, run_pk, "complete")
    manifest.status = "complete"
    return results


def _score_pending(
    conn: psycopg.Connection,
    cfg: EvalConfig,
    manifest: RunManifest,
    run_pk: int,
    cases: list[GoldenCase],
    done_results: list[CaseResult] | None,
    on_case_start: Callable[[int, int, GoldenCase], None] | None,
    on_case_done: Callable[[int, int, GoldenCase, CaseResult], None] | None,
    run_case: Callable[[WorkflowConfig, object, ParameterRecord, GoldenCase, date], ReviewItem] | None,
    concurrency: int,
) -> list[CaseResult]:
    """execute_run's case loop: every result scored and upserted as it lands."""
    results = list(done_results or [])
    scored = {r.case_id for r in results}
    pending = [c for c in cases if c.id not in scored]

    wf_cfg = _workflow_config(cfg, manifest)
    tracer = setup_tracing(wf_cfg)
    constants_of = _constants_for(conn, cases)
    total = len(cases)
    started_count = len(results)

    def workflow(record: ParameterRecord, case: GoldenCase) -> ReviewItem:
        # Each case runs on the date its ground truth was established for. Until
        # 16 Nov 2026 every case ran on the run's as_of, so a case drafted for
        # another date (or another system year) was scored against a value in
        # force on a day its expectation never described (code audit D14).
        if run_case is not None:
            return run_case(wf_cfg, tracer, record, case, case.as_of)
        return run_parameter(
            wf_cfg, tracer, record, case.as_of,
            force=True, parameter_ref=case.parameter_target, enqueue=False,
        )

    def timed(record: ParameterRecord, case: GoldenCase) -> tuple[ReviewItem | None, BaseException | None, float]:
        started = time.perf_counter()
        try:
            return workflow(record, case), None, started
        except Exception as exc:  # scored as an error result, the run goes on
            return None, exc, started

    def finish(case: GoldenCase, item: ReviewItem | None, exc: BaseException | None, started: float) -> None:
        if exc is None and item is not None:
            try:
                result = score_item(case, item, constants_of(case))
            except Exception as score_exc:
                result = _error_result(case, score_exc)
        else:
            result = _error_result(case, exc or RuntimeError("no review item"))
        result.latency_ms = int((time.perf_counter() - started) * 1000)
        results.append(result)
        evaldb.upsert_result(
            conn, run_pk, result, item.model_dump(mode="json") if item is not None else None
        )
        if on_case_done:
            on_case_done(len(results), total, case, result)

    def load(case: GoldenCase) -> ParameterRecord | None:
        nonlocal started_count
        started_count += 1
        if on_case_start:
            on_case_start(started_count, total, case)
        try:
            record = load_case_record(conn, case.parameter_target)
            if manifest.blind_before is not None:
                record = paramdb.blind_record(record, manifest.blind_before)
            return record
        except Exception as exc:
            conn.rollback()
            finish(case, None, exc, time.perf_counter())
            return None

    queue = list(pending)
    with ThreadPoolExecutor(max_workers=max(1, concurrency), thread_name_prefix="eval-case") as pool:
        in_flight: dict[Future, GoldenCase] = {}
        try:
            while queue or in_flight:
                while queue and len(in_flight) < max(1, concurrency):
                    case = queue.pop(0)
                    record = load(case)
                    if record is not None:
                        in_flight[pool.submit(timed, record, case)] = case
                if not in_flight:
                    continue
                done, _ = wait(in_flight, return_when=FIRST_COMPLETED)
                for future in done:
                    case = in_flight.pop(future)
                    finish(case, *future.result())
        except BaseException:
            # Ctrl-C: drop what has not started; the cases in flight are lost
            # (resume re-runs them) — the pool still waits for their threads.
            pool.shutdown(wait=False, cancel_futures=True)
            raise

    if not manifest.model.startswith("mock") and pending:
        if _attach_impact(results, wf_cfg):
            for result in results:
                if result.llm_calls is not None:
                    evaldb.upsert_result(conn, run_pk, result)
    return results


def rescore_run(conn: psycopg.Connection, run_id: str) -> tuple[RunManifest, list[CaseResult], list[CaseResult]]:
    """Re-score a finished run from the ReviewItems it stored — no LLM.

    Every eval.results row keeps the ReviewItem the pipeline produced, so a fix
    to `scoring.py` can be re-applied to past runs instead of re-spending a
    full run's tokens. Only the scoring moves: routing, values, citations and
    retrieval traces stay exactly what the model produced at the time.

    Expectations come from the run's frozen eval.run_cases, never from today's
    golden set — so a rescore isolates the effect of a scoring change from any
    golden-set edit. To measure a golden-set change instead, start a new run.
    Latency and impact columns are carried over from the previous results: they
    are measurements, not scores, and cannot be recomputed offline.

    Returns (manifest, previous results, rescored results).
    """
    loaded = evaldb.load_run(conn, run_id)
    if loaded is None:
        raise LookupError(f"no evaluation run {run_id} in eval.runs")
    run_pk, manifest = loaded
    cases = {case.id: case for case in evaldb.load_run_cases(conn, run_pk)}
    previous_list = evaldb.load_results(conn, run_pk)
    previous = {r.case_id: r for r in previous_list}
    items = evaldb.load_review_items(conn, run_pk)
    constants_of = _constants_for(conn, list(cases.values()))

    rescored: list[CaseResult] = []
    for case_id, case in cases.items():
        before = previous.get(case_id)
        if before is None:
            continue
        item_dump = items.get(case_id)
        if before.error or item_dump is None:
            # Nothing to re-score: an errored case has no ReviewItem, and a
            # result stored without one keeps only what it already recorded.
            rescored.append(before)
            continue
        item = ReviewItem.model_validate(item_dump)
        result = score_item(case, item, constants_of(case))
        for measured in (
            "latency_ms", "phoenix_trace_id", "llm_calls", "tokens_prompt",
            "tokens_completion", "energy_kwh", "gwp_kgco2eq", "impact_estimated",
        ):
            setattr(result, measured, getattr(before, measured))
        rescored.append(result)
    return manifest, previous_list, rescored


def store_rescored(conn: psycopg.Connection, run_id: str, results: list[CaseResult]) -> None:
    """Persist a rescore. The run's eval_version moves to today's scoring rules
    with its results: the row must say which rules produced the scores it holds."""
    loaded = evaldb.load_run(conn, run_id)
    if loaded is None:
        raise LookupError(f"no evaluation run {run_id} in eval.runs")
    for result in results:
        evaldb.upsert_result(conn, loaded[0], result)  # review_item kept (coalesce)
    evaldb.set_eval_version(conn, loaded[0], eval_version())


def _attach_impact(results: list[CaseResult], wf_cfg: WorkflowConfig) -> bool:
    """Fill each case's token/energy columns from its Phoenix trace via EcoLogits.

    Runs after the case loop so the OTLP batch exporter can be flushed first;
    Phoenix bulk-inserts asynchronously, so a case whose spans are not yet
    queryable gets one retry. Impact is a best-effort side metric: a missing
    or down Phoenix DB must never fail the evaluation run. Returns True if any
    result was filled in (so the caller can re-persist them).
    """
    try:
        from opentelemetry import trace as otel_trace

        provider = otel_trace.get_tracer_provider()
        if hasattr(provider, "force_flush"):
            provider.force_flush()
    except Exception:
        pass
    filled = False
    # Cases restored from a previous attempt already carry their impact columns.
    pending = [r for r in results if r.phoenix_trace_id and r.llm_calls is None]
    unestimated: set[str] = set()
    for attempt in range(2):
        if not pending:
            return filled
        if attempt:
            time.sleep(2)  # give Phoenix's async bulk inserter a beat
        still_pending: list[CaseResult] = []
        for result in pending:
            try:
                usage = trace_impact(
                    wf_cfg.phoenix_database_url,
                    result.phoenix_trace_id,
                    electricity_mix_zone=wf_cfg.electricity_mix_zone,
                )
            except Exception:
                return filled  # phoenix DB unreachable: leave the columns NULL
            if usage is None:
                still_pending.append(result)
                continue
            result.llm_calls = usage["llm_calls"]
            result.tokens_prompt = usage["tokens_prompt"]
            result.tokens_completion = usage["tokens_completion"]
            # EcoLogits returns 0.0 for a model missing from its registry, which
            # is indistinguishable from a genuinely measured zero once stored.
            # `not_estimated` names those models: when nothing could be
            # estimated, leave energy/GWP NULL so a report says "unknown"
            # instead of "this run cost 0 gCO2eq".
            estimated = not usage.get("not_estimated")
            result.impact_estimated = estimated
            result.energy_kwh = usage["energy_kwh"] if estimated else None
            result.gwp_kgco2eq = usage["gwp_kgco2eq"] if estimated else None
            filled = True
            unestimated.update(usage.get("not_estimated") or ())
        pending = still_pending
    if unestimated:
        print(
            "  impact: no EcoLogits registry entry for "
            + ", ".join(sorted(unestimated))
            + " — energy/GWP left unset for this run"
        )
    return filled
