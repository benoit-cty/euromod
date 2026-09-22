"""Nomergon: the worker that owns every model call (ADR 0004).

The workstation never executes anything: it inserts a row into ``ops.jobs``
and polls ``ops.jobs`` / ``ops.job_events``. This package claims those rows,
runs each job as a subprocess of the existing CLIs (or, for ``encode``,
in-process with BGE-M3 kept warm) and streams their output back as rows.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("nomergon-worker")
except PackageNotFoundError:  # pragma: no cover - source checkout without install
    __version__ = "0.0.0"

__all__ = ["__version__"]
