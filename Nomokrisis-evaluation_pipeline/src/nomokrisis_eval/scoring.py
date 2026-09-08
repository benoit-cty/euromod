"""Deterministic scoring of a workflow ReviewItem against a GoldenCase.

Pure functions only — no LLM judge in v1. KPI semantics follow
04_activity4_validation.md:

  routing_correct   changed / unchanged / new / not_found / national_team_source
  value_correct     normalised match (scalars, see below) or structure+cell match (brackets)
  date_correct      proposed valid_from == expected valid_from. NOT scored when both
                    sides route `unchanged`: there the pipeline keeps EUROMOD's own
                    validity window by design, which is a different quantity from the
                    date the law made the value effective.
  citation_correct  pinpoint citation matches one of the accepted citations
  extract_verbatim  the cited chunk contains the supporting_extract character-for-
                    character. Purely mechanical — no LLM has a say in it.
  supportedness     extract_verbatim AND the critique model's judgement that the
                    extract supports the value. LLM-assisted: only comparable across
                    models when the run pinned a fixed critique model.
  critique_pass     the critique's overall verdict (dates, units, sanity).
  rejected          a value was proposed and the critique failed it: routing/value/
                    date are then scored False whatever the routing says.
  hallucination     a value was proposed whose extract is not verbatim in the cited
                    chunk — the mechanical leg alone, so a critique that failed on
                    dates or units is not reported as a hallucination.
  abstained         no proposal on a case that has a ground-truth value: the pipeline
                    refused rather than guessed. Still scores False on value/date/
                    citation, but the flag keeps refusals distinguishable.
  retrieval_hit     the ground-truth citation appears in the retrieval trace (recall@k)

Value comparison never string-matches raw EUROMOD strings. Either side may be a
raw value ("11496#y", the FYA average "(1766.92*10+1801.80*2)/12#m", the
cross-reference "$PSS * 4"); both sides are normalised first — arithmetic
evaluated, percent literals divided ('4.1%' is the same rate as 0.041 — EUROMOD
spells some rates that way, OpenFisca never does), $constants resolved against a
caller-supplied map, the period suffix
converted to the monthly basis when the two sides state different periods. The
tolerance is relative 1e-6: wide enough for float noise and period conversion,
tight enough that a 1 € discrepancy on a 11 496 € threshold (the FR 2025 barème
erratum, ~9e-5 relative) still scores as a difference.
"""

from __future__ import annotations

import ast
import re
from collections.abc import Mapping
from dataclasses import dataclass
from math import isclose

from nomoscope_workflow.schema import Bracket, ReviewItem, Routing

from .schema import CaseResult, GoldenCase

_NORM_RE = re.compile(r"[\s. ,;:'’-]+")


def _norm(text: str) -> str:
    return _NORM_RE.sub("", text).casefold()


def citation_matches(expected: str, candidate: str | None) -> bool:
    """True when `candidate` cites at least what `expected` names.

    Containment in ONE direction only: the expected citation must appear inside
    the candidate, never the reverse. An instrument-level expectation is meant
    to be satisfied by a pinpoint ("JORFTEXT000051393142" by
    "JORFTEXT000051393142, art. 1"), but the reverse — accepting "CGI, art. 19"
    for an expected "CGI, art. 197" — would credit a citation of a different
    article.

    The match is also anchored on digits: a run of digits may not be cut in
    half, so "CGI, art. 197" does not claim "CGI, art. 1975" and "art. 197"
    does not claim "art. 1197". Everything else stays loose on purpose —
    punctuation, case and separators are normalised away first, so
    "CGI, art. 197" matches "cgi art 197" and matches inside a retrieval
    context header.
    """
    if not candidate:
        return False
    a, b = _norm(expected), _norm(candidate)
    if not a:
        return False
    start = b.find(a)
    while start != -1:
        before = b[start - 1] if start else ""
        after = b[start + len(a)] if start + len(a) < len(b) else ""
        if not (before.isdigit() and a[0].isdigit()) and not (
            after.isdigit() and a[-1].isdigit()
        ):
            return True
        start = b.find(a, start + 1)
    return False


