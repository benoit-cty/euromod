"""Run the agentic workflow over the golden set and score each case.

Reuses nomoscope_workflow end-to-end (same retrieval, prompts, critique, Phoenix
tracing), but writes queue items to a per-run scratch directory so evaluation
runs never pollute the human review queue.

A run is crash-safe: the manifest and the frozen case list are written before
the first case, and every scored case is appended to ``results.jsonl`` as soon
as it lands. An interrupted run is therefore resumable — see `resume_run`,
which replays the same manifest and case list and skips what is already scored.
"""

from __future__ import annotations

import json
import re
import subprocess
import time
import uuid
from collections import defaultdict
from collections.abc import Callable
from datetime import date, datetime, timezone
from pathlib import Path

from nomoscope_workflow import AGENT_VERSION
from nomoscope_workflow.config import WorkflowConfig, load_config as load_workflow_config
from nomoscope_workflow.impact import trace_impact
from nomoscope_workflow.pipeline import run_parameter
from nomoscope_workflow.prompts import PROMPT_VERSION
from nomoscope_workflow.tracing import setup_tracing

from . import EVAL_VERSION
from .config import REPO_ROOT, EvalConfig
from .dataset import dataset_version
from .schema import CaseResult, GoldenCase, RunManifest
from .scoring import score_item

MANIFEST_FILENAME = "manifest.json"
CASES_FILENAME = "cases.json"
PARTIAL_FILENAME = "results.jsonl"  # append-only, one CaseResult per line
RESULTS_FILENAME = "results.json"


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


def _value_in_force(rows: list[dict], as_of: date):
    """The value of the latest row in force at as_of; falls back to the raw
    EUROMOD string in lineage.model_answer when the row has no normalised
    scalar (FYA/formula rows materialize as value: null)."""
    best: tuple[date, object] | None = None
    for row in rows:
        valid_from = date.fromisoformat(row["valid_from"])
        valid_to = row.get("valid_to")
        if valid_from <= as_of and (valid_to is None or date.fromisoformat(valid_to) >= as_of):
            value = row.get("value")
            if value is None:
                value = (row.get("lineage") or {}).get("model_answer")
            if best is None or valid_from >= best[0]:
                best = (valid_from, value)
    return best[1] if best else None


def _scoring_constants(cases: list[GoldenCase], as_of: date) -> dict[str, dict[str, object]]:
    """Per-country $-constant resolution map for scoring.values_equal: every
    parameter file in the directories the cases point at, keyed by casefolded
    constant name, valued by its value in force at as_of (a number, or the raw
    EUROMOD string that normalise_value resolves recursively)."""
    by_country: dict[str, dict[str, object]] = {}
    for directory in sorted({(REPO_ROOT / c.parameter_file).parent for c in cases}):
        for path in sorted(directory.glob("*.json")):
            try:
                record = json.loads(path.read_text(encoding="utf-8"))
                info = record["information"]
                name = info["model_target"].rsplit("/", 1)[-1].lstrip("$").casefold()
                country = info["country"]
                value = _value_in_force(record.get("values", []), as_of)
            except (OSError, ValueError, KeyError, TypeError):
                continue
            if value is not None:
                by_country.setdefault(country, {})[name] = value
    return by_country


# --------------------------------------------------------------------------- #
# Run directories: manifest + frozen case list + append-only partial results
# --------------------------------------------------------------------------- #


def run_directory(cfg: EvalConfig, run_id: str) -> Path:
    return cfg.runs_dir / run_id


def load_manifest(run_dir: Path) -> RunManifest:
    return RunManifest.model_validate_json(
        (run_dir / MANIFEST_FILENAME).read_text(encoding="utf-8")
    )


def load_run_cases(run_dir: Path) -> list[GoldenCase]:
    """The case list frozen at run start — resuming must replay exactly it, not
    whatever the dataset filters would select today."""
    payload = json.loads((run_dir / CASES_FILENAME).read_text(encoding="utf-8"))
    return [GoldenCase.model_validate(entry) for entry in payload]


def load_partial_results(run_dir: Path) -> list[CaseResult]:
    """Every case scored so far. A torn last line (killed mid-write) is dropped."""
    path = run_dir / PARTIAL_FILENAME
    if not path.exists():
        return []
    results: list[CaseResult] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            results.append(CaseResult.model_validate_json(line))
        except ValueError:
            continue
    return results


