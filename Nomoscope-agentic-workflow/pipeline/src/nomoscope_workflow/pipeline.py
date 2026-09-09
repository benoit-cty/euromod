"""The agentic workflow: an explicit pipeline of steps, deterministic wherever possible.

frame -> retrieve -> propose -> critique -> diff -> enqueue
                 \\ (no hits) ----------------/    (one LLM retry on critique fail)

LLM steps: propose, critique — both PydanticAI structured-output calls (skipped
mechanics stay). Everything else is code: retrieval is SQL, citation
verification is a string match against the corpus, diffing and routing are
pure functions. One Phoenix trace per parameter run.
"""

from __future__ import annotations

import ast
import json
import math
import operator
import re
import uuid
from datetime import date, datetime, timedelta, timezone
from collections.abc import Iterable
from pathlib import Path
from typing import TypedDict

from opentelemetry.trace import Tracer

from . import AGENT_VERSION, llm, mock, paramdb, queue_store, regions, retrieval, scout, translate
from .config import WorkflowConfig
from .prompts import PROMPT_VERSION
from .schema import (
    Bracket,
    CritiqueFindings,
    CritiqueReport,
    ItemStatus,
    Lineage,
    ParameterRecord,
    ParameterValue,
    ProposalDraft,
    Reference,
    RetrievalHit,
    ReviewItem,
    Routing,
    SourceType,
    SourceTrustClass,
    TemporalBasis,
    income_year_for,
)
from .tracing import progress, set_output, step_span

MAX_PROPOSAL_ATTEMPTS = 2

#: Informational critique finding (ADR 0001). "Legislation is King" stays
#: visible in every decision record without blocking circular-governed schemes:
#: it never changes the verdict, the routing, or the reviewer's ability to
#: Accept — it only says what the value rests on.
GUIDANCE_ONLY_ISSUE = "supported by guidance only: no legislation among the cited sources"


def cited_classes(
    draft: ProposalDraft | None, hits: list[RetrievalHit]
) -> list[SourceTrustClass]:
    """Source-trust class of every retrieved chunk the draft actually cites."""
    if draft is None or not draft.citation_chunk_id:
        return []
    return [hit.source_trust_class for hit in hits if hit.chunk_id == draft.citation_chunk_id]


def guidance_only(classes: Iterable[SourceTrustClass | None]) -> bool:
    """True when a proposal cites something and every citation is guidance.

    An empty citation list is not guidance-only: there is nothing to label.
    """
    values = list(classes)
    return bool(values) and all(value == SourceTrustClass.GUIDANCE for value in values)


class WorkflowState(TypedDict, total=False):
    record: ParameterRecord
    parameter_file: str
    as_of: date
    # Date used to select in-force legislation versions; differs from as_of
    # for income_year parameters (see _retrieval_as_of).
    retrieval_as_of: date
    run_id: str
    phoenix_trace_id: str | None
    force: bool
    query: str
    citations: list[str]
    #: Jurisdiction codes retrieval drew on: the country, plus the region's
    #: child jurisdiction for a regional parameter (ADR 0003).
    jurisdictions: list[str]
    hits: list[RetrievalHit]
    draft: ProposalDraft | None
    critique: CritiqueReport | None
    attempts: int
    routing: Routing
    item: ReviewItem
    enqueued: bool
    derived_from: list[str]
    #: Merged view of every gap-fill round, carried on the ReviewItem.
    scout: scout.ScoutResult
    #: One entry per gap-fill round, in order.
    scout_rounds: list[scout.ScoutResult]
    #: Candidate ids already fetched (or already failed) this run, so a later
    #: round never spends its ingest budget on them again.
    scout_attempted: set[str]


def _values_equal(a, b) -> bool:
    """Compare parameter values (scalar/bool/str/brackets) with float tolerance."""
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return False
        return all(_values_equal_bracket(x, y) for x, y in zip(a, b))
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(float(a) - float(b)) < 1e-9
    return a == b


def _values_equal_bracket(a: Bracket, b: Bracket) -> bool:
    def eq(x: float | None, y: float | None) -> bool:
        return (x is None) == (y is None) and (x is None or abs(x - y) < 1e-9)

    return eq(a.threshold, b.threshold) and eq(a.rate, b.rate) and eq(a.amount, b.amount)


_PARAM_REF = re.compile(r"\$[A-Za-z_]\w*")


def _derived_refs(record: ParameterRecord, current: ParameterValue | None) -> list[str]:
    """$references to other parameters in the current value / raw EUROMOD string.

    A value like `$PSS * 4` has no independent legislative existence: the
    anchor parameter is what legislation sets, so asking the corpus about the
    derived one is a guaranteed not_found.
    """
    if current is None:
        return []
    own = record.information.model_target.rsplit("/", 1)[-1]
    sources = [
        current.value if isinstance(current.value, str) else "",
        (current.lineage.model_answer or "") if current.lineage else "",
    ]
    refs = dict.fromkeys(m for s in sources for m in _PARAM_REF.findall(s))
    return [r for r in refs if r != own]


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


def _clean_query_text(text: str) -> str:
    """Strip EUROMOD-side noise from a label/description before it becomes a query."""
    for pattern in _QUERY_NOISE:
        text = pattern.sub(" ", text)
    return re.sub(r"\s+", " ", text).strip(" ,;:.-")


def _retrieval_as_of(record: ParameterRecord, as_of: date) -> date:
    """The date used to select in-force legislation versions.

    income_year parameters (FR income tax family): the enacting finance act is
    published months AFTER the income year it governs, so look for versions
    consolidated mid-way through the year FOLLOWING the income year — for
    system year 2025 (income year 2024) that is 1 July 2025, when LF 2025 is
    consolidated. Open-ended current versions still match, and the critique's
    version-window check catches the act not being in the corpus yet.
    """
    if record.information.temporal_basis == TemporalBasis.INCOME_YEAR:
        return date(income_year_for(as_of.year) + 1, 7, 1)
    return as_of