def citation_equal(expected: str, candidate: str | None) -> bool:
    """Punctuation/case-insensitive equality — no containment, so 'art. 2' never
    claims 'art. 20'. Rank scoring (embedding eval) needs this strictness."""
    if not candidate:
        return False
    a = _norm(expected)
    return bool(a) and a == _norm(candidate)


# ---------------------------------------------------------------------------
# EUROMOD raw-value normalisation (FR_parameter_matching.md §1.1–1.2)
# ---------------------------------------------------------------------------

#: EUROMOD period suffix -> factor converting the magnitude to the monthly
#: basis (the conversion table in FR_parameter_matching.md §1.1). '#c'
#: (capital) has no time basis; like '#m' it is left unconverted.
PERIOD_TO_MONTHLY: dict[str, float] = {
    "m": 1.0,
    "y": 1 / 12,
    "q": 1 / 3,
    "w": 4.34,
    "d": 30.5,
    "l": 21.73,
    "s": 26.07,
    "c": 1.0,
}

_SUFFIX_RE = re.compile(r"\s*#\s*([myqwdlsc])\s*$")
#: A percent literal anywhere in the expression ('4.1%', '100%*$MMS'). Rewritten
#: to a division so the arithmetic below sees a plain number.
_PERCENT_RE = re.compile(r"(\d+(?:\.\d+)?)\s*%")
_CONST_RE = re.compile(r"\$([A-Za-z_]\w*)")
_ALLOWED_BINOPS = (ast.Add, ast.Sub, ast.Mult, ast.Div)
_ALLOWED_UNARY = (ast.UAdd, ast.USub)

#: Relative tolerance for normalised comparisons. Must stay below ~9e-5 so the
#: FR 2025 barème's 1-€-below-the-law thresholds keep scoring as differences.
_REL_TOL = 1e-6


@dataclass(frozen=True)
class NormalisedValue:
    """A numeric magnitude plus the period basis its raw form stated, if any."""

    magnitude: float
    period: str | None = None  # 'm', 'y', … (no '#'); None = basis unstated

    def monthly(self) -> float:
        return self.magnitude * PERIOD_TO_MONTHLY.get(self.period or "m", 1.0)


