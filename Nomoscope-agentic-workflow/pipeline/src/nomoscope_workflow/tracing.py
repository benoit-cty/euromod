"""Arize Phoenix observability via OpenTelemetry (OpenInference semantics).

One trace per (country, parameter, as_of) run, with nested spans
retrieval -> proposal -> critique -> diff. PydanticAI agent runs are
instrumented natively (Agent.instrument_all) and mapped to OpenInference
spans by openinference-instrumentation-pydantic-ai; the pipeline steps below
get manual spans so mock runs trace identically to LLM runs.

Swapping the backend is a config change (OTLP endpoint), not a re-instrumentation.
"""

from __future__ import annotations

import json
from contextlib import contextmanager
from typing import Any, Iterator

from opentelemetry import trace
from opentelemetry.trace import Tracer

from .config import WorkflowConfig

_INITIALISED = False


def setup_tracing(cfg: WorkflowConfig) -> Tracer:
    """Register the Phoenix OTLP exporter once and return a tracer (no-op if disabled)."""
    global _INITIALISED
    if cfg.tracing_enabled and not _INITIALISED:
        try:
            from phoenix.otel import register

            tracer_provider = register(
                project_name=cfg.phoenix_project,
                endpoint=cfg.phoenix_endpoint.rstrip("/") + "/v1/traces",
                auto_instrument=False,
                set_global_tracer_provider=True,
                verbose=False,
            )
            _instrument_pydantic_ai(tracer_provider)
            _INITIALISED = True
        except Exception as exc:  # Phoenix down or package missing: run untraced
            print(f"[tracing] Phoenix disabled ({exc.__class__.__name__}: {exc})")
    return trace.get_tracer("nomoscope_workflow")


def _instrument_pydantic_ai(tracer_provider: Any) -> None:
    """Emit PydanticAI agent/LLM spans in OpenInference form for Phoenix."""
    from openinference.instrumentation.pydantic_ai import OpenInferenceSpanProcessor
    from pydantic_ai import Agent

    # replace_default_processor=False: phoenix's provider otherwise drops its
    # own OTLP export processor, and spans are created but never reach Phoenix.
    tracer_provider.add_span_processor(
        OpenInferenceSpanProcessor(), replace_default_processor=False
    )
    Agent.instrument_all()


@contextmanager
def step_span(
    tracer: Tracer,
    name: str,
    kind: str = "CHAIN",
    input_value: Any = None,
) -> Iterator[Any]:
    """Open an OpenInference-typed span; caller may attach output via span.set_attribute."""
    with tracer.start_as_current_span(name) as span:
        span.set_attribute("openinference.span.kind", kind)
        if input_value is not None:
            span.set_attribute("input.value", _as_json(input_value))
            span.set_attribute("input.mime_type", "application/json")
        yield span


def set_output(span: Any, output_value: Any) -> None:
    """Attach a JSON output payload to a span."""
    span.set_attribute("output.value", _as_json(output_value))
    span.set_attribute("output.mime_type", "application/json")


def _as_json(value: Any) -> str:
    """Serialise pydantic models / plain values to a JSON string for span attributes."""
    if hasattr(value, "model_dump"):
        value = value.model_dump(mode="json")
    return json.dumps(value, ensure_ascii=False, default=str)
