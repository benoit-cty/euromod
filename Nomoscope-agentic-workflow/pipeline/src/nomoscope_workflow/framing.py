"""Framing: the retrieval query and the citations a parameter is searched with.

Query cleaning (EUROMOD noise out, the law's own names kept) and `frame_query`
(split out of pipeline.py, code audit 4).
"""

from __future__ import annotations

import re
from datetime import date

from . import paramdb, retrieval, translate
from .config import WorkflowConfig
from .schema import ParameterRecord

#: What the enrichment wrote for EUROMOD readers, not for the law: CR table
#: references and EUROMOD names in parentheses, quoted EUROMOD function titles,
#: `policy_cc` / `$param` identifiers. In an OR-of-terms FTS leg every such
#: token pulls unrelated chunks; measured offline over the 39 ready FR golden
#: cases with a citation, stripping them raised golden-citation recall at k=15
#: from 31 to 34 (the three barème thresholds: CGI art. 197 rose from rank 22).
#: Numbers stay: the export's value is usually still the law's, and "11,88"
#: is what finds the SMIC arrêté — dropping them lost that case.
_QUERY_NOISE = (
    re.compile(r"\([^()]*\)"),
    re.compile(r"«[^»]*»"),
    re.compile(r"\$?\b\w*_\w*\b"),
    # EUROMOD modelling vocabulary and Country Report pointers: the enrichment
    # says where a constant is USED ("the 'formula' parameter of the ArithOp
    # function", "Table 2.79 confirms", "the taxes theme doc's credit list",
    # "per direct inspection of the ES policy spine"), none of which a statute
    # contains. Measured over the 9 retrieval misses of the 2026-09-08 review.
    re.compile(
        r"\b(?:SchedCalc|BenCalc|ArithOp|DefConst|DefVar|Elig|Loop|Uprate|SetDefault|"
        r"ILDef|ILArithOp|DefIL|Allocate|UnitCalc|Store|Totals|EUROMOD|OpenFisca)\b"
    ),
    re.compile(r"\b(?:Country Report|CR)(?:['’]s)?\b(?:\s+Table\s+[\d.]+)?", re.IGNORECASE),
    re.compile(r"\bTable\s+\d+(?:\.\d+)*\b"),
    re.compile(r"\b(?:policy|theme)\s+(?:spine|doc(?:ument)?)\b", re.IGNORECASE),
)


#: An English EUROMOD comment quoted inside a translated text: «Calculate end
#: of year bonus», «Fix amount».
_ENGLISH_SPAN = re.compile(
    r"\b(?:the|of|and|for|per|with|amount|calculate|fix(?:ed)?|year|bonus|benefit|rate|see)\b", re.IGNORECASE
)
_QUOTED_SPAN = re.compile(r"«([^»]*)»")
_PAREN_SPAN = re.compile(r"\(([^()]*)\)")


def _keep_span(match: re.Match[str]) -> str:
    """A quoted or parenthesised span of a law-language text, unless it is noise.

    In the French translations the quotes and parentheses hold the benefit's
    own name: «prime de fin d'année», «(Prime de fin d'année, également
    appelée prime exceptionnelle de Noël)», «(Revenu de Solidarité Active)».
    Dropped whole, the $bunmt_bonus1 query read «le montant forfaitaire de
    base annuel de la pour un bénéficiaire seul», and décret n° 2025-1212
    ranked 80th. An English EUROMOD comment, or a span left with no word
    («(Table 2.52)»), is still dropped.
    """
    inner = match.group(1)
    if _ENGLISH_SPAN.search(inner) and not re.search(r"[À-ÿ]", inner):
        return " "
    return f" {inner} "


def _clean_query_text(text: str, lang: str = "en") -> str:
    """Strip EUROMOD-side noise from a label/description before it becomes a query.

    In a law-language text other than English, quoted and parenthesised spans
    keep their content (see `_keep_span`); an English record drops them.
    """
    if lang != "en":
        text = _QUOTED_SPAN.sub(_keep_span, text)
        text = _PAREN_SPAN.sub(_keep_span, text)
    for pattern in _QUERY_NOISE:
        text = pattern.sub(" ", text)
    return re.sub(r"\s+", " ", text).strip(" ,;:.-")


def frame_query(cfg: WorkflowConfig, record: ParameterRecord, as_of: date) -> dict:
    """The `frame` step's deterministic output: the search query and known citations.

    Module-level so the retrieval evaluation (nomokrisis_eval, embedding cases
    built from golden cases) searches with exactly the query a run would send.
    """
    info = record.information
    labels = {**(info.short_label or {}), **(info.label or {})}
    descriptions = info.description or {}
    # Prefer law-language text for the query: the FTS leg of hybrid retrieval
    # is language-specific, so an English-only record searches French law
    # poorly. Translations live in params.parameter_texts (best-effort:
    # no rows / no schema -> received text only, previous behaviour).
    lang = retrieval.LANG_BY_COUNTRY.get(info.country, "en")
    native: list[str] = []
    if lang in descriptions:
        # An assembled schedule carries its members' law-language texts
        # (paramdb._group_texts): search with those alone.
        native = [t for t in (labels.get(lang), descriptions[lang]) if t]
    elif lang not in labels:
        try:
            with paramdb.connect(cfg) as conn:
                texts = translate.law_language_texts(conn, info.model_target, lang)
            native = [t for f in ("short_label", "label", "description") if (t := texts.get(f))]
        except Exception:
            native = []
    # Native texts REPLACE the received ones in the query rather than being
    # appended: a mixed-language ~60-term query dilutes the BGE-M3 embedding
    # and turns the OR'd FTS leg into noise.
    parts = (
        [_clean_query_text(p, lang) for p in native]
        if native
        else [_clean_query_text(p) for p in [*labels.values(), *descriptions.values()]]
    )
    query = " ".join(dict.fromkeys(p for p in parts if p)) or info.model_target
    # Country Report enrichment (acronym -> semantic): CR section headings
    # translate EUROMOD codes into official native benefit/tax names
    # ('tinto01_s' -> 'Contribution différentielle sur les hauts revenus').
    # Context only — CR chunks are excluded from evidence retrieval.
    # Probe with the identity tokens ALONE: label words match every fiscal
    # section and drown the one heading that carries this parameter's code.
    ident = retrieval.euromod_ident_tokens(info.model_target)
    cr_terms: list[str] = []
    cr_headings: list[str] = []
    try:
        if ident:
            with retrieval.connect(cfg) as conn:
                cr_hits = retrieval.country_report_search(conn, info.country, as_of, " ".join(ident), k=5)
            cr_terms = retrieval.cr_enrichment_terms(cr_hits, ident, query)
            cr_headings = [h.citation for h in cr_hits if h.citation]
    except Exception:  # no CR corpus / DB hiccup -> frame works as before
        cr_terms = []
    if cr_terms:
        query = " ".join([query, *cr_terms])
    citations: list[str] = []
    for value in reversed(record.values):
        for ref in value.references:
            citations.extend(filter(None, [ref.title, ref.legal_unit_ref]))
        if citations:
            break
    return {
        "query": query,
        "citations": list(dict.fromkeys(citations)),
        "law_language_texts": len(native),
        "cr_terms": cr_terms,
        "cr_headings": cr_headings,
    }
