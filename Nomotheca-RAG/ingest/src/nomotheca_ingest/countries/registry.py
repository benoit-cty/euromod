"""Country adapter registry used by the pipeline and user interfaces."""

from __future__ import annotations

from nomotheca_ingest.countries.base import CountryAdapter, UrlSource
from nomotheca_ingest.countries.es.adapter import EsAdapter
from nomotheca_ingest.countries.fr.adapter import FrAdapter
from nomotheca_ingest.countries.ie.adapter import IeAdapter
from nomotheca_ingest.countries.lt.adapter import LtAdapter
from nomotheca_ingest.countries.nl.adapter import NlAdapter


_ADAPTERS: dict[str, type[CountryAdapter]] = {
    "ES": EsAdapter,
    "FR": FrAdapter,
    "IE": IeAdapter,
    "LT": LtAdapter,
    "NL": NlAdapter,
}


def url_sources() -> dict[str, UrlSource]:
    """Every registered adapter's official-portal descriptor, by jurisdiction.

    What the contributed-document router reads to recognise a URL. An adapter
    with no `url_source` simply never claims one.
    """
    return {
        code: adapter_type.url_source
        for code, adapter_type in _ADAPTERS.items()
        if getattr(adapter_type, "url_source", None) is not None
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
