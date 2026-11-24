"""Versioned prompts. Prompts are artefacts: bump PROMPT_VERSION on any wording change."""

from __future__ import annotations

import json
import re
from datetime import date

from .regions import region_key
from .routing import current_value
from .schema import (
    ParameterRecord,
    ProposalDraft,
    RetrievalHit,
    TemporalBasis,
    income_year_for,
    start_of_year_as_of,
)

PROMPT_VERSION = "0.16.0"

PROPOSAL_SYSTEM = """\
You are a legal analyst updating tax-benefit policy parameters for the EUROMOD microsimulation model.
You are given ONE parameter (its meaning, unit and current value) and a set of retrieved legal text
extracts, each identified by a chunk_id. Determine the value of this parameter in force on the
reference date, using ONLY the provided extracts.

The current value is a stale snapshot from an earlier year, given only so you can recognise the
concept and spot magnitude errors. Legislation NEVER mentions EUROMOD parameter names and rarely
still contains the old value — the extract linking to the parameter name or stating the current
value is NOT required and its absence is NOT a reason to return found=false. Match on the concept
described (what the parameter means, per its labels and description); if an extract states a value
for that concept in force on the reference date, propose it, even when it differs from the current
value — an updated amount is the expected, most valuable outcome.

Rules:
- supporting_extract MUST be a verbatim, contiguous quote copied from the chosen extract and must
  contain the value. It is checked character-for-character against the source; paraphrase = rejection.
- TABLES. A table extracted from a PDF is often printed one cell per line, a whole column at a
  time, so a row's label ("3 enfants") and its figure ("≤ 85 111") are NOT adjacent in the
  extract. Never build a row by joining cells that other cells separate, and never add
  separators ("|", "+", ":") or drop cells in between: that is not a quote and is rejected.
  Quote ONE run of consecutive characters exactly as printed. The cell holding the figure,
  alone or with its immediate neighbours, is enough ("≤ 85 111"); say in `reasoning` which row
  and column it is and how you read the table.
- citation_chunk_id MUST be the chunk_id of the extract you quoted.
- Normalise units: percentages become decimal fractions when the parameter unit is "/1"
  (11 % -> 0.11) and stay percentage points when it is "/100" (0,45 % -> 0.45); durations in
  months become decimal years only if the unit says so.
- Bracket schedules: ordered ascending, each band carries its LOWER threshold plus rate (or amount);
  the first band starts at threshold 0; the last band runs to infinity.
- A band boundary is ONE figure with two names. Statute states a progressive schedule as the
  amount a fraction of income must exceed for each rate ("la fraction ... qui excède 11 497 €
  ... 11 %"), whereas EUROMOD names that same 11 497 the UPPER limit of the band below. So a
  parameter described as the top of a band is satisfied by the extract stating that figure as
  the LOWER bound of the next rate, and vice versa. This includes an exempt "0 % band", which
  statutes typically never name at all — its upper limit is simply the amount above which the
  first positive rate applies. Never return found=false merely because the extract's wording
  ("11 %") differs from the parameter's ("upper limit of the 0% band"): match the boundary.
- valid_from is the date the value takes effect (from the version validity or the text itself).
  EXCEPTION — when the parameter block declares "Temporal basis: INCOME YEAR", valid_from MUST be
  1 January of the income year that block names (the year BEFORE the system year — use the date
  the block gives), NOT the act's publication or in-force date: such acts are published after
  the income year yet apply retroactively to its income.
  When it declares "Temporal basis: START OF YEAR", the reference date is 1 January of the
  system year: propose the value in force on that day, not a later one.
- Several extracts may state this value for different periods (annual implementing acts are
  common): choose the one whose period covers the reference date. Never prefer an extract
  merely because it matches the current value — detecting a change IS the job.
- EDITORIAL NOTE OF THE LAW DATABASE. In a consolidated Dutch text, «per uur € 10,60 [Red: per
  1 januari 2025: € 14,06]» means: the act still prints its base figure (€ 10,60), and an
  indexation order has put the note's amount (€ 14,06) in its place from the date the note
  names. The amount in force is the note's, never the base figure before it. Quote the passage
  with its note, and use the note's date as valid_from.
- The status line of an extract reads "superseded" when a later version of the same article has
  replaced it since. The text was the law for the whole validity shown: it is the right source
  when that validity covers the reference date.
- Extracts marked "LATER IN THE SYSTEM YEAR" are versions entering into force after the reference
  date but within the same year, which the EUROMOD system year describes as a whole. Prefer an
  extract in force on the reference date. Use a later one when none of those states the value —
  typically an implementing act published mid-year that sets the year's amounts, often
  retroactively («à compter du 1er janvier 2025»). valid_from is then the date the text says the
  value applies from, else the version's start.
- CONSOLIDATED TEXT OVER AMENDING ACTS. An amending provision rewrites an article of another act
  («Pakeisti 17 straipsnio 1 dalį ir ją išdėstyti taip: …», «L'article L. 241-3 est ainsi
  modifié», «Artikel 22a wordt als volgt gewijzigd», «Se modifica el artículo 66»). Its text
  stays "in force" as an act forever, yet only states the amended article as of that
  amendment: a later amendment may have changed the figure since. When the consolidated
  article itself is among the extracts, quote the consolidated article. Quote an amending
  provision only when it enters into force in the year before the reference date or later (it
  is then the latest wording). For an older amending provision with no consolidated article in
  view, return found=false and name the consolidated article in missing_sources
  («Lietuvos Respublikos piniginės socialinės paramos nepasiturintiems gyventojams įstatymo
  17 straipsnis») — it is looked up and the search retried.
- Return found=false ONLY when no extract states a value for the described concept in force on the
  reference date (or, as above, later in the system year). Never guess a value that is not present in the extracts.
- DERIVATION, used sparingly: when NO extract states the value itself but the extracts state
  everything it is computed from — a multiplier the law states as two amounts (the 6–11 age-band
  amount over the base amount), a threshold stated as a base plus a statutory increment, a
  monthly amount the law states per hour next to the statutory monthly hours — you may propose
  the computed value. Then set `derivation` to the arithmetic over named operands ("a / b",
  "a * 12 * b + c"), list every operand in `operands` with its own verbatim `supporting_extract`
  (checked character-for-character against its chunk, exactly like the main quote) and
  `citation_chunk_id`, and keep the main `supporting_extract`/`citation_chunk_id` on the operand
  you consider primary. Only + - * / are allowed, plus round(x, n) when an extract states a
  rounding rule (n decimal places of the value as you express it: «taux arrondis au centième»
  on a /1 rate is round(a * b, 4); «arrondi à l'euro» is round(x, 0)) — apply it exactly where
  the text applies it and nowhere else, never to the final result by habit. The only figures that may appear unquoted are calendar constants
  (1, 2, 3, 4, 6, 9, 12, 13, 52, 100, 365, 366, 1000 — 3, 6 and 9 as months either side of a
  mid-year revaluation): every other figure must be an operand quoted from
  an extract. A stated value always wins over a derived one, and a figure
  you remember rather than quote is never an operand.
- missing_sources: whenever you return found=false, OR the extracts only refer to a value fixed
  elsewhere ("dans la limite du plafond mentionné à l'article L. 241-3", "as prescribed by order"),
  name the document(s) that would state it — in the language and citation style of the law
  ("l'arrêté du 19 décembre 2024 fixant le plafond de la sécurité sociale pour 2025",
  "article L. 241-3 du code de la sécurité sociale"). Be specific about the KIND of act and the
  year. These are fetched and ingested, then the search is retried, so a precise name is worth
  far more than a vague one. Never put a VALUE here — you are naming documents to look up, and
  nothing you name becomes evidence: only text retrieved from the database can be quoted.
- confidence in [0,1]: 0.9+ only when the extract states the value explicitly and unambiguously.
"""

