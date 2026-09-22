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
import subprocess
import time
import uuid
from collections import defaultdict
from collections.abc import Callable
from datetime import date, datetime, timezone

import psycopg

from nomoscope_workflow import AGENT_VERSION, paramdb
from nomoscope_workflow.config import WorkflowConfig, load_config as load_workflow_config
from nomoscope_workflow.impact import trace_impact
from nomoscope_workflow.pipeline import run_parameter
from nomoscope_workflow.prompts import PROMPT_VERSION
from nomoscope_workflow.schema import ParameterRecord, ReviewItem
from nomoscope_workflow.tracing import setup_tracing

from . import EVAL_VERSION
from . import db as evaldb
from .config import REPO_ROOT, EvalConfig
from .golden_store import golden_set_hash
from .openfisca_golden import db_constants
from .schema import CaseResult, GoldenCase, RunManifest
from .scoring import score_item

GROUP_PREFIX = "group:"


def _git_commit() -> str | None:
    try:
        return subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=REPO_ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
    except Exception:
        return None


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def load_case_record(conn: psycopg.Connection, parameter_target: str) -> ParameterRecord:
    """The parameter under test, from the params DB: `group:<group_id>` is a
    bracket schedule assembled from params.parameter_groups, anything else a
    model_target (or parameter_key) in params.parameters."""
    if parameter_target.startswith(GROUP_PREFIX):
        return paramdb.load_group_record(conn, parameter_target[len(GROUP_PREFIX):])
    return paramdb.load_record(conn, parameter_target)


def _scoring_constants(
    conn: psycopg.Connection, cases: list[GoldenCase], as_of: date
) -> dict[str, dict[str, object]]:
    """Per-country $-constant resolution map for scoring.values_equal, read
    from the params DB (`openfisca_golden.db_constants`) for every country the
    cases cover."""
    return {
        country: db_constants(conn, country, as_of)
        for country in sorted({c.country.upper() for c in cases})
    }


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
        eval_version=EVAL_VERSION,
        dataset_version=golden_set_hash(cases),
        git_commit=_git_commit(),
        countries=sorted({c.country for c in cases}),
        notes=notes,
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
) -> list[CaseResult]:
    """Score every case not already in `done_results`, persisting as it goes.

    Each result is upserted into eval.results (with the ReviewItem) the moment
    the case is scored, so a Ctrl-C (or a crash) loses at most the case in
    flight; the run is flipped to `complete` at the end. `run_case` exists for
    tests — it replaces the workflow call and nothing else.
    """
    loaded = evaldb.load_run(conn, manifest.run_id)
    if loaded is None:
        raise LookupError(f"run {manifest.run_id} is not in eval.runs — start_run first")
    run_pk = loaded[0]
    evaldb.set_run_status(conn, run_pk, "running")

    results = list(done_results or [])
    scored = {r.case_id for r in results}
    pending = [c for c in cases if c.id not in scored]

    wf_cfg = _workflow_config(cfg, manifest)
    tracer = setup_tracing(wf_cfg)
    constants = _scoring_constants(conn, cases, manifest.as_of)
    total = len(cases)

    for case in pending:
        index = len(results) + 1
        if on_case_start:
            on_case_start(index, total, case)
        started = time.perf_counter()
        item: ReviewItem | None = None
        try:
            record = load_case_record(conn, case.parameter_target)
            if run_case is not None:
                item = run_case(wf_cfg, tracer, record, case, manifest.as_of)
            else:
                item = run_parameter(
                    wf_cfg, tracer, record, manifest.as_of,
                    force=True, parameter_ref=case.parameter_target, enqueue=False,
                )
            result = score_item(case, item, constants.get(case.country.upper()))
        except Exception as exc:  # score the failure, keep the run going
            conn.rollback()
            result = _error_result(case, exc)
        result.latency_ms = int((time.perf_counter() - started) * 1000)
        results.append(result)
        evaldb.upsert_result(
            conn, run_pk, result, item.model_dump(mode="json") if item is not None else None
        )
        if on_case_done:
            on_case_done(index, total, case, result)

    if not manifest.model.startswith("mock") and pending:
        if _attach_impact(results, wf_cfg):
            for result in results:
                if result.llm_calls is not None:
                    evaldb.upsert_result(conn, run_pk, result)
    evaldb.set_run_status(conn, run_pk, "complete")
    manifest.status = "complete"
    return results


def run_evaluation(
    conn: psycopg.Connection,
    cfg: EvalConfig,
    cases: list[GoldenCase],
    as_of: date,
    model: str,
    notes: str | None = None,
    on_case_start: Callable[[int, int, GoldenCase], None] | None = None,
    on_case_done: Callable[[int, int, GoldenCase, CaseResult], None] | None = None,
) -> tuple[RunManifest, list[CaseResult]]:
    """Fresh run: freeze the manifest + case list, then score every case."""
    manifest = start_run(conn, cfg, cases, as_of, model, notes=notes)
    results = execute_run(
        conn, cfg, manifest, cases, on_case_start=on_case_start, on_case_done=on_case_done
    )
    return manifest, results


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
    constants = _scoring_constants(conn, list(cases.values()), manifest.as_of)

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
        result = score_item(case, item, constants.get(case.country.upper()))
        for measured in (
            "latency_ms", "phoenix_trace_id", "llm_calls", "tokens_prompt",
            "tokens_completion", "energy_kwh", "gwp_kgco2eq", "impact_estimated",
        ):
            setattr(result, measured, getattr(before, measured))
        rescored.append(result)
    return manifest, previous_list, rescored


