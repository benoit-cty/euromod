"""Run the agentic workflow over the golden set and score each case.

Reuses nomoscope_workflow end-to-end (same retrieval, prompts, critique, Phoenix
tracing), but writes queue items to a per-run scratch directory so evaluation
runs never pollute the human review queue.
"""

from __future__ import annotations

import re
import subprocess
import time
import uuid
from collections import defaultdict
from datetime import date, datetime, timezone

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


def run_evaluation(
    cfg: EvalConfig,
    cases: list[GoldenCase],
    as_of: date,
    model: str,
    notes: str | None = None,
) -> tuple[RunManifest, list[CaseResult]]:
    provider, _, model_name = model.partition("/")
    run_id = f"eval-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-{_slug(model_name or provider)}-{uuid.uuid4().hex[:6]}"

    wf_cfg = load_workflow_config()
    wf_cfg.model = model
    wf_cfg.critique_model = model
    wf_cfg.phoenix_project = cfg.phoenix_project
    wf_cfg.data_dir = cfg.runs_dir / run_id  # scratch queue, not the review queue
    wf_cfg.data_dir.mkdir(parents=True, exist_ok=True)
    tracer = setup_tracing(wf_cfg)

    manifest = RunManifest(
        run_id=run_id,
        created_at=datetime.now(timezone.utc),
        as_of=as_of,
        model=model,
        model_provider=provider,
        model_name=model_name or provider,
        prompt_version=PROMPT_VERSION,
        agent_version=AGENT_VERSION,
        eval_version=EVAL_VERSION,
        dataset_version=dataset_version(cfg.dataset_dir),
        git_commit=_git_commit(),
        countries=sorted({c.country for c in cases}),
        notes=notes,
    )

    results: list[CaseResult] = []
    for case in cases:
        started = time.perf_counter()
        try:
            item = run_parameter(
                wf_cfg, tracer, REPO_ROOT / case.parameter_file, as_of, force=True
            )
            result = score_item(case, item)
        except Exception as exc:  # score the failure, keep the run going
            result = CaseResult(
                case_id=case.id,
                country=case.country,
                language=case.language,
                difficulty=case.difficulty,
                source_class=case.source_class,
                routing_expected=case.expected.routing.value,
                error=f"{exc.__class__.__name__}: {exc}",
            )
        result.latency_ms = int((time.perf_counter() - started) * 1000)
        results.append(result)

    if not model.startswith("mock"):
        _attach_impact(results, wf_cfg)
    return manifest, results


def _attach_impact(results: list[CaseResult], wf_cfg: WorkflowConfig) -> None:
    """Fill each case's token/energy columns from its Phoenix trace via EcoLogits.

    Runs after the case loop so the OTLP batch exporter can be flushed first;
    Phoenix bulk-inserts asynchronously, so a case whose spans are not yet
    queryable gets one retry. Impact is a best-effort side metric: a missing
    or down Phoenix DB must never fail the evaluation run.
    """
    try:
        from opentelemetry import trace as otel_trace

        provider = otel_trace.get_tracer_provider()
        if hasattr(provider, "force_flush"):
            provider.force_flush()
    except Exception:
        pass
    pending = [r for r in results if r.phoenix_trace_id]
    for attempt in range(2):
        if not pending:
            return
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
                return  # phoenix DB unreachable: leave the columns NULL
            if usage is None:
                still_pending.append(result)
                continue
            result.llm_calls = usage["llm_calls"]
            result.tokens_prompt = usage["tokens_prompt"]
            result.tokens_completion = usage["tokens_completion"]
            result.energy_kwh = usage["energy_kwh"]
            result.gwp_kgco2eq = usage["gwp_kgco2eq"]
        pending = still_pending


def summarize(results: list[CaseResult]) -> dict[str, dict[str, str]]:
    """Console summary: KPI rates per language (avg over non-None values)."""
    kpis = [
        "routing_correct", "value_correct", "date_correct", "citation_correct",
        "supportedness", "hallucination", "retrieval_hit",
    ]
    by_lang: dict[str, list[CaseResult]] = defaultdict(list)
    for r in results:
        by_lang[r.language].append(r)

    table: dict[str, dict[str, str]] = {}
    for lang, rows in sorted(by_lang.items()):
        entry = {"cases": str(len(rows)), "errors": str(sum(1 for r in rows if r.error))}
        for kpi in kpis:
            values = [getattr(r, kpi) for r in rows if getattr(r, kpi) is not None]
            entry[kpi] = f"{100 * sum(values) / len(values):.0f}%" if values else "-"
        table[lang] = entry
    return table