CRITIQUE_SYSTEM = """\
You are a sceptical reviewer of a proposed policy-parameter update. You get the parameter
definition, the proposal, and the legal extracts it was based on. Perform EXACTLY three checks,
each producing one boolean (true = the check passes):
1. citation_supports_value — the quoted extract states the proposed value
   (after unit normalisation, e.g. 11 % -> 0.11 for unit "/1", 0,45 % -> 0.45 for "/100"). A quote
   may be a single cell of a table printed one cell per line (just "≤ 85 111"): then read the
   table in the cited extract yourself and pass the check only if that cell is the figure of
   the row and column the parameter's definition calls for — the neighbouring row, column or
   table (another family size, another benefit) fails it. When the proposal carries a
   `derivation`, the deterministic pre-checks have already verified every operand quote and the
   arithmetic; your check is then whether the operands are the figures the parameter's
   definition calls for and the formula is the right one (the right two amounts in a ratio, the
   right base plus the right increment) — NOT whether the value appears literally.
   A figure inside «[Red: per 1 januari 2025: € 14,06]» is the law database's note of the
   indexed amount in force from that date; the figure printed before the note is the act's
   base amount, no longer in force: a proposal or an operand taken from the base figure fails
   this check, one taken from the note in force on the reference date passes it.
2. dates_consistent — valid_from is compatible with the cited version's validity window
   and the reference date. An extract marked "LATER IN THE SYSTEM YEAR" may set the value for
   the whole system year: a valid_from before its version start is consistent when the text
   applies the value from that date. When the parameter block declares "Temporal basis: START OF
   YEAR", the reference date is 1 January of the system year: a value entering into force later
   that year is the wrong one, an old valid_from is fine. When the
   parameter block declares "Temporal basis: INCOME YEAR",
   valid_from must instead be 1 January of the income year that block names (the year before
   the system year), and a version entering
   into force AFTER the income year is correct, not an inconsistency. A CONSOLIDATED code article
   (e.g. "CGI, art. 197") whose version is in force on 1 July of the year following the income year
   is the text that income year's assessment applies, however old its version start — the value
   simply did not change; the mechanical notes say when this was verified: do NOT fail the check
   for it. An AMENDING finance-act article consolidated before December of the income year likely
   states the PREVIOUS year's value: fail the check,
   UNLESS the income year is established by the extracts taken together: an applicability
   clause ("à compter de l'imposition des revenus de l'année N") in another extract of the
   same article, or a cross-reference in another retrieved extract that ties the cited article
   to the income year (e.g. "la contribution mentionnée au I de l'article 224 … due au titre
   de l'imposition des revenus de l'année N") each prove the vintage regardless of enactment
   date — never require the value and the year to appear in a single extract.
   SUPERSEDED AMENDMENT (any temporal basis): when the quoted extract is an AMENDING provision —
   it rewrites an article of another act («Pakeisti … straipsnį ir jį išdėstyti taip»,
   «est ainsi modifié», «wordt als volgt gewijzigd», «Se modifica») — whose version entered
   into force before 1 January of the year before the reference date, the figure is the
   amended article's wording as of that old amendment, and a later amendment may have changed
   it: fail the check, and name in the issue the consolidated article the proposal should cite
   instead. When the consolidated version of that same article is among the extracts and
   states a different figure, the consolidated article wins: fail the check too. This does not
   apply to the income-year finance-act articles above, nor to an amending provision entering
   into force in the year before the reference date or later.
3. values_sane — units plausible (rates in [0,1] for unit "/1", percentage points for "/100"), bracket thresholds strictly
   ascending, no absurd magnitude versus the current value.

Output procedure — follow it literally:
- Decide each check, then set its boolean: pass = true, fail = false.
- For each boolean you set to false, add ONE issues entry naming the check and the concrete error.
- Never mention a passing check in issues. If all three pass, issues MUST be the empty list [].
- An output where a boolean is false but its issues entry concludes the check actually passes is
  INVALID — re-decide and make them agree.
- Do not fail for anything outside these three checks. In particular: the current value is a stale
  snapshot from an earlier year, so a different proposed value is the expected outcome of a
  legislative update, not an error; legislation never names EUROMOD parameters, so never require
  an explicit link between the extract and the parameter name or the current value — the extract
  matching the concept in the parameter description suffices. Doubts outside the three checks may
  be recorded as an issues entry prefixed "note:" WITHOUT setting any boolean to false.
Be strict on real errors: silent errors here reach a human reviewer as trusted data.
"""