def store_rescored(conn: psycopg.Connection, run_id: str, results: list[CaseResult]) -> None:
    loaded = evaldb.load_run(conn, run_id)
    if loaded is None:
        raise LookupError(f"no evaluation run {run_id} in eval.runs")
    for result in results:
        evaldb.upsert_result(conn, loaded[0], result)  # review_item kept (coalesce)


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


#: KPIs reported per language, in the order the console prints them.
KPIS = [
    "routing_correct", "value_correct", "date_correct", "citation_correct",
    "extract_verbatim", "supportedness", "critique_pass", "hallucination",
    "retrieval_hit",
]


def _rate(rows: list[CaseResult], kpi: str) -> str:
    values = [getattr(r, kpi) for r in rows if getattr(r, kpi) is not None]
    return f"{100 * sum(values) / len(values):.0f}%" if values else "-"


def readiness_of(result: CaseResult) -> str:
    """`readiness` for results written before the field existed: those carry
    corpus_available but nothing that distinguishes `undocumented`, so they fall
    back to the coarser corpus split rather than silently claiming to be ready."""
    if result.readiness:
        return result.readiness
    return "no_corpus" if result.corpus_available is False else "ready"


def summarize(results: list[CaseResult]) -> dict[str, dict[str, str]]:
    """Console summary: KPI rates per language, then the two breakdowns that say
    *why* a rate is what it is.

    Three kinds of row, in order:

    ``<lang>``            every case, including the ones no model could answer.
    ``<lang> (ready)``    only cases whose ground truth is complete enough to
                          measure the model: the source act is in the corpus AND
                          a ground-truth citation was recorded. Readiness is a
                          property of the golden set, so mixing unready cases
                          into the headline reports dataset gaps as if they were
                          LLM accuracy — on the first mistral run that was the
                          difference between 54% and 73% routing.
    ``difficulty: <rung>`` / ``hazard: <flag>``
                          the ready cases only, split by how much work the
                          parameter takes and by which known failure mode it
                          exercises. Unready cases are excluded on purpose: they
                          fail for a reason that has nothing to do with the rung.
    """
    by_lang: dict[str, list[CaseResult]] = defaultdict(list)
    for r in results:
        by_lang[r.language].append(r)

    table: dict[str, dict[str, str]] = {}
    for lang, rows in sorted(by_lang.items()):
        ready = [r for r in rows if readiness_of(r) == "ready"]
        entry = {
            "cases": str(len(rows)),
            "errors": str(sum(1 for r in rows if r.error)),
            # Refusals, and the two readiness gaps, so the reader can see how
            # much of a low score is "the model was wrong" versus "there was
            # nothing to read" versus "we never said what the answer was".
            "abstained": str(sum(1 for r in rows if r.abstained)),
            "rejected": str(sum(1 for r in rows if r.rejected)),
            "no_corpus": str(sum(1 for r in rows if readiness_of(r) == "no_corpus")),
            "undocumented": str(sum(1 for r in rows if readiness_of(r) == "undocumented")),
        }
        for kpi in KPIS:
            entry[kpi] = _rate(rows, kpi)
        table[lang] = entry
        if len(ready) != len(rows):
            table[f"{lang} (ready)"] = {
                "cases": str(len(ready)),
                **{kpi: _rate(ready, kpi) for kpi in KPIS},
            }

    ready_all = [r for r in results if readiness_of(r) == "ready"]
    _breakdown(table, "difficulty", ready_all, lambda r: [r.difficulty or "unlabelled"])
    _breakdown(table, "hazard", ready_all, lambda r: list(r.hazards))
    return table


def _breakdown(
    table: dict[str, dict[str, str]],
    label: str,
    rows: list[CaseResult],
    keys_of: Callable[[CaseResult], list[str]],
) -> None:
    """Add one `label: <bucket>` row per bucket, aggregated across languages.

    `keys_of` returns a list because hazards are multi-valued: a case that is
    both income_year and cross_instrument counts in both rows, so the buckets
    deliberately do not sum to the case total.
    """
    buckets: dict[str, list[CaseResult]] = defaultdict(list)
    for row in rows:
        for key in keys_of(row):
            buckets[key].append(row)
    if len(buckets) < 2 and label == "difficulty":
        return  # a single rung says nothing; don't print a row that cannot compare
    for key, bucket in sorted(buckets.items()):
        table[f"{label}: {key}"] = {
            "cases": str(len(bucket)),
            **{kpi: _rate(bucket, kpi) for kpi in KPIS},
        }