def _append_result(run_dir: Path, result: CaseResult) -> None:
    with (run_dir / PARTIAL_FILENAME).open("a", encoding="utf-8") as handle:
        handle.write(result.model_dump_json() + "\n")
        handle.flush()


def rewrite_partial(run_dir: Path, results: list[CaseResult]) -> None:
    """Re-materialize results.jsonl (used after impact columns are backfilled)."""
    (run_dir / PARTIAL_FILENAME).write_text(
        "".join(r.model_dump_json() + "\n" for r in results), encoding="utf-8"
    )


def list_runs(cfg: EvalConfig) -> list[dict]:
    """Every run on disk, newest first: manifest plus done/total progress."""
    runs: list[dict] = []
    if not cfg.runs_dir.exists():
        return runs
    for run_dir in sorted(cfg.runs_dir.iterdir(), reverse=True):
        if not (run_dir / MANIFEST_FILENAME).exists():
            continue
        try:
            manifest = load_manifest(run_dir)
            cases = load_run_cases(run_dir) if (run_dir / CASES_FILENAME).exists() else []
        except (OSError, ValueError):
            continue
        done = len(load_partial_results(run_dir))
        runs.append(
            {
                "run_id": manifest.run_id,
                "manifest": manifest,
                "run_dir": run_dir,
                "done": done,
                "total": len(cases),
                # Runs written before results.jsonl existed have no case list;
                # a finished results.json still marks them complete.
                "complete": bool(cases) and done >= len(cases),
                "stored": (run_dir / RESULTS_FILENAME).exists(),
            }
        )
    return runs


def latest_incomplete_run(cfg: EvalConfig) -> dict | None:
    for run in list_runs(cfg):
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
    cfg: EvalConfig,
    cases: list[GoldenCase],
    as_of: date,
    model: str,
    notes: str | None = None,
) -> RunManifest:
    """Allocate a run id, create its directory and freeze manifest + case list."""
    provider, _, model_name = model.partition("/")
    run_id = f"eval-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-{_slug(model_name or provider)}-{uuid.uuid4().hex[:6]}"
    manifest = RunManifest(
        run_id=run_id,
        created_at=datetime.now(timezone.utc),
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
        dataset_version=dataset_version(cfg.dataset_dir),
        git_commit=_git_commit(),
        countries=sorted({c.country for c in cases}),
        notes=notes,
    )
    run_dir = run_directory(cfg, run_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / MANIFEST_FILENAME).write_text(
        manifest.model_dump_json(indent=2), encoding="utf-8"
    )
    (run_dir / CASES_FILENAME).write_text(
        json.dumps([c.model_dump(mode="json") for c in cases], indent=2), encoding="utf-8"
    )
    return manifest


def resume_run(cfg: EvalConfig, run_id: str) -> tuple[RunManifest, list[GoldenCase], list[CaseResult]]:
    """Reload an interrupted run: its manifest, its frozen case list, and what
    it already scored. Raises FileNotFoundError if the run cannot be resumed."""
    run_dir = run_directory(cfg, run_id)
    if not (run_dir / MANIFEST_FILENAME).exists():
        raise FileNotFoundError(f"no evaluation run at {run_dir}")
    if not (run_dir / CASES_FILENAME).exists():
        raise FileNotFoundError(
            f"run {run_id} predates resumable runs (no {CASES_FILENAME}) — start a new run"
        )
    return load_manifest(run_dir), load_run_cases(run_dir), load_partial_results(run_dir)


def _workflow_config(cfg: EvalConfig, manifest: RunManifest) -> WorkflowConfig:
    wf_cfg = load_workflow_config()
    wf_cfg.model = manifest.model
    # Older manifests (before the judge could be pinned) have no critique_model;
    # they graded themselves, so replaying them must keep doing that.
    wf_cfg.critique_model = manifest.critique_model or manifest.model
    wf_cfg.phoenix_project = cfg.phoenix_project
    wf_cfg.data_dir = run_directory(cfg, manifest.run_id)  # scratch queue, not the review queue
    wf_cfg.data_dir.mkdir(parents=True, exist_ok=True)
    return wf_cfg