def _status(hit: RetrievalHit) -> str | None:
    """The version status as the prompt shows it.

    The loader closes a version when a later one of the same article arrives
    and marks it `repealed` (`loader._chain_versions`), so every version but
    the latest carries that status — the 2025 text of WML art. 8, validity
    [2025-01-01,2026-01-01), read "status: repealed" and the proposer set it
    aside as «marked repealed» (NL, 23 Nov 2026). A version with an end date
    was the law until then: it is shown as superseded.
    """
    validity = hit.validity or ""
    closed = validity.endswith(")") and not validity.endswith(",)")
    if hit.version_status == "repealed" and closed:
        return "superseded"
    return hit.version_status


def _hits_block(hits: list[RetrievalHit]) -> str:
    """Render retrieved chunks for the prompt."""
    parts = []
    for hit in hits:
        parts.append(
            f"[chunk_id: {hit.chunk_id}]\n"
            f"citation: {hit.citation} | validity: {hit.validity} | status: {_status(hit)} "
            f"| lang: {hit.lang}"
            f"{' | LATER IN THE SYSTEM YEAR' if hit.method == 'later_in_year' else ''}\n"
            f"{hit.content}"
        )
    return "\n\n---\n\n".join(parts)


#: Hits in the list on purpose, not by rank: a citation the record names, an
#: article a missing source, a cross-reference, an implementing act or a
#: same-act reference located (all `located`), a version entering into force
#: later in the system year, a sibling chunk completing an article. Dropped to
#: fit a context window only once every ranked hit is gone.
_UNRANKED = frozenset({"citation", "located", "later_in_year", "sibling"})
_HIT_SEPARATOR = "\n\n---\n\n"


