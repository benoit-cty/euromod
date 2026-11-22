"""KPI summaries of scored results: the console's per-language table.

The same KPIs are aggregated in SQL by the views of db/eval_schema.sql
(eval.scored_results, eval.run_summary) for the UI and `report`. The two are
kept in step by a test against the live view: `RATE_COLUMNS` and
`COUNT_COLUMNS` name the run_summary column each Python figure is, and
`SQL_ONLY_COLUMNS` the view columns Python deliberately does not print.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable

from .schema import CaseResult

#: KPIs reported per language, in the order the console prints them.
KPIS = [
    "routing_correct",
    "value_correct",
    "date_correct",
    "citation_correct",
    "extract_verbatim",
    "supportedness",
    "critique_pass",
    "hallucination",
    "retrieval_hit",
]

#: Python KPI rate -> its eval.run_summary column (a percentage over the
#: cases that exercise it — NULL KPIs are skipped on both sides).
RATE_COLUMNS = {
    "routing_correct": "routing_pct",
    "value_correct": "value_pct",
    "date_correct": "date_pct",
    "citation_correct": "citation_pct",
    "extract_verbatim": "extract_verbatim_pct",
    "supportedness": "supportedness_pct",
    "critique_pass": "critique_pass_pct",
    "hallucination": "hallucination_pct",
    "retrieval_hit": "retrieval_recall_pct",
}

#: Python per-language count -> its eval.run_summary column.
COUNT_COLUMNS = {
    "cases": "cases",
    "errors": "errors",
    "abstained": "abstentions",
    "rejected": "rejections",
    "no_corpus": "cases_no_corpus",
    "undocumented": "cases_undocumented",
    "fts_only": "fts_only_cases",
    "euromod_off_law": "euromod_discrepancies",
}

#: eval.run_summary columns with no Python twin: the run's identity, the
#: ready-only rates (Python prints a whole `<lang> (ready)` row instead), the
#: guidance share (ADR 0001 evidence, not a KPI), latency and impact.
SQL_ONLY_COLUMNS = frozenset(
    {
        "run_pk",
        "run_id",
        "created_at",
        "as_of",
        "model_provider",
        "model_name",
        "prompt_version",
        "agent_version",
        "dataset_version",
        "critique_model",
        "resolved_model",
        "resolved_critique_model",
        "language",
        "country",
        "routing_pct_ready",
        "value_pct_ready",
        "citation_pct_ready",
        "guidance_only_cases",
        "guidance_only_pct",
        "avg_latency_ms",
        "tokens_prompt",
        "tokens_completion",
        "energy_kwh",
        "gwp_kgco2eq",
    }
)


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
            # Cases retrieved without the vector leg (encoder down or paused).
            "fts_only": str(sum(1 for r in rows if r.vector_leg is False)),
            # Findings: EUROMOD one unit of its precision off the figure the
            # law states (scoring.law_vs_euromod). value_correct stays False.
            "euromod_off_law": str(sum(1 for r in rows if r.euromod_discrepancy)),
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