def execute_run(
    cfg: EvalConfig,
    manifest: RunManifest,
    cases: list[GoldenCase],
    done_results: list[CaseResult] | None = None,
    on_case_start: Callable[[int, int, GoldenCase], None] | None = None,
    on_case_done: Callable[[int, int, GoldenCase, CaseResult], None] | None = None,
) -> list[CaseResult]:
    """Score every case not already in `done_results`, persisting as it goes.

    Results are appended to the run's results.jsonl the moment each case is
    scored, so a Ctrl-C (or a crash) loses at most the case in flight.
    """
    results = list(done_results or [])
    scored = {r.case_id for r in results}
    pending = [c for c in cases if c.id not in scored]

    wf_cfg = _workflow_config(cfg, manifest)
    tracer = setup_tracing(wf_cfg)
    run_dir = run_directory(cfg, manifest.run_id)
    constants = _scoring_constants(cases, manifest.as_of)
    total = len(cases)

    for case in pending:
        index = len(results) + 1
        if on_case_start:
            on_case_start(index, total, case)
        started = time.perf_counter()
        try:
            item = run_parameter(
                wf_cfg, tracer, REPO_ROOT / case.parameter_file, manifest.as_of, force=True
            )
            result = score_item(case, item, constants.get(case.country))
        except Exception as exc:  # score the failure, keep the run going
            result = CaseResult(
                case_id=case.id,
                country=case.country,
                language=case.language,
                difficulty=case.difficulty,
                source_class=case.source_class,
                routing_expected=case.expected.routing.value,
                corpus_available=case.corpus_available,
                error=f"{exc.__class__.__name__}: {exc}",
            )
        result.latency_ms = int((time.perf_counter() - started) * 1000)
        results.append(result)
        _append_result(run_dir, result)
        if on_case_done:
            on_case_done(index, total, case, result)

    if not manifest.model.startswith("mock") and pending:
        if _attach_impact(results, wf_cfg):
            rewrite_partial(run_dir, results)
    return results


def run_evaluation(
    cfg: EvalConfig,
    cases: list[GoldenCase],
    as_of: date,
    model: str,
    notes: str | None = None,
    on_case_start: Callable[[int, int, GoldenCase], None] | None = None,
    on_case_done: Callable[[int, int, GoldenCase, CaseResult], None] | None = None,
) -> tuple[RunManifest, list[CaseResult]]:
    """Fresh run: freeze the manifest + case list, then score every case."""
    manifest = start_run(cfg, cases, as_of, model, notes=notes)
    results = execute_run(
        cfg, manifest, cases, on_case_start=on_case_start, on_case_done=on_case_done
    )
    return manifest, results


def rescore_run(cfg: EvalConfig, run_id: str) -> tuple[RunManifest, list[CaseResult]]:
    """Re-score a finished run from the ReviewItems it stored — no LLM, no DB.

    A run directory keeps every queue item the pipeline produced, so a fix to
    `scoring.py` can be re-applied to past runs instead of re-spending a full
    run's tokens. Only the scoring moves: routing, values, citations and
    retrieval traces stay exactly what the model produced at the time.

    Expectations come from the run's frozen `cases.json`, never from today's
    golden set — so a rescore isolates the effect of a scoring change from any
    golden-set edit. To measure a golden-set change instead, start a new run.
    Latency and impact columns are carried over from the previous results: they
    are measurements, not scores, and cannot be recomputed offline.
    """
    from nomoscope_workflow.schema import ReviewItem

    run_dir = run_directory(cfg, run_id)
    manifest = load_manifest(run_dir)
    cases = {case.id: case for case in load_run_cases(run_dir)}
    previous = {r.case_id: r for r in load_partial_results(run_dir)}
    constants = _scoring_constants(list(cases.values()), manifest.as_of)

    rescored: list[CaseResult] = []
    for case_id, case in cases.items():
        before = previous.get(case_id)
        if before is None:
            continue
        item_path = run_dir / "queue" / f"{before.item_id}.json" if before.item_id else None
        if before.error or item_path is None or not item_path.exists():
            # Nothing to re-score: an errored case has no ReviewItem, and a run
            # whose queue was cleaned keeps only what it already recorded.
            rescored.append(before)
            continue
        item = ReviewItem.model_validate_json(item_path.read_text(encoding="utf-8"))
        result = score_item(case, item, constants.get(case.country))
        for measured in (
            "latency_ms", "phoenix_trace_id", "llm_calls", "tokens_prompt",
            "tokens_completion", "energy_kwh", "gwp_kgco2eq", "impact_estimated",
        ):
            setattr(result, measured, getattr(before, measured))
        rescored.append(result)
    return manifest, rescored


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