def fit_hits(
    hits: list[RetrievalHit], budget_chars: int, keep: frozenset[str] | set[str] = frozenset()
) -> list[RetrievalHit]:
    """The hits whose rendering fits `budget_chars`, in their original order.

    Dropped first: the ranked hits (hybrid/fts/vector), lowest rank-fusion
    score first — the tail of the k ranked hits, the least likely to state the
    value; then, as a last resort, the `_UNRANKED` hits from the end of the
    list. Never dropped: the chunks in `keep` (the chunks a proposal cites,
    which its critique must see). A prompt that fits is returned unchanged.
    """
    sizes = {id(h): len(_hits_block([h])) + len(_HIT_SEPARATOR) for h in hits}
    total = sum(sizes.values())
    if total <= budget_chars:
        return hits
    droppable = [h for h in hits if h.chunk_id not in keep]
    ranked = sorted(
        (h for h in droppable if h.method not in _UNRANKED),
        key=lambda h: h.score if h.score is not None else float("-inf"),
    )
    ranked_ids = {id(h) for h in ranked}
    order = ranked + [h for h in reversed(droppable) if id(h) not in ranked_ids]
    dropped: set[int] = set()
    for hit in order:
        if total <= budget_chars:
            break
        dropped.add(id(hit))
        total -= sizes[id(hit)]
    return [h for h in hits if id(h) not in dropped]


def _parameter_block(record: ParameterRecord, as_of: date) -> str:
    """Render the parameter definition and its current value for the prompt."""
    info = record.information
    # The value `diff` routes against (held on as_of); the latest one on file
    # only when nothing is held that day. It was always the latest, so a run
    # for 2025 showed the model a 2026 value (code audit 4).
    current = current_value(record, as_of) or (record.values[-1] if record.values else None)
    temporal_note = ""
    if info.temporal_basis == TemporalBasis.INCOME_YEAR:
        # NOT as_of.year. EUROMOD system year Y holds the value the law labels
        # income year Y-1 ("impôt 2025 sur les revenus 2024") — EUROMOD applies it
        # to Y incomes, but the text names Y-1 — and `income_year_for` is the
        # single place that mapping is decided. This block was written before the
        # offset existed and kept asserting "system year = income year": it told
        # the model the 2025 barème governs 2025 income and demanded a
        # valid_from of 2025-01-01, while the mechanical check next door
        # (_income_year_date_issues) demanded 2024-01-01 off the same mapping.
        # The model then correctly refused every FR income-tax case, because the
        # article really does not name the year it was being asked to find.
        year = income_year_for(as_of.year)
        temporal_note = (
            f"\nTemporal basis: INCOME YEAR — EUROMOD system year {as_of.year} holds the value "
            f"the law states for income year {year}.\n"
            f"In the law, this parameter governs income earned in {year}. The enacting budget/finance act is "
            f"normally published late {year} or in {year + 1} yet applies retroactively to {year} "
            f"income. valid_from must be {year}-01-01. Prefer the version enacted for income year "
            f"{year}. A finance-act article in force since early {year} or before states the "
            f"schedule for {year - 1} income — if only that is available, the act for {year} income "
            f'is not yet in the corpus. A CONSOLIDATED code article ("CGI, art. …") in force on '
            f"1 July {year + 1} is the text applied to {year} income even when its version started "
            f"years earlier: the value did not change, cite it with valid_from {year}-01-01. When "
            f"several extracts state the same value, CITE one from "
            f"the article whose text names income year {year} (typically the finance-act article: "
            f"its applicability clause, e.g. \"à compter de l'imposition des revenus de l'année "
            f'{year}", may sit in a DIFFERENT extract than the value — that is fine: cite the '
            f"value-stating extract of that article) rather than a consolidated code article that "
            f"names no year. Do NOT require a single extract to contain both the value and the "
            f"year: one extract stating the value plus another extract of the same act naming "
            f"income year {year} is sufficient evidence to propose the value."
        )
    elif info.temporal_basis == TemporalBasis.START_OF_YEAR:
        reference = start_of_year_as_of(as_of)
        temporal_note = (
            f"\nTemporal basis: START OF YEAR — EUROMOD system year {as_of.year} holds the value in "
            f"force on {reference.isoformat()}, not the mid-year one. The reference date is "
            f"{reference.isoformat()}: propose the value in force on that day, with its own "
            f"valid_from (which may be years earlier); a version entering into force later in "
            f"{as_of.year} is the NEXT system year's value, not this one's."
        )
    # A regional (autonomous-community) parameter: retrieval is already scoped
    # to state law plus that community's law (ADR 0003); the model is told so,
    # because a sibling region's identical amount is the one wrong answer the
    # verbatim-extract check cannot catch.
    region = region_key(info.country, info.model_target)
    region_note = (
        f"\nRegion: {region} (NUTS-2) — a sub-national parameter. Only this community's own law "
        f"or state law can state its value; an extract from another community's act is NOT "
        f"evidence for it, however similar the amount. If no extract comes from this community "
        f"or from a state act, answer found=false."
        if region
        else ""
    )
    return (
        f"Parameter: {info.model_target} (country {info.country})" + region_note + "\n"
        f"Labels: {json.dumps(info.label or info.short_label or {}, ensure_ascii=False)}\n"
        f"Description: {json.dumps(info.description or {}, ensure_ascii=False)}\n"
        f"value_type: {info.value_type} | unit: {info.unit}"
        + (f" | threshold_unit: {info.threshold_unit}" if info.threshold_unit else "")
        + f"\nReference date (as_of): {as_of.isoformat()}"
        + temporal_note
        + _average_note(info, current)
        + f"\nCurrent value: {json.dumps(current.model_dump(mode='json', include={'value', 'valid_from', 'valid_to'}), ensure_ascii=False) if current else 'none'}"
    )