def _eval_expr(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _eval_expr(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.BinOp) and isinstance(node.op, _ALLOWED_BINOPS):
        left, right = _eval_expr(node.left), _eval_expr(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        return left / right
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, _ALLOWED_UNARY):
        operand = _eval_expr(node.operand)
        return operand if isinstance(node.op, ast.UAdd) else -operand
    raise ValueError(f"unsupported expression node: {ast.dump(node)}")


def normalise_value(
    value,
    constants: Mapping[str, object] | None = None,
    _resolving: frozenset[str] = frozenset(),
) -> NormalisedValue | None:
    """Normalise a scalar to (magnitude, period), or None when it has neither.

    Accepts plain numbers and raw EUROMOD strings: an optional trailing period
    suffix ('#m', '#y', …) over an arithmetic expression that may reference
    other parameters ('$PSS * 4'), with percent literals read as the rate they
    denote ('4.1%' -> 0.041, '100%*$MMS' -> the value of $MMS). References
    resolve through `constants`
    (casefolded name without '$' -> number or raw string, resolved recursively
    with a cycle guard); a reference's own period suffix is dropped — EUROMOD
    formulas operate on the stored magnitude. Returns None for 'n/a', unknown
    constants, multiplicative unit suffixes ('×1000'), a period marker inside an
    expression ('242#w*$sw_weeks') or anything else that is not a scalar —
    callers then fall back to strict equality.
    """
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return NormalisedValue(float(value))
    if not isinstance(value, str):
        return None

    text = value.strip()
    period = None
    if m := _SUFFIX_RE.search(text):
        period = m.group(1)
        text = text[: m.start()].strip()
    if not text or text.casefold() in ("n/a", "na"):
        return None
    # A '#' that survived the suffix strip is a period marker inside the
    # expression ('242#w*$sw_weeks'). It is NOT arithmetic this function can
    # read, and leaving it in is actively dangerous: '#' opens a comment in
    # Python's grammar, so ast.parse would silently evaluate the prefix and
    # return 242 for a value that means 242 a week. Refuse instead, and let the
    # caller fall back to strict equality.
    if "#" in text:
        return None
    # EUROMOD stores some rates as percent literals ('4.1%', '8.72%') where
    # OpenFisca and the rest of the store use the unit-/1 form (0.041), and
    # writes some values as a percentage OF another parameter ('100%*$MMS').
    # Both spellings denote the same quantity, so rewrite every percent literal
    # to a division and let the expression evaluator do the rest: without this
    # the two sides fall back to string equality and a correct value scores as
    # a difference.
    text = _PERCENT_RE.sub(r"((\1)/100)", text)

    def substitute(match: re.Match[str]) -> str:
        name = match.group(1).casefold()
        if name in _resolving:
            raise ValueError(f"circular $-reference: {name}")
        resolved = (constants or {}).get(name)
        if resolved is None:
            raise ValueError(f"unknown constant: ${match.group(1)}")
        inner = normalise_value(resolved, constants, _resolving | {name})
        if inner is None:
            raise ValueError(f"unresolvable constant: ${match.group(1)}")
        return f"({inner.magnitude!r})"

    try:
        text = _CONST_RE.sub(substitute, text)
        magnitude = _eval_expr(ast.parse(text, mode="eval"))
    except (ValueError, SyntaxError, ZeroDivisionError):
        return None
    return NormalisedValue(magnitude, period)


def _num_equal(x: float | None, y: float | None) -> bool:
    if x is None or y is None:
        return (x is None) == (y is None)
    return isclose(x, y, rel_tol=_REL_TOL, abs_tol=1e-9)


def values_equal(a, b, constants: Mapping[str, object] | None = None) -> bool:
    """Scalar/bool/str/bracket-schedule comparison after normalisation.

    Scalars compare as normalised magnitudes; when both sides state a period
    suffix and the periods differ, both convert to the monthly basis first (a
    bare number carries the parameter's own storage basis, so no conversion is
    guessed for it). Values that normalisation cannot read fall back to strict
    equality.
    """
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_brackets_equal(x, y) for x, y in zip(a, b))
    if isinstance(a, bool) or isinstance(b, bool):
        return a == b
    na, nb = normalise_value(a, constants), normalise_value(b, constants)
    if na is not None and nb is not None:
        if na.period and nb.period and na.period != nb.period:
            return _num_equal(na.monthly(), nb.monthly())
        return _num_equal(na.magnitude, nb.magnitude)
    return a == b


def _brackets_equal(a: Bracket, b: Bracket) -> bool:
    def eq(x: float | None, y: float | None) -> bool:
        return _num_equal(x, y)

    return eq(a.threshold, b.threshold) and eq(a.rate, b.rate) and eq(a.amount, b.amount)