def _consolidated_in_force(
    provenance: dict | None, retrieval_as_of: date, income_year: int, article_text: str
) -> bool:
    """Is the cited text a consolidated code article in force on the retrieval date?

    France assesses income year Y in Y+1, and the code article as consolidated
    on 1 July Y+1 (`_retrieval_as_of`) is the text that assessment applies —
    CGI art. 197 "en vigueur du 16 février 2025 au 21 février 2026" is the
    barème for 2024 income. That holds however old the version is: art. 223
    sexies has read the same since 2018 because the CEHR thresholds never
    moved, and no finance act for Y restates it. The old rule treated every
    version older than the budget-act window as "probably last year's value"
    and demanded a finance-act clause naming Y, which rejected correct
    unchanged proposals. Two guards keep the presumption honest:

    * an open-ended version only proves "not amended" up to the day we
      fetched it, so the snapshot must postdate the retrieval date;
    * a text whose applicability clause names the NEXT income year (CDHR:
      "applicables à l'imposition des revenus de l'année 2025", in force
      Feb 2025) is for that year, not this one.
    """
    if not provenance or provenance.get("instrument_type") != "code":
        return False
    start = retrieval.validity_start(provenance.get("validity"))
    end = retrieval.validity_end(provenance.get("validity"))
    if start is None or start > retrieval_as_of or (end is not None and end <= retrieval_as_of):
        return False
    retrieved = provenance.get("retrieved_at")
    if provenance.get("open_ended") and retrieved is not None:
        retrieved_day = retrieved.date() if hasattr(retrieved, "date") else retrieved
        if retrieved_day < retrieval_as_of:
            return False
    names_this = re.search(rf"\b{income_year}\b", article_text) is not None
    for hit in re.finditer(rf"\b{income_year + 1}\b", article_text):
        if _APPLICABILITY.search(article_text[max(0, hit.start() - 200) : hit.start()]) and not names_this:
            return False
    return True


def _income_year_date_issues(
    valid_from: date | None,
    version_start: date | None,
    income_year: int,
    cited_text: str = "",
    consolidated_in_force: bool = False,
) -> tuple[list[str], bool]:
    """Mechanical date checks for income_year parameters.

    Returns (issues, provisional): issues empty = consistent; provisional=True
    when the cited version predates the budget-act window — the window opens
    1 December of the income year: finance acts for income year Y are normally
    promulgated late December Y (or later — Feb 2025 for LF 2025). An older
    version almost certainly states the previous year's value: the act for Y
    is not in the corpus (yet), which routes the item to PROVISIONAL rather
    than plain critique failure.

    Exemption: a cited text that NAMES the income year ("à compter de
    l'imposition des revenus de l'année 2025") proves its own vintage, however
    early it was enacted — the CDHR was instituted by LF 2025 (Feb 2025) FOR
    2025 income. Consolidated code articles drop such clauses (CGI art. 224
    never says 2025), so the year-naming extract is the finance-act article;
    the propose prompt nudges the model towards it.

    Second exemption, `consolidated_in_force` (decided by
    `_consolidated_in_force` from the corpus): the cited text is the code
    article as consolidated on the retrieval date, i.e. the text the income
    year's assessment applies — an old version start means the value did not
    change, not that the act is missing.
    """
    issues: list[str] = []
    provisional = False
    if valid_from != date(income_year, 1, 1):
        issues.append(
            f"income-year parameter: valid_from must be exactly {income_year}-01-01 "
            f"(the income-year start, NOT the act's publication or in-force date), got "
            f"{valid_from.isoformat() if valid_from else 'none'}"
        )
    window = date(income_year, 12, 1)
    names_year = re.search(rf"\b{income_year}\b", cited_text) is not None
    if (
        version_start is not None
        and version_start < window
        and not names_year
        and not consolidated_in_force
    ):
        provisional = True
        issues.append(
            f"cited version in force since {version_start.isoformat()} predates the "
            f"budget-act window for income year {income_year} and its text does not "
            f"name {income_year} — likely the previous year's value; the act for "
            f"{income_year} income may not be in the corpus yet (treat as provisional)"
        )
    return issues, provisional


#: Critique issues that mean "the establishing text is not in the corpus"
#: rather than "the model reasoned badly". Only these justify spending another
#: gap-fill round on a proposal that WAS produced: a unit-sanity or
#: value-support complaint is about the answer, and fetching more law cannot
#: fix it.
_SOURCE_GAP_ISSUES = (
    "citation_chunk_id missing",
    "predates the budget-act window",
    "never names income year",
)


def _needs_gap_fill(state: WorkflowState) -> bool:
    """Whether the corpus still looks like it is missing the establishing text.

    Three cases, all meaning "fetch more law and try again":
      * no proposal at all, or the analyst returned found=false;
      * the critique routed the item provisional (the act for this income year
        has not reached the corpus, so only last year's value was found);
      * the proposal exists but the critique failed for a source-availability
        reason — the cited chunk was not among the hits, or nothing ties the
        cited article to the income year.

    A proposal that survived the critique never triggers a round, and neither
    does one the critique rejected on its own merits.
    """
    draft = state.get("draft")
    if draft is None or not draft.found:
        return True
    report = state.get("critique")
    if report is None:
        return False
    # Provisional is checked before the verdict: it means the act for this
    # income year is not in the corpus, which is a source gap however the rest
    # of the critique came out.
    if report.provisional:
        return True
    if report.verdict == "pass":
        return False
    return any(marker in issue for issue in report.issues for marker in _SOURCE_GAP_ISSUES)


def _unchanged_window(proposed: ParameterValue, current: ParameterValue) -> ParameterValue:
    """The proposal rewritten to keep the validity window already in force.

    The value the law states is the one EUROMOD already holds, so the existing
    period simply continues: proposing a fresh valid_from (the model's date, or
    as_of) would read as a legislative change that did not happen. The citation
    re-confirms the value, it does not restart it — everything else about the
    proposal (evidence, legal_status, OJ date) is kept as proposed.
    """
    return proposed.model_copy(
        update={"valid_from": current.valid_from, "valid_to": current.valid_to}
    )


_ARTICLE_NUM = re.compile(r"art(?:icle|\.)\s*([0-9]+(?:\s+[A-Za-z]+)*)", re.IGNORECASE)

#: Stock openings of a French applicability clause. A finance-act article ends
#: with one — "II. - Les A et B du I s'appliquent à l'impôt sur le revenu dû au
#: titre de l'année 2024 et des années suivantes" — and it governs everything
#: above it, however far away that is.
_APPLICABILITY = re.compile(
    r"(s'appliquent?|applicables?|à compter de|au titre de|pour l'imposition|"
    r"aux revenus (?:perçus|réalisés))",
    re.IGNORECASE,
)


