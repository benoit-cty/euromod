"""Country adapter registry used by the pipeline and user interfaces."""

from __future__ import annotations

from nomotheca_ingest.countries.base import CountryAdapter
from nomotheca_ingest.countries.fr.adapter import FrAdapter
from nomotheca_ingest.countries.ie.adapter import IeAdapter
from nomotheca_ingest.countries.lt.adapter import LtAdapter


_ADAPTERS: dict[str, type[CountryAdapter]] = {
    "FR": FrAdapter,
    "IE": IeAdapter,
    "LT": LtAdapter,
}


def get_adapter(jurisdiction: str) -> CountryAdapter:
    """Return the adapter implementation for a jurisdiction code."""
    try:
        adapter_type = _ADAPTERS[jurisdiction.upper()]
    except KeyError as exc:
        supported = ", ".join(sorted(_ADAPTERS))
        msg = f"Unsupported jurisdiction {jurisdiction!r}. Supported: {supported}"
        raise ValueError(msg) from exc
    return adapter_type()