def score_item(
    case: GoldenCase,
    item: ReviewItem,
    constants: Mapping[str, object] | None = None,
) -> CaseResult:
    """Score one case. `constants` feeds $-reference resolution in values_equal
    (casefolded constant name -> value in force for the case's country)."""
    expected = case.expected
    proposed = item.proposed_value

    result = CaseResult(
        case_id=case.id,
        country=case.country,
        language=case.language,
        model_target=item.model_target,
        difficulty=case.difficulty,
        hazards=list(case.hazards),
        source_class=case.source_class,
        routing_expected=expected.routing.value,
        routing_actual=item.routing.value,
        routing_correct=item.routing == expected.routing,
        item_id=item.id,
        phoenix_trace_id=item.phoenix_trace_id,
        confidence=(
            proposed.lineage.confidence if proposed is not None and proposed.lineage else None
        ),
        expected_value=_dump(expected.value),
        proposed_value=_dump(proposed.value) if proposed is not None else None,
        corpus_available=case.corpus_available,
        readiness=case.readiness,
        guidance_only=item.guidance_only,
    )

    if expected.value is not None:
        result.value_correct = proposed is not None and values_equal(
            proposed.value, expected.value, constants
        )

    # The date leg is only meaningful when the pipeline is dating a change.
    # On an `unchanged` verdict `pipeline._unchanged_window` deliberately keeps
    # the validity window EUROMOD already holds — the citation re-confirms the
    # value, it does not restart it — while the golden `valid_from` is the date
    # the LAW made that value effective. EUROMOD's windows are system-year rows
    # (2025-01-01, or an untouched 2013-01-01), so the two agree only by
    # coincidence: comparing them scored a correct no-change verdict as a date
    # error. Both sides routing `unchanged` therefore leaves the leg unscored.
    both_unchanged = expected.routing == Routing.UNCHANGED == item.routing
    if expected.valid_from is not None and not both_unchanged:
        result.date_correct = proposed is not None and proposed.valid_from == expected.valid_from

    # The evidence legs are only meaningful when the pipeline is looking for
    # evidence. On a `derived` verdict `pipeline._derived_refs` short-circuits to
    # the anchor parameter BEFORE retrieval and before any LLM call — a value
    # like "$PSS * 4" has no independent legislative existence, so there is
    # deliberately no proposal, no citation and an empty retrieval trace. Scoring
    # those as misses penalises the pipeline for doing exactly what it should,
    # the same way comparing validity windows penalised a correct `unchanged`.
    # Both sides routing `derived` therefore leaves citation and recall unscored;
    # a case where only ONE side says `derived` still scores both, because then
    # the routing itself is in dispute and the evidence is what settles it.
    both_derived = expected.routing == Routing.DERIVED == item.routing
    if expected.citations and not both_derived:
        result.citation_correct = proposed is not None and any(
            citation_matches(exp, ref.title)
            for exp in expected.citations
            for ref in proposed.references
        )
        result.retrieval_hit = any(
            citation_matches(exp, hit.citation) or citation_matches(exp, hit.context_header)
            for exp in expected.citations
            for hit in item.retrieval_trace
        )

    if proposed is not None:
        critique = item.critique
        # Mechanical only: `extract_offsets` is set by the verbatim check in
        # pipeline.critique and is never touched by the LLM leg, whereas
        # `citation_verified` is that check ANDed with the critique model's
        # `citation_supports_value`. Hallucination — a value presented with an
        # extract that is not in the cited text — is the mechanical one.
        verbatim = bool(critique and critique.extract_offsets is not None)
        result.extract_verbatim = verbatim
        result.hallucination = not verbatim
        result.supportedness = bool(critique and critique.citation_verified)
        result.critique_pass = critique.verdict == "pass" if critique else None
        # The pipeline routes on the value even when its critique rejected the
        # proposal (see CaseResult.rejected): a stale value re-proposed with a
        # citation the critique refused would otherwise score a correct
        # `unchanged`. What the pipeline does not stand behind cannot be
        # credited on routing, value or date; the evidence legs above keep
        # scoring, since they describe the rejected proposal itself.
        if critique is not None and critique.verdict == "fail":
            result.rejected = True
            result.routing_correct = False
            if result.value_correct is not None:
                result.value_correct = False
            if result.date_correct is not None:
                result.date_correct = False
    elif expected.value is not None:
        # No proposal where ground truth has a value: an abstention, not a
        # wrong answer. It still scores False on value/date/citation, so keep
        # the flag to tell "refused to guess" apart from "guessed wrong".
        result.abstained = item.routing == Routing.NOT_FOUND

    return result


def _dump(value):
    if isinstance(value, list):
        return [b.model_dump(exclude_none=True) if isinstance(b, Bracket) else b for b in value]
    return value
