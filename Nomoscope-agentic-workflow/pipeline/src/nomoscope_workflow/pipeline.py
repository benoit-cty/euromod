"""The agentic workflow: an explicit pipeline of steps, deterministic wherever possible.

frame -> retrieve -> propose -> critique -> diff -> enqueue
                 \\ (no hits) ----------------/    (one LLM retry on critique fail)

LLM steps: propose, critique — both PydanticAI structured-output calls (skipped
mechanics stay). Everything else is code: retrieval is SQL, citation
verification is a string match against the corpus, diffing and routing are
pure functions. One Phoenix trace per parameter run.
"""

from __future__ import annotations

import re
import uuid
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import TypedDict

from opentelemetry.trace import Tracer

from . import AGENT_VERSION, llm, mock, paramdb, queue_store, retrieval, scout, translate
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
    TemporalBasis,
    income_year_for,
)
from .tracing import progress, set_output, step_span

MAX_PROPOSAL_ATTEMPTS = 2


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
    hits: list[RetrievalHit]
    draft: ProposalDraft | None
    critique: CritiqueReport | None
    attempts: int
    routing: Routing
    item: ReviewItem
    enqueued: bool
    derived_from: list[str]
    scout: scout.ScoutResult


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


def _income_year_date_issues(
    valid_from: date | None,
    version_start: date | None,
    income_year: int,
    cited_text: str = "",
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
    if version_start is not None and version_start < window and not names_year:
        provisional = True
        issues.append(
            f"cited version in force since {version_start.isoformat()} predates the "
            f"budget-act window for income year {income_year} and its text does not "
            f"name {income_year} — likely the previous year's value; the act for "
            f"{income_year} income may not be in the corpus yet (treat as provisional)"
        )
    return issues, provisional


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
    for hit in re.finditer(rf"article\s+{re.escape(number)}\b", text, re.IGNORECASE):
        window = text[max(0, hit.start() - 400) : hit.end() + 400]
        if re.search(rf"\b{income_year}\b", window):
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
        parts = native or [*labels.values(), *descriptions.values()]
        query = " ".join(dict.fromkeys(parts)) or info.model_target
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
                hits = retrieval.retrieve(
                    conn, cfg, info.country, retrieval_as_of, state["query"], state["citations"]
                )
            for i, hit in enumerate(hits):
                span.set_attribute(f"retrieval.documents.{i}.document.id", hit.chunk_id)
                span.set_attribute(f"retrieval.documents.{i}.document.score", hit.score or 0.0)
                span.set_attribute(f"retrieval.documents.{i}.document.content", hit.content[:500])
            set_output(span, [h.model_dump(mode="json", exclude={"content"}) for h in hits])
        return {"hits": hits}

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
                    date_issues, provisional = _income_year_date_issues(
                        draft.valid_from, version_start, income_year_for(as_of.year), article_text
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
                                and re.search(rf"\b{as_of.year}\b", h.content or "")
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
                            if _cross_article_year_proof(cited_citation, alt_text, as_of.year):
                                # The year-naming act explicitly references the
                                # cited article for this income year: vintage
                                # proven, whatever chunk the model cited.
                                date_issues.pop()
                                mech_notes.append(
                                    f"applicability of the cited article to income year "
                                    f"{as_of.year} is established by the cross-reference in "
                                    f"({alt.citation}); its early in-force date is NOT an "
                                    f"inconsistency"
                                )
                                report.issues.append(
                                    f"note: applicability to income year {as_of.year} "
                                    f"established by cross-reference in ({alt.citation})"
                                )
                            else:
                                date_issues[-1] = (
                                    f"the cited article never names income year {as_of.year}, "
                                    f"but ({alt.citation}) does — cite the value from the "
                                    f"article whose text names income year {as_of.year} (the "
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
                            f"the income-year vintage ({as_of.year}) of the cited article was "
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
                retrieval_trace=[
                    h.model_copy(update={"content": ""}) for h in state.get("hits", [])
                ],
                proposed_record=proposed_record,
                parameter_file=state.get("parameter_file"),
                derived_from=state.get("derived_from") or None,
                scout=state["scout"].summary() if state.get("scout") else None,
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

    def scout_step(state: WorkflowState) -> dict:
        record, as_of = state["record"], state["as_of"]
        with step_span(
            tracer,
            "scout",
            kind="TOOL",
            input_value={"mode": cfg.scout, "model_target": record.information.model_target},
        ) as span:
            # Scout hunts the ENACTING act: for income_year parameters that act
            # lives around the shifted retrieval date, not around as_of.
            result = scout.run(cfg, record, state.get("retrieval_as_of", as_of))
            set_output(span, result.summary())
        return {"scout": result}

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

        # Gap-fill: nothing usable retrieved — or only the previous year's value
        # (provisional) — -> discover + archive-first ingest the missing
        # instrument, then retry retrieval once. Mock runs skip it to stay
        # deterministic and offline.
        draft = state.get("draft")
        critique_report = state.get("critique")
        provisional = critique_report is not None and critique_report.provisional
        if cfg.scout != "off" and not is_mock and (draft is None or not draft.found or provisional):
            state.update(scout_step(state))
            if state["scout"].ingested:
                state.update(retrieve(state))
                if state["hits"]:
                    _propose_and_critique(state)

        state.update(diff(state))
        state.update(enqueue(state))
        return state

    return invoke


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
            )
        )
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
            model_answer=draft.reasoning,
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