def _cross_article_year_proof(cited_citation: str | None, text: str, income_year: int) -> bool:
    """True when `text` ties the CITED article to the income year.

    Finance acts often state the applicability of a code article they created
    in a cross-reference — LF 2025 art. 10: "La contribution mentionnée au I
    de l'article 224 du code général des impôts due au titre de l'imposition
    des revenus de l'année 2025…". A mention of the cited article number with
    the income year nearby (±400 chars) proves the vintage of the cited
    consolidated article, which itself names no year.
    """
    if not cited_citation:
        return False
    match = _ARTICLE_NUM.search(cited_citation)
    if not match:
        return False
    number = match.group(1).strip()
    mentions = list(re.finditer(rf"article\s+{re.escape(number)}\b", text, re.IGNORECASE))
    if not mentions:
        return False
    for hit in mentions:
        window = text[max(0, hit.start() - 400) : hit.end() + 400]
        if re.search(rf"\b{income_year}\b", window):
            return True
    # Proximity is the strong signal but it is not how finance acts are drafted.
    # `text` is ONE article (pulled whole via retrieval.unit_chunks), and its
    # closing applicability clause governs every amendment above it: LF 2025
    # art. 2 rewrites the barème in CGI art. 197 at offset 199 and only says
    # "dû au titre de l'année 2024" at offset 5365 — 5 166 characters later, so
    # the window could never see it and every FR barème case refused. Inside a
    # single article, "this article mentions the cited article" plus "this
    # article carries an applicability clause for the income year" is the proof.
    for hit in re.finditer(rf"\b{income_year}\b", text):
        if _APPLICABILITY.search(text[max(0, hit.start() - 200) : hit.start()]):
            return True
    return False


def _current_value(record: ParameterRecord, as_of: date) -> ParameterValue | None:
    """The value in force at as_of, if any."""
    for value in record.values:
        if value.valid_from <= as_of and (value.valid_to is None or value.valid_to >= as_of):
            return value
    return None


def _draft_value(draft: ProposalDraft):
    return draft.value_brackets if draft.value_brackets is not None else draft.value_scalar