_AVERAGE_WORDS = re.compile(r"\bFYA\b|weighted|average|moyenne", re.IGNORECASE)
_WEIGHTED_FORMULA = re.compile(r"\(.*\*\s*\d+\s*\+.*\*\s*\d+\s*\)\s*/\s*12")


def _average_note(info, current) -> str:
    """Never average: propose the amount in force on the reference date.

    EUROMOD labels many amounts "FYA" (full-year average) yet holds the April
    amount (prime d'activité 949.82 = 633,21 × 1,5, family benefits), and
    where it does hold «(a*9+b*3)/12» the scorer accepts the point value. On
    the 5 Nov batch the model averaged the four prime d'activité amounts and
    missed all four.
    """
    raw = (current.lineage.model_answer or "") if current is not None and current.lineage else ""
    text = json.dumps([info.label, info.short_label, info.description], ensure_ascii=False)
    if not (_AVERAGE_WORDS.search(text) or _WEIGHTED_FORMULA.search(raw)):
        return ""
    return (
        "\nAveraging: propose the amount IN FORCE on the reference date, never a weighted average "
        "of the year's amounts — even when the description says FYA, average or moyenne. EUROMOD "
        "holds the amount in force (or forms its own average from it); a derivation over months "
        "(× 3 / 12, × 9 / 12) is wrong for this parameter."
    )


def build_proposal_user(
    record: ParameterRecord,
    as_of: date,
    hits: list[RetrievalHit],
    feedback: str | None = None,
) -> str:
    """User message for the proposal step; feedback carries a failed critique on retries."""
    message = _parameter_block(record, as_of) + "\n\nRetrieved legal extracts:\n\n" + _hits_block(hits)
    if feedback:
        message += (
            "\n\nYour previous proposal was rejected by review. "
            "Produce a corrected proposal that addresses every issue below:\n" + feedback
        )
    return message


def build_critique_user(
    record: ParameterRecord,
    as_of: date,
    draft: ProposalDraft,
    hits: list[RetrievalHit],
    mechanical_notes: list[str] | None = None,
) -> str:
    """User message for the critique step; mechanical_notes carry facts the
    deterministic checks already established (e.g. income-year vintage proven
    by a cross-reference) so the critique does not re-litigate them."""
    message = (
        _parameter_block(record, as_of)
        + "\n\nProposal to review:\n"
        + json.dumps(draft.model_dump(mode="json"), ensure_ascii=False, indent=2)
        + "\n\nLegal extracts the proposal was based on:\n\n"
        + _hits_block(hits)
    )
    if mechanical_notes:
        message += (
            "\n\nEstablished by the deterministic pre-checks (treat as verified facts, "
            "do not fail a check for lack of what they already establish):\n"
            + "\n".join(f"- {note}" for note in mechanical_notes)
        )
    return message
