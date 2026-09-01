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
import os
import time
from contextlib import contextmanager
from typing import Any, Iterator

from opentelemetry import trace
from opentelemetry.trace import Tracer

from .config import WorkflowConfig

_INITIALISED = False

# Console progress mirrors the span tree: one line at step start and end, so
# anything streaming stdout (the validation UI console, a terminal) shows what
# the run is doing during long silent stretches (model loads, LLM calls).
# WORKFLOW_PROGRESS=0 silences it, e.g. for eval batch runs.
_PROGRESS = os.environ.get("WORKFLOW_PROGRESS", "1").lower() not in {"0", "false", "off"}


def progress(message: str) -> None:
    if _PROGRESS:
        print(message, flush=True)


def set_progress(enabled: bool) -> None:
    """Toggle the console step mirror at runtime (the env var only reads once at
    import, which is too late for a caller that imports this module first —
    nomokrisis-eval, whose batch runs print one line per case instead)."""
    global _PROGRESS
    _PROGRESS = enabled


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
    progress(f"  › {name}")
    started = time.monotonic()
    with tracer.start_as_current_span(name) as span:
        span.set_attribute("openinference.span.kind", kind)
        if input_value is not None:
            span.set_attribute("input.value", _as_json(input_value))
            span.set_attribute("input.mime_type", "application/json")
        try:
            yield span
        except Exception:
            progress(f"  ✗ {name} failed ({time.monotonic() - started:.1f}s)")
            raise
    progress(f"  ✓ {name} ({time.monotonic() - started:.1f}s)")


def set_output(span: Any, output_value: Any) -> None:
    """Attach a JSON output payload to a span."""
    span.set_attribute("output.value", _as_json(output_value))
    span.set_attribute("output.mime_type", "application/json")


def _as_json(value: Any) -> str:
    """Serialise pydantic models / plain values to a JSON string for span attributes."""
    if hasattr(value, "model_dump"):
        value = value.model_dump(mode="json")
    return json.dumps(value, ensure_ascii=False, default=str)
