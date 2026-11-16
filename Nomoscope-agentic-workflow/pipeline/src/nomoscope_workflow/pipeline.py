"""The agentic workflow: an explicit pipeline of steps, deterministic wherever possible.

frame -> retrieve -> propose -> critique -> diff -> enqueue
                 \\ (no hits) ----------------/    (one LLM retry on critique fail)

LLM steps: propose, critique — both PydanticAI structured-output calls (skipped
mechanics stay). Everything else is code: retrieval is SQL, citation
verification is a string match against the corpus, diffing and routing are
pure functions. One Phoenix trace per parameter run.
"""

from __future__ import annotations

import json
import re
import uuid
from datetime import date, datetime, timezone
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import TypedDict

from opentelemetry.trace import Tracer

from . import AGENT_VERSION, issues, llm, mock, paramdb, queue_store, quotes, regions, retrieval, scout
from .config import WorkflowConfig
from .prompts import PROMPT_VERSION
from .schema import (
    CritiqueFindings,
    CritiqueReport,
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
from .derivation import (  # noqa: F401  (re-exported for callers and tests)
    DERIVATION_CONSTANTS,
    DERIVATION_MAX_DIGITS,
    _check_derivation,
    _derivation_summary,
    _extract_states,
    _figures_in,
    _round_like_held,
    _values_sane,
    evaluate_derivation,
)
from .framing import _clean_query_text, frame_query  # noqa: F401
from .routing import (  # noqa: F401
    _confirms_held,
    _current_value,
    _derived_refs,
    _draft_value,
    _merge_record,
    _unchanged_window,
    _values_equal,
)
from .temporal import (  # noqa: F401
    _consolidated_in_force,
    _cross_article_year_proof,
    _income_year_date_issues,
    _later_until,
    _retrieval_as_of,
)

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
    #: What the run was asked for: a `euromod://…` target or `group:<group_id>`.
    parameter_ref: str
    as_of: date
    # Date used to select in-force legislation versions; differs from as_of
    # for income_year parameters (see _retrieval_as_of).
    retrieval_as_of: date
    run_id: str
    phoenix_trace_id: str | None
    force: bool
    #: False = return the item without writing it to params.review_queue (the
    #: evaluation pipeline keeps the item itself and scores it).
    enqueue: bool
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


#: Critique issues that mean "the establishing text is not in the corpus"
#: rather than "the model reasoned badly". Only these justify spending another
#: gap-fill round on a proposal that WAS produced: a unit-sanity or
#: value-support complaint is about the answer, and fetching more law cannot
#: fix it.


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
    return any(issues.code_of(issue) in issues.SOURCE_GAP for issue in report.issues)


@dataclass(slots=True)
class StepContext:
    """What every step reads besides the state: config, tracer and the two LLM calls.

    The steps are module-level functions `step(ctx, state) -> delta` so they
    can be imported and tested one by one; the proposer and the critic are
    injected (`build_workflow` picks the LLM or the deterministic mock), which
    is also what replaced the four `is_mock` branches (code audit 4, design).
    """

    cfg: WorkflowConfig
    tracer: Tracer
    proposer: Callable[[ParameterRecord, date, list[RetrievalHit], str | None], ProposalDraft]
    critic: Callable[
        [ParameterRecord, date, ProposalDraft, list[RetrievalHit], list[str] | None], CritiqueFindings
    ]
    #: Deterministic proposer (mock): no retry, no gap-fill (offline, repeatable).
    deterministic: bool = False


def step_context(cfg: WorkflowConfig, tracer: Tracer) -> StepContext:
    """The production wiring: the LLM named by cfg, or the key-less mock."""
    if cfg.model.startswith("mock"):
        return StepContext(
            cfg=cfg,
            tracer=tracer,
            proposer=lambda record, as_of, hits, feedback: mock.propose_with_mock(record, as_of, hits),
            critic=lambda record, as_of, draft, hits, notes: mock.critique_with_mock(draft),
            deterministic=True,
        )
    return StepContext(
        cfg=cfg,
        tracer=tracer,
        proposer=lambda record, as_of, hits, feedback: llm.propose_with_llm(
            cfg.model, record, as_of, hits, feedback
        ),
        critic=lambda record, as_of, draft, hits, notes: llm.critique_with_llm(
            cfg.critique_model, record, as_of, draft, hits, notes
        ),
    )


def frame(ctx: StepContext, state: WorkflowState) -> dict:
    record = state["record"]
    framed = frame_query(ctx.cfg, record, state["as_of"])
    with step_span(ctx.tracer, "frame", input_value={"model_target": record.information.model_target}) as span:
        set_output(span, framed)
    return {"query": framed["query"], "citations": framed["citations"], "attempts": 0}

def retrieve(ctx: StepContext, state: WorkflowState) -> dict:
    info = state["record"].information
    retrieval_as_of = state.get("retrieval_as_of", state["as_of"])
    with step_span(
        ctx.tracer,
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
        with retrieval.connect(ctx.cfg) as conn:
            # Scope, not country: a regional parameter ($bsarg_rg24_*) may
            # draw on state law and its own community's law, never on a
            # sibling community's (ADR 0003). National parameters scope to
            # the country alone, so regional acts stay out of their runs.
            scope = retrieval.jurisdiction_scope(
                conn, info.country, regions.region_key(info.country, info.model_target)
            )
            hits = retrieval.retrieve(
                conn, ctx.cfg, scope, retrieval_as_of, state["query"], state["citations"],
                later_until=_later_until(state["record"], state["as_of"]),
            )
        span.set_attribute("retrieval.jurisdictions", json.dumps(scope))
        for i, hit in enumerate(hits):
            span.set_attribute(f"retrieval.documents.{i}.document.id", hit.chunk_id)
            span.set_attribute(f"retrieval.documents.{i}.document.score", hit.score or 0.0)
            span.set_attribute(f"retrieval.documents.{i}.document.content", hit.content[:500])
        set_output(span, [h.model_dump(mode="json", exclude={"content"}) for h in hits])
    return {"hits": hits, "jurisdictions": scope}

def propose(ctx: StepContext, state: WorkflowState) -> dict:
    record, as_of, hits = state["record"], state["as_of"], state["hits"]
    # A retry that repeats the same inputs re-rolls the same draft — feed
    # the failed critique back so the second attempt can actually differ.
    feedback = None
    if state.get("attempts", 0) and state.get("critique") and state["critique"].issues:
        feedback = "\n".join(f"- {issue}" for issue in state["critique"].issues)
    with step_span(
        ctx.tracer,
        "propose",
        input_value={
            "attempt": state.get("attempts", 0) + 1,
            "model": ctx.cfg.model,
            "feedback": feedback,
        },
    ) as span:
        draft = ctx.proposer(record, as_of, hits, feedback)
        set_output(span, draft)
    return {"draft": draft, "attempts": state.get("attempts", 0) + 1}

def critique(ctx: StepContext, state: WorkflowState) -> dict:
    record, as_of, draft, hits = state["record"], state["as_of"], state["draft"], state["hits"]
    info = record.information
    extra_hits: list[RetrievalHit] = []
    mech_notes: list[str] = []
    income_year_dates_proven = False
    with step_span(ctx.tracer, "critique", input_value=draft) as span:
        report = CritiqueReport(schema_valid=draft is not None, critique_model=ctx.cfg.critique_model)
        if draft is None or not draft.found:
            report.issues.append("no value proposed")
            # Surface WHY to the reviewer — the refusal usually names the
            # exact source that is missing from the corpus.
            if draft is not None and draft.reasoning:
                report.issues.append(f"model: {draft.reasoning}")
        else:
            # The verbatim rule (quotes.check_quote): resolve a mistyped
            # id, re-point a swapped one, verify against the chunk named.
            if draft.supporting_extract:
                with retrieval.connect(ctx.cfg) as conn:
                    check = quotes.check_quote(
                        hits,
                        draft.citation_chunk_id,
                        draft.supporting_extract,
                        lambda chunk_id, extract: quotes.verify_extract(conn, chunk_id, extract),
                    )
                mech_notes.extend(check.notes)
                draft.citation_chunk_id = check.chunk_id
            if not draft.supporting_extract or check.status == "not_retrieved":
                report.issues.append(issues.CITATION_NOT_RETRIEVED)
            else:
                report.citation_verified = check.verified
                report.extract_offsets = check.offsets
                if not check.verified:
                    report.issues.append(issues.NOT_VERBATIM)
                    if check.hint:
                        report.issues.append(check.hint)

            if draft.derivation:
                # A derived value: the extract check, operand by operand,
                # plus the arithmetic. Verified, the critique is told so
                # (the value is not literally in any extract); failed, the
                # proposal is rejected exactly like a non-verbatim quote.
                with retrieval.connect(ctx.cfg) as conn:
                    derivation_issues, report.operand_offsets, note = _check_derivation(
                        draft,
                        hits,
                        lambda chunk_id, extract: quotes.verify_extract(
                            conn, chunk_id, extract
                        ),
                    )
                if derivation_issues:
                    report.citation_verified = False
                    report.issues.extend(derivation_issues)
                else:
                    mech_notes.append(note)
                    report.issues.append(f"note: derived — {_derivation_summary(draft, hits)}")
                    result = (
                        evaluate_derivation(draft.derivation, {op.name: op.value for op in draft.operands})
                        if draft.value_brackets is None
                        else None
                    )
                    rounded = _round_like_held(info.unit, draft, _current_value(record, as_of), result)
                    if rounded is not None:
                        report.issues.append(rounded)

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
                # No `except Exception` here: a DB error used to fall back to
                # "no siblings, no provenance" and could flip a correct
                # proposal to provisional (code audit 4); now it fails the run.
                siblings = []
                provenance = None
                if cited is not None:
                    with retrieval.connect(ctx.cfg) as conn:
                        siblings = retrieval.unit_chunks(conn, cited.chunk_id)
                        provenance = retrieval.version_provenance(conn, cited.chunk_id)
                    article_text = " ".join(h.content for h in siblings) or article_text
                version_start = retrieval.validity_start(cited.validity) if cited else None
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
                        with retrieval.connect(ctx.cfg) as conn:
                            alt_siblings = retrieval.unit_chunks(conn, alt.chunk_id) or [alt]
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
                cited = next((h for h in hits if h.chunk_id == draft.citation_chunk_id), None)
                later = cited is not None and cited.method == "later_in_year"
                # A version entering into force later in the system year
                # may take effect after as_of: the year's value, not 1 July's.
                # A start_of_year parameter is dated 1 January throughout.
                reference = state.get("retrieval_as_of", as_of)
                latest = date(as_of.year, 12, 31) if later else reference
                report.dates_consistent = draft.valid_from is not None and (
                    draft.legal_status != "enacted_in_force" or draft.valid_from <= latest
                )
                if not report.dates_consistent:
                    report.issues.append(
                        "valid_from missing or inconsistent with legal_status/as_of"
                    )
                elif later:
                    version_start = retrieval.validity_start(cited.validity)
                    mech_notes.append(
                        f"the cited version enters into force on {version_start}, after the "
                        f"reference date {as_of.isoformat()} but within system year "
                        f"{as_of.year}, which the parameter describes as a whole: a valid_from "
                        f"before that date is consistent when the text itself applies the value "
                        f"from then (e.g. «à compter du 1er janvier {as_of.year}»)"
                    )
                    report.issues.append(
                        f"note: cites a version in force from {version_start}, later in "
                        f"system year {as_of.year} than the reference date"
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

            findings = ctx.critic(record, as_of, draft, hits, mech_notes or None)
            report.issues.extend(findings.issues)
            report.citation_verified = report.citation_verified and findings.citation_supports_value
            # Confirming the value EUROMOD already holds changes nothing,
            # whatever date the proposal gives it: tscersi_rate2 (0.07) and
            # tscer_red_coef2 (0.3233) were right and refused on the 5 Nov
            # run for a valid_from the critique would have dated otherwise.
            confirms_held = findings.citation_supports_value and _confirms_held(
                draft, _current_value(record, as_of)
            )
            if confirms_held and not findings.dates_consistent:
                report.issues.append(
                    "note: the value is the one already held; the start-date objection "
                    "does not block a confirmation"
                )
            report.dates_consistent = report.dates_consistent and (
                findings.dates_consistent or income_year_dates_proven or confirms_held
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

def diff(ctx: StepContext, state: WorkflowState) -> dict:
    record, as_of, draft = state["record"], state["as_of"], state.get("draft")
    report = state.get("critique")
    info = record.information
    with step_span(ctx.tracer, "diff", input_value={"as_of": as_of.isoformat()}) as span:
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
            proposed_value = _build_proposed_value(state, ctx.cfg)
        else:
            proposed_value = _build_proposed_value(state, ctx.cfg)
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
            parameter_ref=state.get("parameter_ref"),
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

def enqueue(ctx: StepContext, state: WorkflowState) -> dict:
    item = state["item"]
    # Keep full source texts on the item so the UI can show the cited law
    # without another corpus query.
    item = item.model_copy(update={"retrieval_trace": state.get("hits", [])})
    wanted = state.get("enqueue", True)
    written = False
    with step_span(
        ctx.tracer, "enqueue", input_value={"item_id": item.id, "enqueue": wanted}
    ) as span:
        if wanted:
            # The queue is rows in params.review_queue (ADR 0004); a DB that
            # refuses the write fails the run — there is no file to fall
            # back on, and a silently lost item is worse than a failed run.
            with paramdb.connect(ctx.cfg) as conn:
                written = queue_store.write_item(conn, item, force=state.get("force", False))
        set_output(span, {"written": written})
    return {"item": item, "enqueued": written}

def _retry_proposal(ctx: StepContext, state: WorkflowState) -> bool:
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
        and (
            state.get("attempts", 0) < MAX_PROPOSAL_ATTEMPTS
            or (state.get("attempts", 0) < MAX_PROPOSAL_ATTEMPTS + 1 and quotes.misquoted_only(report.issues))
        )
        and not ctx.deterministic  # the mock extractor is deterministic; retrying can't help
    )

def _scout_needs(ctx: StepContext, state: WorkflowState) -> list[str]:
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

def scout_step(ctx: StepContext, state: WorkflowState, round_index: int) -> dict:
    record, as_of = state["record"], state["as_of"]
    needs = _scout_needs(ctx, state)
    with step_span(
        ctx.tracer,
        "scout",
        kind="TOOL",
        input_value={
            "mode": ctx.cfg.scout,
            "model_target": record.information.model_target,
            "round": round_index,
            "needs": needs,
        },
    ) as span:
        # Scout hunts the ENACTING act: for income_year parameters that act
        # lives around the shifted retrieval date, not around as_of.
        result = scout.run(
            ctx.cfg,
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

def locate_step(ctx: StepContext, state: WorkflowState) -> bool:
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
        ctx.tracer,
        "locate",
        kind="RETRIEVER",
        input_value={"needs": last.needs, "round": last.round},
    ) as span:
        located_hits, citations = scout.locate(
            ctx.cfg, record, state.get("retrieval_as_of", as_of), last.needs, known,
            later_until=_later_until(record, as_of),
        )
        last.located = citations
        state["scout"] = scout.merge_results(state["scout_rounds"])
        set_output(span, {"located": citations, "chunks": len(located_hits)})
    if not located_hits:
        return False
    progress(f"  [scout] located in the corpus: {', '.join(citations)}")
    state["hits"] = [*located_hits, *state.get("hits", [])]
    return True

def _propose_and_critique(ctx: StepContext, state: WorkflowState) -> None:
    while True:
        state.update(propose(ctx, state))
        state.update(critique(ctx, state))
        if not _retry_proposal(ctx, state):
            break

def invoke(ctx: StepContext, state: WorkflowState) -> WorkflowState:
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
            ctx.tracer, "national_team_source", input_value={"as_of": as_of.isoformat()}
        ) as span:
            set_output(span, {"routing": Routing.NATIONAL_TEAM_SOURCE})
        state.update({"hits": [], "citations": [], "attempts": 0})
        state.update(diff(ctx, state))
        state.update(enqueue(ctx, state))
        return state

    # Formula parameters ($PSS * 4) are never stated by legislation: route
    # them to their anchor without spending retrieval or LLM calls.
    derived = _derived_refs(record, current)
    if derived:
        with step_span(ctx.tracer, "derived", input_value={"references": derived}) as span:
            set_output(span, {"routing": Routing.DERIVED})
        state.update({"derived_from": derived, "hits": [], "citations": [], "attempts": 0})
        state.update(diff(ctx, state))
        state.update(enqueue(ctx, state))
        return state

    state.update(frame(ctx, state))
    state.update(retrieve(ctx, state))
    if state["hits"]:
        _propose_and_critique(ctx, state)

    # Gap-fill: the corpus is missing the text that sets the value -> discover
    # + archive-first ingest it, re-retrieve, re-propose. Each round is driven
    # by what the LAST proposal said it still lacked, so a chain of
    # cross-references resolves one hop per round (the code article names an
    # implementing order, which names another) instead of stopping after one.
    # It stops as soon as a proposal survives the critique, when a round
    # ingests nothing new, or at scout_max_rounds. Mock runs skip it entirely
    # to stay deterministic and offline.
    if ctx.cfg.scout != "off" and not ctx.deterministic:
        for round_index in range(1, ctx.cfg.scout_max_rounds + 1):
            if not _needs_gap_fill(state):
                break
            state.update(scout_step(ctx, state, round_index))
            ingested = bool(state["scout_rounds"][-1].ingested)
            if ingested:
                state.update(retrieve(ctx, state))
            # Whether or not anything was fetched, the named article may be
            # held and ranked out (a freshly ingested act's article can be
            # too): look it up directly. Nothing new from either leg means
            # another round would only ask the same question.
            if not locate_step(ctx, state) and not ingested:
                break
            if state["hits"]:
                _propose_and_critique(ctx, state)

    state.update(diff(ctx, state))
    state.update(enqueue(ctx, state))
    return state



def build_workflow(cfg: WorkflowConfig, tracer: Tracer):
    """The workflow as a plain function of the state (see `invoke`)."""
    ctx = step_context(cfg, tracer)
    return lambda state: invoke(ctx, state)


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
            # only the hits the value cites; the item keeps the full trace
            retrieval_trace=[
                h.model_copy(update={"content": ""})
                for h in hits
                if h.chunk_id in {r.jrc_database_id for r in references}
            ],
        ),
    )


def run_parameter(
    cfg: WorkflowConfig,
    tracer: Tracer,
    record: ParameterRecord,
    as_of: date,
    force: bool = False,
    parameter_ref: str | None = None,
    enqueue: bool = True,
) -> ReviewItem:
    """Run the full workflow for one parameter record; returns the queue item.

    `record` comes from the params DB (`paramdb.load_record` /
    `load_group_record`) — never from a file. `parameter_ref` is what the run
    was asked for (`euromod://…` or `group:<id>`; defaults to the record's
    model_target) and travels on the item. With `enqueue=False` the item is
    returned but not written to params.review_queue: the evaluation pipeline
    scores items without ever touching the review queue.
    """
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
                "parameter_ref": parameter_ref or info.model_target,
                "as_of": as_of,
                "run_id": run_id,
                "phoenix_trace_id": phoenix_trace_id,
                "force": force,
                "enqueue": enqueue,
            }
        )
        set_output(span, {"routing": result["routing"], "item_id": result["item"].id})
    item: ReviewItem = result["item"]
    paramdb.record_run_safe(
        cfg, item, PROMPT_VERSION, AGENT_VERSION, started_at, datetime.now(timezone.utc)
    )
    return item