def build_workflow(cfg: WorkflowConfig, tracer: Tracer):
    """Assemble the workflow as a plain function; steps close over config, DB and tracer."""
    is_mock = cfg.model.startswith("mock")

    def frame(state: WorkflowState) -> dict:
        record = state["record"]
        info = record.information
        labels = {**(info.short_label or {}), **(info.label or {})}
        descriptions = info.description or {}
        # Prefer law-language text for the query: the FTS leg of hybrid retrieval
        # is language-specific, so an English-only record searches French law
        # poorly. Translations live in params.parameter_texts (best-effort:
        # no rows / no schema -> received text only, previous behaviour).
        lang = retrieval.LANG_BY_COUNTRY.get(info.country, "en")
        native: list[str] = []
        if lang not in labels and lang not in descriptions:
            try:
                with paramdb.connect(cfg) as conn:
                    texts = translate.law_language_texts(conn, info.model_target, lang)
                native = [t for f in ("short_label", "label", "description") if (t := texts.get(f))]
            except Exception:
                native = []
        # Native texts REPLACE the received ones in the query rather than being
        # appended: a mixed-language ~60-term query dilutes the BGE-M3 embedding
        # and turns the OR'd FTS leg into noise.
        parts = [_clean_query_text(p) for p in (native or [*labels.values(), *descriptions.values()])]
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
                    cr_hits = retrieval.country_report_search(
                        conn, info.country, state["as_of"], " ".join(ident), k=5
                    )
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
        with step_span(tracer, "frame", input_value={"model_target": info.model_target}) as span:
            set_output(
                span,
                {
                    "query": query,
                    "citations": citations,
                    "law_language_texts": len(native),
                    "cr_terms": cr_terms,
                    "cr_headings": cr_headings,
                },
            )
        return {"query": query, "citations": list(dict.fromkeys(citations)), "attempts": 0}

    def retrieve(state: WorkflowState) -> dict:
        info = state["record"].information
        retrieval_as_of = state.get("retrieval_as_of", state["as_of"])
        with step_span(
            tracer,
            "retrieve",
            kind="RETRIEVER",
            input_value={
                "query": state["query"],
                "citations": state["citations"],
                "as_of": state["as_of"].isoformat(),
                "retrieval_as_of": retrieval_as_of.isoformat(),
                "temporal_basis": info.temporal_basis,
                "country": info.country,
            },
        ) as span:
            with retrieval.connect(cfg) as conn:
                # Scope, not country: a regional parameter ($bsarg_rg24_*) may
                # draw on state law and its own community's law, never on a
                # sibling community's (ADR 0003). National parameters scope to
                # the country alone, so regional acts stay out of their runs.
                scope = retrieval.jurisdiction_scope(
                    conn, info.country, regions.region_key(info.country, info.model_target)
                )
                hits = retrieval.retrieve(
                    conn, cfg, scope, retrieval_as_of, state["query"], state["citations"]
                )
            span.set_attribute("retrieval.jurisdictions", json.dumps(scope))
            for i, hit in enumerate(hits):
                span.set_attribute(f"retrieval.documents.{i}.document.id", hit.chunk_id)
                span.set_attribute(f"retrieval.documents.{i}.document.score", hit.score or 0.0)
                span.set_attribute(f"retrieval.documents.{i}.document.content", hit.content[:500])
            set_output(span, [h.model_dump(mode="json", exclude={"content"}) for h in hits])
        return {"hits": hits, "jurisdictions": scope}

    def propose(state: WorkflowState) -> dict:
        record, as_of, hits = state["record"], state["as_of"], state["hits"]
        # A retry that repeats the same inputs re-rolls the same draft — feed
        # the failed critique back so the second attempt can actually differ.
        feedback = None
        if state.get("attempts", 0) and state.get("critique") and state["critique"].issues:
            feedback = "\n".join(f"- {issue}" for issue in state["critique"].issues)
        with step_span(
            tracer,
            "propose",
            input_value={
                "attempt": state.get("attempts", 0) + 1,
                "model": cfg.model,
                "feedback": feedback,
            },
        ) as span:
            if is_mock:
                def translation_lookup(chunk_id: str) -> str | None:
                    with retrieval.connect(cfg) as conn:
                        return retrieval.sibling_text(conn, chunk_id, "en")

                draft = mock.propose_with_mock(record, as_of, hits, translation_lookup)
            else:
                draft = llm.propose_with_llm(cfg.model, record, as_of, hits, feedback)
            set_output(span, draft)
        return {"draft": draft, "attempts": state.get("attempts", 0) + 1}

    def critique(state: WorkflowState) -> dict:
        record, as_of, draft, hits = state["record"], state["as_of"], state["draft"], state["hits"]
        info = record.information
        extra_hits: list[RetrievalHit] = []
        mech_notes: list[str] = []
        income_year_dates_proven = False
        with step_span(tracer, "critique", input_value=draft) as span:
            report = CritiqueReport(schema_valid=draft is not None, critique_model=cfg.critique_model)
            if draft is None or not draft.found:
                report.issues.append("no value proposed")
                # Surface WHY to the reviewer — the refusal usually names the
                # exact source that is missing from the corpus.
                if draft is not None and draft.reasoning:
                    report.issues.append(f"model: {draft.reasoning}")
            else:
                hit_ids = {h.chunk_id for h in hits}
                if draft.citation_chunk_id not in hit_ids and draft.supporting_extract:
                    resolved = _resolve_chunk_by_extract(hits, draft.supporting_extract)
                    if resolved is not None:
                        mech_notes.append(
                            f"citation_chunk_id {draft.citation_chunk_id!r} is not a retrieved "
                            f"chunk; resolved to {resolved} — the only retrieved chunk that "
                            "contains the supporting_extract verbatim"
                        )
                        draft.citation_chunk_id = resolved
                if draft.citation_chunk_id in hit_ids and draft.supporting_extract:
                    with retrieval.connect(cfg) as conn:
                        offsets = retrieval.verify_extract(
                            conn, draft.citation_chunk_id, draft.supporting_extract
                        )
                    report.citation_verified = offsets is not None
                    report.extract_offsets = offsets
                    if offsets is None:
                        report.issues.append(
                            "supporting_extract is not a verbatim quote of the cited chunk"
                        )
                else:
                    report.issues.append("citation_chunk_id missing or not among retrieved chunks")

                if draft.derivation:
                    # A derived value: the extract check, operand by operand,
                    # plus the arithmetic. Verified, the critique is told so
                    # (the value is not literally in any extract); failed, the
                    # proposal is rejected exactly like a non-verbatim quote.
                    with retrieval.connect(cfg) as conn:
                        derivation_issues, report.operand_offsets, note = _check_derivation(
                            draft,
                            hits,
                            lambda chunk_id, extract: retrieval.verify_extract(
                                conn, chunk_id, extract
                            ),
                        )
                    if derivation_issues:
                        report.citation_verified = False
                        report.issues.extend(derivation_issues)
                    else:
                        mech_notes.append(note)
                        report.issues.append(f"note: derived — {_derivation_summary(draft, hits)}")

                if info.temporal_basis == TemporalBasis.INCOME_YEAR:
                    # Publication after as_of is EXPECTED here (the finance act
                    # for income year Y arrives in Y+1); the real checks are
                    # back-dating and the budget-act window.
                    cited = next((h for h in hits if h.chunk_id == draft.citation_chunk_id), None)
                    # Vintage is proven at ARTICLE level: the value and the
                    # applicability clause ("revenus de l'année 2025") usually
                    # sit in different chunks of the same article — and the
                    # clause's chunk may not even have been retrieved. Read the
                    # cited article's FULL text from the corpus.
                    article_text = cited.content if cited else ""
                    if cited is not None:
                        try:
                            with retrieval.connect(cfg) as conn:
                                siblings = retrieval.unit_chunks(conn, cited.chunk_id)
                            article_text = " ".join(h.content for h in siblings) or article_text
                        except Exception:
                            siblings = []  # DB hiccup: fall back to the retrieved chunk
                    version_start = retrieval.validity_start(cited.validity) if cited else None
                    provenance = None
                    if cited is not None:
                        try:
                            with retrieval.connect(cfg) as conn:
                                provenance = retrieval.version_provenance(conn, cited.chunk_id)
                        except Exception:
                            provenance = None
                    retrieval_as_of = state.get("retrieval_as_of", as_of)
                    # The income year, not the system year — everything below
                    # must agree with _income_year_date_issues, which is the
                    # mechanical authority. The cross-reference proof used to
                    # take as_of.year here while the check above took the income
                    # year, so the proof hunted for a year the act never names.
                    income_year = income_year_for(as_of.year)
                    consolidated = _consolidated_in_force(
                        provenance, retrieval_as_of, income_year, article_text
                    )
                    date_issues, provisional = _income_year_date_issues(
                        draft.valid_from, version_start, income_year, article_text, consolidated
                    )
                    if consolidated and version_start is not None:
                        mech_notes.append(
                            f"the cited text is the consolidated code article in force on "
                            f"{retrieval_as_of.isoformat()} (version {provenance.get('validity')}, "
                            f"corpus snapshot {str(provenance.get('retrieved_at'))[:10]}): that is "
                            f"the text the assessment of income year {income_year} applies, so its "
                            f"in-force date of {version_start.isoformat()} is NOT an inconsistency "
                            f"and no finance-act clause naming {income_year} is required (the value "
                            f"simply did not change)"
                        )
                        report.issues.append(
                            f"note: consolidated code article in force on "
                            f"{retrieval_as_of.isoformat()} — applies to income year {income_year}"
                        )
                    if provisional:
                        # Provisional means CORPUS GAP. If a different article's
                        # extract names the income year, the corpus is fine —
                        # the proposal just cited the wrong act (consolidated
                        # article instead of the year-naming finance act):
                        # ordinary critique failure, retriable with feedback.
                        cited_citation = cited.citation if cited else None
                        alt = next(
                            (
                                h
                                for h in hits
                                if h.citation != cited_citation
                                and re.search(rf"\b{income_year}\b", h.content or "")
                            ),
                            None,
                        )
                        if alt is not None:
                            provisional = False
                            # Pull the WHOLE year-naming article: the proving
                            # clause may sit in a chunk retrieval never
                            # surfaced (LF 2025 art. 10: CDHR in chunk 1, its
                            # 2025 clause in chunk 2).
                            try:
                                with retrieval.connect(cfg) as conn:
                                    alt_siblings = retrieval.unit_chunks(conn, alt.chunk_id)
                            except Exception:
                                alt_siblings = [alt]
                            known = {h.chunk_id for h in hits}
                            extra_hits = [h for h in alt_siblings if h.chunk_id not in known]
                            alt_text = " ".join(h.content for h in alt_siblings)
                            if _cross_article_year_proof(cited_citation, alt_text, income_year):
                                # The year-naming act explicitly references the
                                # cited article for this income year: vintage
                                # proven, whatever chunk the model cited.
                                date_issues.pop()
                                mech_notes.append(
                                    f"applicability of the cited article to income year "
                                    f"{income_year} is established by the cross-reference in "
                                    f"({alt.citation}); its early in-force date is NOT an "
                                    f"inconsistency"
                                )
                                report.issues.append(
                                    f"note: applicability to income year {income_year} "
                                    f"established by cross-reference in ({alt.citation})"
                                )
                            else:
                                date_issues[-1] = (
                                    f"the cited article never names income year {income_year}, "
                                    f"but ({alt.citation}) does — cite the value from the "
                                    f"article whose text names income year {income_year} (the "
                                    f"value extract and the year clause may be different "
                                    f"portions of that article)"
                                )
                    report.dates_consistent = not date_issues
                    report.provisional = provisional
                    report.issues.extend(date_issues)
                    # All mechanical income-year date checks passed: the
                    # semantics are exactly what they encode, and LLM critics
                    # routinely mis-handle retroactive acts — the mechanical
                    # result is authoritative; LLM date doubts stay as issues.
                    income_year_dates_proven = not date_issues
                    if income_year_dates_proven and version_start is not None:
                        mech_notes.append(
                            f"the income-year vintage ({income_year}) of the cited article was "
                            f"verified deterministically against the full corpus text; do not "
                            f"fail dates_consistent for the in-force date "
                            f"({version_start.isoformat()}) or for the year clause sitting in "
                            f"another extract"
                        )
                else:
                    report.dates_consistent = draft.valid_from is not None and (
                        draft.legal_status != "enacted_in_force" or draft.valid_from <= as_of
                    )
                    if not report.dates_consistent:
                        report.issues.append(
                            "valid_from missing or inconsistent with legal_status/as_of"
                        )

                report.values_sane = _values_sane(info.unit, draft)
                if not report.values_sane:
                    report.issues.append("values fail sanity checks (unit range or bracket order)")

                # Informational only: appended to issues, never folded into the
                # four booleans the verdict is computed from.
                if guidance_only(cited_classes(draft, hits)):
                    report.issues.append(GUIDANCE_ONLY_ISSUE)

                # The LLM critique must see the sibling chunks too — the
                # applicability clause they carry is exactly what it needs to
                # judge dates_consistent.
                if extra_hits:
                    hits = [*hits, *extra_hits]

                findings = (
                    mock.critique_with_mock(draft)
                    if is_mock
                    else llm.critique_with_llm(
                        cfg.critique_model, record, as_of, draft, hits, mech_notes or None
                    )
                )
                report.issues.extend(findings.issues)
                report.citation_verified = report.citation_verified and findings.citation_supports_value
                report.dates_consistent = report.dates_consistent and (
                    findings.dates_consistent or income_year_dates_proven
                )
                report.values_sane = report.values_sane and findings.values_sane

                if (
                    report.schema_valid
                    and report.citation_verified
                    and report.dates_consistent
                    and report.values_sane
                ):
                    report.verdict = "pass"
            set_output(span, report)
        if extra_hits:
            # Sibling chunks of the year-naming article, so the proposal retry
            # (and the reviewer's source view) can see the applicability clause.
            return {"critique": report, "hits": hits}
        return {"critique": report}

    def diff(state: WorkflowState) -> dict:
        record, as_of, draft = state["record"], state["as_of"], state.get("draft")
        report = state.get("critique")
        info = record.information
        with step_span(tracer, "diff", input_value={"as_of": as_of.isoformat()}) as span:
            current = _current_value(record, as_of)
            proposed_value, proposed_record = None, None

            if state.get("derived_from"):
                routing = Routing.DERIVED
            elif current is not None and current.source_type == SourceType.NATIONAL_TEAM:
                routing = Routing.NATIONAL_TEAM_SOURCE
            elif draft is None or not draft.found:
                routing = Routing.NOT_FOUND
            elif report is not None and report.provisional:
                # The evidence found is (likely) the previous year's value: keep
                # the proposed_value so the reviewer sees WHAT was found, but no
                # proposed_record — there is nothing acceptable to export yet.
                routing = Routing.PROVISIONAL
                proposed_value = _build_proposed_value(state, cfg)
            else:
                proposed_value = _build_proposed_value(state, cfg)
                if current is None:
                    routing = Routing.NEW
                elif _values_equal(current.value, proposed_value.value):
                    routing = Routing.UNCHANGED
                    proposed_value = _unchanged_window(proposed_value, current)
                else:
                    routing = Routing.CHANGED
                proposed_record = _merge_record(record, proposed_value, as_of, routing)

            item = ReviewItem(
                id=queue_store.item_id(info.country, info.model_target, as_of.year),
                run_id=state["run_id"],
                phoenix_trace_id=state.get("phoenix_trace_id"),
                created_at=datetime.now(timezone.utc),
                country=info.country,
                model_target=info.model_target,
                as_of=as_of,
                system_year=as_of.year,
                value_type=info.value_type,
                unit=info.unit,
                label=(info.short_label or info.label or {}).get("en"),
                routing=routing,
                current_value=current,
                proposed_value=proposed_value,
                critique=report,
                guidance_only=guidance_only(
                    reference.source_trust_class
                    for reference in (proposed_value.references if proposed_value else [])
                ),
                retrieval_trace=[
                    h.model_copy(update={"content": ""}) for h in state.get("hits", [])
                ],
                proposed_record=proposed_record,
                parameter_file=state.get("parameter_file"),
                derived_from=state.get("derived_from") or None,
                scout=state["scout"].summary() if state.get("scout") else None,
                derivation=(
                    _derivation_summary(draft, state.get("hits", []))
                    if draft is not None and draft.found and draft.derivation
                    else None
                ),
            )
            set_output(span, {"routing": routing, "item_id": item.id})
        return {"routing": routing, "item": item}

    def enqueue(state: WorkflowState) -> dict:
        item = state["item"]
        # Keep full source texts on the item so the UI can show the cited law offline.
        item = item.model_copy(update={"retrieval_trace": state.get("hits", [])})
        written = queue_store.write_item(item, cfg.data_dir, force=state.get("force", False))
        with step_span(tracer, "enqueue", input_value={"item_id": item.id}) as span:
            set_output(span, {"written": written, "path": str(queue_store.queue_dir(cfg.data_dir))})
        return {"item": item, "enqueued": written}

    def _retry_proposal(state: WorkflowState) -> bool:
        report = state.get("critique")
        draft = state.get("draft")
        return (
            report is not None
            and report.verdict == "fail"
            # provisional is a corpus state, not a proposal defect: another
            # LLM attempt over the same chunks cannot produce the missing act
            and not report.provisional
            and draft is not None
            and draft.found
            and state.get("attempts", 0) < MAX_PROPOSAL_ATTEMPTS
            and not is_mock  # the mock extractor is deterministic; retrying can't help
        )

    def _scout_needs(state: WorkflowState) -> list[str]:
        """What the last proposal said it lacked, best first.

        `missing_sources` is the structured channel; the prose `reasoning` is the
        fallback for a model that left it empty, and it usually names the act
        anyway ("the extract only states the limit of four times the annual
        Social Security ceiling"). The critique's own issues come last: when the
        proposal looked fine but the critique could not tie it to the income
        year, the missing document is the applicability clause.
        """
        draft = state.get("draft")
        report = state.get("critique")
        needs: list[str] = []
        if draft is not None:
            needs += [s for s in draft.missing_sources if s.strip()]
            if not needs and draft.reasoning:
                needs.append(draft.reasoning)
        if not needs and report is not None:
            needs += [i for i in report.issues if not i.startswith("model:")][:2]
        return needs

    def scout_step(state: WorkflowState, round_index: int) -> dict:
        record, as_of = state["record"], state["as_of"]
        needs = _scout_needs(state)
        with step_span(
            tracer,
            "scout",
            kind="TOOL",
            input_value={
                "mode": cfg.scout,
                "model_target": record.information.model_target,
                "round": round_index,
                "needs": needs,
            },
        ) as span:
            # Scout hunts the ENACTING act: for income_year parameters that act
            # lives around the shifted retrieval date, not around as_of.
            result = scout.run(
                cfg,
                record,
                state.get("retrieval_as_of", as_of),
                needs=needs,
                known_citations=[h.citation for h in state.get("hits", []) if h.citation],
                attempted=state.setdefault("scout_attempted", set()),
                round_index=round_index,
            )
            set_output(span, result.summary())
        state["scout_attempted"].update(result.candidate_ids)
        rounds = [*state.get("scout_rounds", []), result]
        return {"scout_rounds": rounds, "scout": scout.merge_results(rounds)}

    def locate_step(state: WorkflowState) -> bool:
        """Look the last round's needs up in the corpus we hold; True when new chunks arrived.

        The scout's other half: `run` fetches what is missing, this finds what
        is present but ranked out — on the 2026-09-09 eval, six of nine "corpus
        gap" refusals named an act already held (LIRPF art. 66, Wet IB 2001
        art. 2.10, CSS art. D633-3, Finance Act 2024 …). Located chunks go in
        FRONT of the hits so the retry reads them first.
        """
        record, as_of = state["record"], state["as_of"]
        last = state["scout_rounds"][-1]
        known = [h.chunk_id for h in state.get("hits", [])]
        with step_span(
            tracer,
            "locate",
            kind="RETRIEVER",
            input_value={"needs": last.needs, "round": last.round},
        ) as span:
            located_hits, citations = scout.locate(
                cfg, record, state.get("retrieval_as_of", as_of), last.needs, known
            )
            last.located = citations
            state["scout"] = scout.merge_results(state["scout_rounds"])
            set_output(span, {"located": citations, "chunks": len(located_hits)})
        if not located_hits:
            return False
        progress(f"  [scout] located in the corpus: {', '.join(citations)}")
        state["hits"] = [*located_hits, *state.get("hits", [])]
        return True

    def _propose_and_critique(state: WorkflowState) -> None:
        while True:
            state.update(propose(state))
            state.update(critique(state))
            if not _retry_proposal(state):
                break

    def invoke(state: WorkflowState) -> WorkflowState:
        state = dict(state)
        record, as_of = state["record"], state["as_of"]
        state["retrieval_as_of"] = _retrieval_as_of(record, as_of)

        current = _current_value(record, as_of)

        # National-team-sourced values (a modelling assumption, a schedule set
        # below the national level) have no legislation to cite and are never
        # overwritten: route them without spending retrieval or LLM calls.
        # Without this the run costs a full propose+critique and a scout attempt
        # only for diff to discard the result at the very end.
        if current is not None and current.source_type == SourceType.NATIONAL_TEAM:
            with step_span(
                tracer, "national_team_source", input_value={"as_of": as_of.isoformat()}
            ) as span:
                set_output(span, {"routing": Routing.NATIONAL_TEAM_SOURCE})
            state.update({"hits": [], "citations": [], "attempts": 0})
            state.update(diff(state))
            state.update(enqueue(state))
            return state

        # Formula parameters ($PSS * 4) are never stated by legislation: route
        # them to their anchor without spending retrieval or LLM calls.
        derived = _derived_refs(record, current)
        if derived:
            with step_span(tracer, "derived", input_value={"references": derived}) as span:
                set_output(span, {"routing": Routing.DERIVED})
            state.update({"derived_from": derived, "hits": [], "citations": [], "attempts": 0})
            state.update(diff(state))
            state.update(enqueue(state))
            return state

        state.update(frame(state))
        state.update(retrieve(state))
        if state["hits"]:
            _propose_and_critique(state)

        # Gap-fill: the corpus is missing the text that sets the value -> discover
        # + archive-first ingest it, re-retrieve, re-propose. Each round is driven
        # by what the LAST proposal said it still lacked, so a chain of
        # cross-references resolves one hop per round (the code article names an
        # implementing order, which names another) instead of stopping after one.
        # It stops as soon as a proposal survives the critique, when a round
        # ingests nothing new, or at scout_max_rounds. Mock runs skip it entirely
        # to stay deterministic and offline.
        if cfg.scout != "off" and not is_mock:
            for round_index in range(1, cfg.scout_max_rounds + 1):
                if not _needs_gap_fill(state):
                    break
                state.update(scout_step(state, round_index))
                ingested = bool(state["scout_rounds"][-1].ingested)
                if ingested:
                    state.update(retrieve(state))
                # Whether or not anything was fetched, the named article may be
                # held and ranked out (a freshly ingested act's article can be
                # too): look it up directly. Nothing new from either leg means
                # another round would only ask the same question.
                if not locate_step(state) and not ingested:
                    break
                if state["hits"]:
                    _propose_and_critique(state)

        state.update(diff(state))
        state.update(enqueue(state))
        return state

    return invoke


