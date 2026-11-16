"""Contributed documents: a reviewer hands over a URL or a file, we ingest it.

A country adapter can only ingest what a national portal keys by a national
id. Much of what actually fixes a EUROMOD value is not there at all: a Unedic
circular, a BOFiP doctrine page, a ministerial arrete a reviewer saved as PDF.
This module is the path for those — one library function behind the CLI (which
the validation UI reaches through a worker `ingest` job, ADR 0004) and the
scout's guidance ingests, so a workflow can contribute a document with no UI
in sight.

The rules that matter (ADR 0001, and the spec's Implementation Decisions):

* **Archive first.** The raw bytes are written to a fetch snapshot with their
  content type, origin and sha256 before anything is parsed.
* **Identity is the document, not the run.** A URL keys the instrument on its
  canonical form (fragment dropped), so the same BOFiP page linked with two
  anchors is one instrument; an uploaded file keys on ``file:<sha256>``.
* **Trust follows the kind, mechanically.** The reviewer names the kind in
  their own country's words; the source-trust class is derived, and "other"
  is never granted evidence-level trust.
* **No invented dates.** A missing validity start is refused, not guessed.
"""

from __future__ import annotations

from nomotheca_ingest.core.errors import RefusalError
from nomotheca_ingest.core.ir import NormLevel
from nomotheca_ingest.core.contributed.fetch import (
    BROWSER_USER_AGENT,
    SourceDocument,
    canonical_url,
    content_hash,
    fetch_in_browser,
    national_id_for,
    read_input,
    suggest,
)
from nomotheca_ingest.core.contributed.ingest import (
    ID_SYSTEM,
    IMPLEMENTS_RELATION,
    SKILL_VERSION,
    SOURCE_TYPE,
    DocumentResult,
    ingest_document,
    parse_document,
    reparse_documents,
    route,
    source_ref,
    stored_content_hash,
)
from nomotheca_ingest.core.contributed.kinds import (
    DEFAULT_KINDS,
    TRUST_CLASS_BY_LEVEL,
    ContributedFields,
    kinds_by_jurisdiction,
    kinds_for,
    norm_level_for,
    source_code_for,
    stated_fields,
    trust_class_for,
)

__all__ = [
    "BROWSER_USER_AGENT",
    "ID_SYSTEM",
    "IMPLEMENTS_RELATION",
    "DEFAULT_KINDS",
    "SKILL_VERSION",
    "SOURCE_TYPE",
    "TRUST_CLASS_BY_LEVEL",
    "ContributedFields",
    "DocumentResult",
    "NormLevel",
    "RefusalError",
    "SourceDocument",
    "canonical_url",
    "content_hash",
    "fetch_in_browser",
    "ingest_document",
    "kinds_by_jurisdiction",
    "kinds_for",
    "national_id_for",
    "norm_level_for",
    "parse_document",
    "read_input",
    "reparse_documents",
    "route",
    "source_code_for",
    "source_ref",
    "stated_fields",
    "stored_content_hash",
    "suggest",
    "trust_class_for",
]
