"""Environmental impact of LLM calls, estimated from Phoenix traces via EcoLogits.

Every real LLM call is already traced to Phoenix (OpenInference spans with
llm_token_count_* columns), so impact estimation is a deterministic offline
read over the phoenix DB — no hot-path instrumentation, retroactive over all
runs, and provider-agnostic like the rest of the pipeline. Mock runs carry no
token counts and are naturally excluded.

EcoLogits' methodology keys on *output* tokens (inference energy scales with
generation, not prompt reading); prompt tokens are reported for context only.
Models missing from the EcoLogits registry are listed as not-estimated rather
than silently dropped. Impacts are computed per span, then summed, so any
per-request constants in the methodology are preserved.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime

import psycopg
from psycopg.rows import dict_row


def phoenix_url_from(database_url: str) -> str:
    """Swap the database name of a Postgres URL for `phoenix` (same instance)."""
    base, _, _ = database_url.rpartition("/")
    return f"{base}/phoenix"

# EcoLogits provider keys, from its model registry.
_ECOLOGITS_PROVIDERS = {"openai", "anthropic", "mistralai", "cohere", "google_genai", "huggingface_hub"}

# OpenInference llm.provider values / model-string vendor prefixes -> EcoLogits provider.
_PROVIDER_ALIASES = {
    "azure": "openai",
    "azure_openai": "openai",
    "mistral": "mistralai",
    "google": "google_genai",
    "google_vertex": "google_genai",
    "huggingface": "huggingface_hub",
}

# Model-name prefix fallback when the span has no usable provider attribute.
_MODEL_PREFIXES = [
    ("gpt-", "openai"),
    ("o1", "openai"),
    ("o3", "openai"),
    ("o4", "openai"),
    ("chatgpt", "openai"),
    ("claude", "anthropic"),
    ("mistral", "mistralai"),
    ("magistral", "mistralai"),
    ("ministral", "mistralai"),
    ("codestral", "mistralai"),
    ("gemini", "google_genai"),
    ("gemma", "google_genai"),
    ("command", "cohere"),
]


@dataclass(slots=True)
class ModelImpact:
    """Aggregated impact for one (model, provider) across the selected spans."""

    model: str
    provider: str  # EcoLogits provider key, or the raw attribute when unresolved
    calls: int = 0
    prompt_tokens: int = 0
    output_tokens: int = 0
    latency_s: float = 0.0
    estimated: bool = True  # False: model not in the EcoLogits registry
    energy_kwh_min: float = 0.0
    energy_kwh_max: float = 0.0
    gwp_kgco2eq_min: float = 0.0
    gwp_kgco2eq_max: float = 0.0
    adpe_kgsbeq_min: float = 0.0
    adpe_kgsbeq_max: float = 0.0
    pe_mj_min: float = 0.0
    pe_mj_max: float = 0.0


@dataclass(slots=True)
class ImpactReport:
    electricity_mix_zone: str
    models: list[ModelImpact] = field(default_factory=list)
    total_calls: int = 0
    total_output_tokens: int = 0
    energy_kwh_min: float = 0.0
    energy_kwh_max: float = 0.0
    gwp_kgco2eq_min: float = 0.0
    gwp_kgco2eq_max: float = 0.0
    adpe_kgsbeq_min: float = 0.0
    adpe_kgsbeq_max: float = 0.0
    pe_mj_min: float = 0.0
    pe_mj_max: float = 0.0
    not_estimated: list[str] = field(default_factory=list)  # models missing from the registry

    def as_dict(self) -> dict:
        return asdict(self)


def resolve_provider(provider_attr: str | None, model_name: str) -> tuple[str | None, str]:
    """Map a span's provider attribute / model string to an EcoLogits provider.

    Returns (ecologits_provider or None, bare model name) — openrouter-style
    "vendor/model" strings contribute their vendor prefix.
    """
    name = model_name
    vendor = None
    if "/" in name:  # openrouter/together route through vendor-prefixed ids
        vendor, _, name = name.partition("/")
    for candidate in (provider_attr, vendor):
        if not candidate:
            continue
        candidate = candidate.lower()
        candidate = _PROVIDER_ALIASES.get(candidate, candidate)
        if candidate in _ECOLOGITS_PROVIDERS:
            return candidate, name
    for prefix, prov in _MODEL_PREFIXES:
        if name.lower().startswith(prefix):
            return prov, name
    return None, name


def fetch_llm_spans(
    phoenix_database_url: str,
    project: str | None = None,
    since: datetime | None = None,
    until: datetime | None = None,
    trace_ids: list[str] | None = None,
) -> list[dict]:
    """Read LLM spans (model, tokens, latency) from the phoenix DB.

    Spans without a completion token count (mock runs, non-generation spans)
    are excluded — there is nothing to estimate for them.
    """
    query = """
        SELECT s.attributes#>>'{llm,model_name}'                  AS model,
               s.attributes#>>'{llm,provider}'                    AS provider,
               COALESCE(s.llm_token_count_prompt, 0)              AS prompt_tokens,
               s.llm_token_count_completion                       AS output_tokens,
               EXTRACT(EPOCH FROM s.end_time - s.start_time)::float8 AS latency_s
        FROM spans s
        JOIN traces t ON t.id = s.trace_rowid
        JOIN projects p ON p.id = t.project_rowid
        WHERE s.span_kind = 'LLM'
          AND s.llm_token_count_completion IS NOT NULL
          AND s.attributes#>>'{llm,model_name}' IS NOT NULL
          AND (%(project)s::text IS NULL OR p.name = %(project)s)
          AND (%(since)s::timestamptz IS NULL OR s.start_time >= %(since)s)
          AND (%(until)s::timestamptz IS NULL OR s.start_time < %(until)s)
          AND (%(trace_ids)s::text[] IS NULL OR t.trace_id = ANY(%(trace_ids)s))
        ORDER BY s.start_time
    """
    params = {"project": project, "since": since, "until": until, "trace_ids": trace_ids}
    with psycopg.connect(phoenix_database_url, row_factory=dict_row) as conn:
        return conn.execute(query, params).fetchall()


def _value_range(metric) -> tuple[float, float]:
    """An EcoLogits metric value is a float or a RangeValue(min, max)."""
    value = metric.value
    if hasattr(value, "min"):
        return float(value.min), float(value.max)
    return float(value), float(value)


def compute_impact_report(
    spans: list[dict], electricity_mix_zone: str = "EEE"
) -> ImpactReport:
    """Sum EcoLogits impact estimates over LLM spans, grouped by model."""
    from ecologits.tracers.utils import llm_impacts  # deferred: heavy registry load

    report = ImpactReport(electricity_mix_zone=electricity_mix_zone)
    by_model: dict[str, ModelImpact] = {}
    for span in spans:
        provider, model = resolve_provider(span["provider"], span["model"])
        agg = by_model.setdefault(
            model, ModelImpact(model=model, provider=provider or (span["provider"] or "?"))
        )
        agg.calls += 1
        agg.prompt_tokens += span["prompt_tokens"]
        agg.output_tokens += span["output_tokens"]
        agg.latency_s += span["latency_s"]
        if provider is None:
            agg.estimated = False
            continue
        impacts = llm_impacts(
            provider=provider,
            model_name=model,
            output_token_count=span["output_tokens"],
            request_latency=span["latency_s"],
            electricity_mix_zone=electricity_mix_zone,
        )
        if impacts.has_errors or impacts.energy is None:
            agg.estimated = False
            continue
        for attr, metric in (
            ("energy_kwh", impacts.energy),
            ("gwp_kgco2eq", impacts.gwp),
            ("adpe_kgsbeq", impacts.adpe),
            ("pe_mj", impacts.pe),
        ):
            lo, hi = _value_range(metric)
            setattr(agg, f"{attr}_min", getattr(agg, f"{attr}_min") + lo)
            setattr(agg, f"{attr}_max", getattr(agg, f"{attr}_max") + hi)

    report.models = sorted(by_model.values(), key=lambda m: m.energy_kwh_max, reverse=True)
    for agg in report.models:
        report.total_calls += agg.calls
        report.total_output_tokens += agg.output_tokens
        if not agg.estimated:
            report.not_estimated.append(agg.model)
            continue
        for attr in ("energy_kwh", "gwp_kgco2eq", "adpe_kgsbeq", "pe_mj"):
            for bound in ("min", "max"):
                key = f"{attr}_{bound}"
                setattr(report, key, getattr(report, key) + getattr(agg, key))
    return report


def build_report(
    phoenix_database_url: str,
    project: str | None = None,
    since: datetime | None = None,
    until: datetime | None = None,
    electricity_mix_zone: str = "EEE",
) -> ImpactReport:
    """Fetch spans and compute the impact report in one call (CLI / eval entry point)."""
    spans = fetch_llm_spans(phoenix_database_url, project=project, since=since, until=until)
    return compute_impact_report(spans, electricity_mix_zone=electricity_mix_zone)


def trace_impact(
    phoenix_database_url: str, trace_id: str, electricity_mix_zone: str = "EEE"
) -> dict | None:
    """Scalar impact summary for a single trace (per-case eval metric).

    Energy/GWP are the midpoint of the EcoLogits min–max range so they can be
    stored and summed as plain columns. Returns None when the trace has no LLM
    spans with token counts (mock runs) or nothing could be estimated.
    """
    spans = fetch_llm_spans(phoenix_database_url, trace_ids=[trace_id])
    if not spans:
        return None
    report = compute_impact_report(spans, electricity_mix_zone=electricity_mix_zone)
    return {
        "llm_calls": report.total_calls,
        "tokens_prompt": sum(m.prompt_tokens for m in report.models),
        "tokens_completion": report.total_output_tokens,
        "energy_kwh": (report.energy_kwh_min + report.energy_kwh_max) / 2,
        "gwp_kgco2eq": (report.gwp_kgco2eq_min + report.gwp_kgco2eq_max) / 2,
        "not_estimated": report.not_estimated,
    }