def _resolve_chunk_by_extract(hits: list[RetrievalHit], extract: str) -> str | None:
    """The one retrieved chunk that contains `extract` verbatim, else None.

    The proposer transcribes a 36-character chunk id into its answer, and one
    hex digit off (`4a56d7eb…` for the retrieved `4a56d5eb…`) failed a correct
    27 382 on both attempts; another run put the citation string in the id
    field. The extract is the evidence the anti-hallucination check verifies,
    so when it sits character-for-character in exactly ONE retrieved chunk that
    chunk is the citation and the id was a typo. Two or more candidates (the
    same sentence in two versions of an article) keep the failure: guessing
    between them would cite a version the model never read.
    """
    needle = extract.strip()
    if not needle:
        return None
    matches = [h.chunk_id for h in hits if h.content and needle in h.content]
    return matches[0] if len(matches) == 1 else None


#: Figures a derivation may use without quoting them: calendar and scaling
#: constants (months, quarters, weeks, days in a year, percent, per mille).
#: Everything else is a fact about the law and must be an operand quoted
#: verbatim from a retrieved chunk — that is what keeps a derived value inside
#: the anti-hallucination contract.
DERIVATION_CONSTANTS = frozenset({1.0, 2.0, 4.0, 12.0, 13.0, 52.0, 100.0, 365.0, 366.0, 1000.0})
_DERIVATION_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def evaluate_derivation(expression: str, operands: dict[str, float]) -> float:
    """Evaluate `expression` over named operands.

    Raises ValueError for anything but + - * / over operand names and
    DERIVATION_CONSTANTS — no calls, no attributes, no other literals.
    """
    try:
        tree = ast.parse(expression.strip(), mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"derivation is not an arithmetic expression ({exc.msg})") from None

    def ev(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return ev(node.body)
        if (
            isinstance(node, ast.Constant)
            and isinstance(node.value, (int, float))
            and not isinstance(node.value, bool)
        ):
            if float(node.value) not in DERIVATION_CONSTANTS:
                raise ValueError(
                    f"bare figure {node.value} is not a quoted operand (only "
                    f"{sorted(int(c) for c in DERIVATION_CONSTANTS)} may appear unquoted)"
                )
            return float(node.value)
        if isinstance(node, ast.Name):
            if node.id not in operands:
                raise ValueError(f"operand {node.id!r} is not listed in operands")
            return operands[node.id]
        if isinstance(node, ast.BinOp) and type(node.op) in _DERIVATION_OPS:
            return _DERIVATION_OPS[type(node.op)](ev(node.left), ev(node.right))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = ev(node.operand)
            return -value if isinstance(node.op, ast.USub) else value
        raise ValueError("only + - * / over operand names and calendar constants are allowed")

    try:
        return float(ev(tree))
    except ZeroDivisionError:
        raise ValueError("derivation divides by zero") from None


_FIGURE = re.compile(r"\d(?:[\d\s\u00a0\u202f.,]*\d)?")


def _figures_in(text: str) -> set[float]:
    """Every reading of every number in `text`: «1 801,80» and «1.801,80»
    (thousands separators), «1,801.80», «9.139» (a Dutch thousand or an English
    decimal — both readings kept), «347,83»."""
    figures: set[float] = set()
    for raw in _FIGURE.findall(text):
        compact = re.sub(r"[\s\u00a0\u202f]", "", raw)
        for candidate in (
            compact,
            compact.replace(",", "."),
            compact.replace(".", "").replace(",", "."),
            compact.replace(",", ""),
        ):
            try:
                figures.add(float(candidate))
            except ValueError:
                pass
    return figures


def _extract_states(extract: str, value: float) -> bool:
    """Whether the extract states `value` — as such, or as a percentage (108 % for 1.08)."""
    return any(
        math.isclose(figure, target, rel_tol=1e-9, abs_tol=1e-9)
        for figure in _figures_in(extract)
        for target in (value, value * 100)
    )


def _derivation_summary(draft: ProposalDraft, hits: list[RetrievalHit]) -> str:
    """«a / b with a = 347.83 (AKW, artikel 12), b = 286.45 (AKW, artikel 12)» — for the reviewer."""
    citations = {h.chunk_id: h.citation for h in hits}
    parts = [
        f"{op.name} = {op.value:g} ({citations.get(op.citation_chunk_id) or op.citation_chunk_id})"
        for op in draft.operands
    ]
    return f"{draft.derivation} with " + ", ".join(parts)


def _check_derivation(
    draft: ProposalDraft,
    hits: list[RetrievalHit],
    verify,
) -> tuple[list[str], list[tuple[int, int] | None], str | None]:
    """Mechanical check of a derived proposal — the extract check, per operand.

    `verify(chunk_id, extract)` returns the extract's offsets in the chunk or
    None (retrieval.verify_extract in production). Every operand must cite a
    retrieved chunk, quote it verbatim and state its own figure; the
    expression may use only those operands and calendar constants; and it
    must evaluate to the proposed value. Returns (issues, operand offsets,
    note for the critique) — issues empty means verified.
    """
    if draft.value_brackets is not None or draft.value_scalar is None:
        return ["derivation: only a scalar value can be derived"], [], None
    if not draft.operands:
        return ["derivation: no operands quoted"], [], None
    issues: list[str] = []
    offsets: list[tuple[int, int] | None] = []
    hit_ids = {h.chunk_id for h in hits}
    values: dict[str, float] = {}
    for op in draft.operands:
        where = f"operand {op.name}"
        if op.name in values:
            issues.append(f"derivation: {where} is listed twice")
            offsets.append(None)
            continue
        values[op.name] = op.value
        if op.citation_chunk_id not in hit_ids:
            issues.append(f"derivation: {where} cites a chunk that was not retrieved")
            offsets.append(None)
            continue
        span = verify(op.citation_chunk_id, op.supporting_extract)
        offsets.append(span)
        if span is None:
            issues.append(f"derivation: {where}'s extract is not a verbatim quote of its chunk")
        elif not _extract_states(op.supporting_extract, op.value):
            issues.append(f"derivation: {where}'s extract does not state {op.value:g}")
    if issues:
        return issues, offsets, None
    try:
        result = evaluate_derivation(draft.derivation or "", values)
    except ValueError as exc:
        return [f"derivation: {exc}"], offsets, None
    if not math.isclose(result, draft.value_scalar, rel_tol=1e-3, abs_tol=1e-6):
        return [
            f"derivation: {draft.derivation} evaluates to {result:g}, "
            f"not the proposed {draft.value_scalar:g}"
        ], offsets, None
    note = (
        f"derivation verified deterministically: {_derivation_summary(draft, hits)} = {result:g}; "
        "every operand extract is verbatim in its cited chunk and states its figure, so do NOT "
        "fail citation_supports_value for the value not being stated literally — judge whether "
        "these are the right operands and the right formula for the parameter"
    )
    return [], offsets, note


def _values_sane(unit: str, draft: ProposalDraft) -> bool:
    """Unit-range and bracket-order sanity."""
    if draft.value_brackets is not None:
        thresholds = [b.threshold for b in draft.value_brackets]
        if thresholds != sorted(thresholds) or len(set(thresholds)) != len(thresholds):
            return False
        if unit == "/1":
            return all(b.rate is None or 0.0 <= b.rate <= 1.0 for b in draft.value_brackets)
        return True
    if draft.value_scalar is not None and unit == "/1":
        return 0.0 <= draft.value_scalar <= 1.0
    return draft.value_scalar is not None


def _build_proposed_value(state: WorkflowState, cfg: WorkflowConfig) -> ParameterValue:
    """Assemble the Activity 1 value envelope from the draft + critique + trace."""
    draft: ProposalDraft = state["draft"]
    report: CritiqueReport | None = state.get("critique")
    hits: list[RetrievalHit] = state.get("hits", [])
    cited = next((h for h in hits if h.chunk_id == draft.citation_chunk_id), None)
    references = []
    if cited is not None:
        references.append(
            Reference(
                title=cited.citation or (cited.context_header or "retrieved chunk"),
                supporting_extract=draft.supporting_extract,
                extract_offsets=report.extract_offsets if report else None,
                jrc_database_id=cited.chunk_id,
                source_trust_class=cited.source_trust_class,
            )
        )
    model_answer = draft.reasoning
    if draft.derivation:
        # One reference per operand, so the reviewer sees every figure the
        # value was computed from with its own verbatim quote; the primary
        # reference is kept first and not repeated.
        offsets = (report.operand_offsets if report else None) or []
        for index, operand in enumerate(draft.operands):
            source = next((h for h in hits if h.chunk_id == operand.citation_chunk_id), None)
            if source is None or (
                operand.citation_chunk_id == draft.citation_chunk_id
                and operand.supporting_extract == draft.supporting_extract
            ):
                continue
            references.append(
                Reference(
                    title=source.citation or (source.context_header or "retrieved chunk"),
                    supporting_extract=operand.supporting_extract,
                    extract_offsets=offsets[index] if index < len(offsets) else None,
                    jrc_database_id=source.chunk_id,
                    source_trust_class=source.source_trust_class,
                )
            )
        model_answer = f"Derived: {_derivation_summary(draft, hits)}. {draft.reasoning or ''}".strip()
    return ParameterValue(
        value=_draft_value(draft),
        valid_from=draft.valid_from or state["as_of"],
        valid_to=draft.valid_to,
        legal_status=draft.legal_status,
        source_type=SourceType.LEGISLATION,
        official_journal_date=draft.official_journal_date,
        references=references,
        lineage=Lineage(
            proposed_by="pipeline",
            run_id=state["run_id"],
            prompt_version=PROMPT_VERSION,
            agent_version=AGENT_VERSION,
            model=cfg.model,
            model_answer=model_answer,
            confidence=draft.confidence,
            retrieval_trace=[h.model_copy(update={"content": ""}) for h in hits],
        ),
    )


def _merge_record(
    record: ParameterRecord, proposed: ParameterValue, as_of: date, routing: Routing
) -> ParameterRecord:
    """The full record as it would look after acceptance (export-first write-back)."""
    merged = record.model_copy(deep=True)
    if routing == Routing.UNCHANGED:
        merged.information.last_confirmed_valid_on = as_of
        return merged
    for value in merged.values:
        if value.valid_to is None and value.valid_from < proposed.valid_from:
            value.valid_to = proposed.valid_from - timedelta(days=1)
    merged.values.append(proposed)
    merged.information.last_confirmed_valid_on = as_of
    return merged


def run_parameter(
    cfg: WorkflowConfig,
    tracer: Tracer,
    parameter_file: Path,
    as_of: date,
    force: bool = False,
) -> ReviewItem:
    """Run the full workflow for one parameter file; returns the queue item."""
    record = queue_store.load_record(parameter_file)
    info = record.information
    run_id = f"{datetime.now(timezone.utc):%Y-%m-%dT%H:%MZ}#{info.country.lower()}-{uuid.uuid4().hex[:6]}"
    workflow = build_workflow(cfg, tracer)
    started_at = datetime.now(timezone.utc)
    with step_span(
        tracer,
        f"parameter_update {info.model_target}",
        kind="AGENT",
        input_value={
            "country": info.country,
            "model_target": info.model_target,
            "as_of": as_of.isoformat(),
            "run_id": run_id,
            "model": cfg.model,
            "prompt_version": PROMPT_VERSION,
            "agent_version": AGENT_VERSION,
        },
    ) as span:
        # The trace id is fixed at root-span creation; carried through the state
        # so the queue item and params.extraction_runs both link to Phoenix.
        span_context = span.get_span_context()
        phoenix_trace_id = f"{span_context.trace_id:032x}" if span_context.is_valid else None
        if phoenix_trace_id:
            progress(f"  phoenix trace {phoenix_trace_id} → {cfg.phoenix_endpoint}")
        result = workflow(
            {
                "record": record,
                "parameter_file": str(parameter_file),
                "as_of": as_of,
                "run_id": run_id,
                "phoenix_trace_id": phoenix_trace_id,
                "force": force,
            }
        )
        set_output(span, {"routing": result["routing"], "item_id": result["item"].id})
    item: ReviewItem = result["item"]
    paramdb.record_run_safe(
        cfg, item, PROMPT_VERSION, AGENT_VERSION, started_at, datetime.now(timezone.utc)
    )
    return item
