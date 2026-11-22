"""Derived values: arithmetic over quoted operands, checked like an extract.

The strict AST evaluator, the operand checks (each operand quoted verbatim,
through quotes.check_quote, and stating its own figure), the half-up rounding
to EUROMOD's held precision and the unit range check (split out of
pipeline.py, code audit 4).
"""

from __future__ import annotations

import ast
import math
import re
from decimal import ROUND_HALF_UP, Decimal

from . import idiom, quotes
from . import issues as issue_text
from .schema import ParameterValue, ProposalDraft, RetrievalHit
from .values import eval_arith

#: Figures a derivation may use without quoting them: calendar and scaling
#: constants (months, quarters, weeks, days in a year, percent, per mille).
#: 3, 6 and 9 are the months either side of an April, July or October
#: revaluation: a full-year average is (a * 3 + b * 9) / 12, and five
#: derivations of the 5 Nov run were refused for the bare 3 alone.
#: Everything else is a fact about the law and must be an operand quoted
#: verbatim from a retrieved chunk — that is what keeps a derived value inside


def round_half_up(value: float, digits: int) -> float:
    """Round half-up to `digits` decimals, as legal texts do (2.5 -> 3), via
    the exact decimal of the float's repr — the one rounding of this module."""
    return float(Decimal(repr(value)).quantize(Decimal(1).scaleb(-digits), rounding=ROUND_HALF_UP))


#: the anti-hallucination contract.
DERIVATION_CONSTANTS = frozenset({1.0, 2.0, 3.0, 4.0, 6.0, 9.0, 12.0, 13.0, 52.0, 100.0, 365.0, 366.0, 1000.0})
#: Most decimal places `round(x, n)` may keep. The precision is not a fact about
#: the law the way a figure is: it is the rounding rule the text itself states —
#: «Les taux ainsi appelés sont arrondis au centième» (AGIRC-ARRCO art. 36: 6,20 %
#: × 127 % = 7,874 % → 7,87 %), «arrondi à l'euro le plus proche».
DERIVATION_MAX_DIGITS = 8


def evaluate_derivation(expression: str, operands: dict[str, float]) -> float:
    """Evaluate `expression` over named operands.

    Raises ValueError for anything but + - * / over operand names and
    DERIVATION_CONSTANTS, plus `round(x, n)` with n an integer literal up to
    DERIVATION_MAX_DIGITS — no other calls, no attributes, no other literals.
    Rounding is half-up, as legal texts mean it (not Python's half-even).
    """
    try:
        tree = ast.parse(expression.strip(), mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"derivation is not an arithmetic expression ({exc.msg})") from None

    def leaf(node: ast.AST) -> float:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
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
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "round"
            and not node.keywords
        ):
            if len(node.args) != 2:
                raise ValueError("round takes exactly (expression, digits)")
            digits = node.args[1]
            if not (
                isinstance(digits, ast.Constant)
                and type(digits.value) is int
                and 0 <= digits.value <= DERIVATION_MAX_DIGITS
            ):
                raise ValueError(f"round's digits must be an integer literal from 0 to {DERIVATION_MAX_DIGITS}")
            return round_half_up(ev(node.args[0]), digits.value)
        raise ValueError("only + - * / and round(x, n) over operand names and calendar constants are allowed")

    def ev(node: ast.AST) -> float:
        # The one arithmetic evaluator (values.eval_arith) with the
        # derivation's whitelist as its leaves.
        return eval_arith(node, leaf)

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
        for number in (raw, *_table_cells(raw)):
            compact = re.sub(r"[\s\u00a0\u202f]", "", number)
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
    lowered = text.lower()
    figures.update(value for word, value in _NUMBER_WORDS.items() if re.search(rf"\b{word}\b", lowered))
    return figures


def _table_cells(run: str) -> list[str]:
    """A run of figures cut where one number visibly ends: «I 329,71 397,64
    449,43 65,21» (a PDF table row, arrêté du 27 sept. 2019 art. 7) is four
    amounts, not one. A number ends after its decimal part, or before a group
    that is not three digits; «1 801,80» stays one number."""
    cells: list[list[str]] = []
    for token in re.split(r"[\s\u00a0\u202f]+", run):
        joins = cells and not re.search(r"[.,]\d+$", cells[-1][-1]) and re.fullmatch(r"\d{3}(?:[.,]\d+)?", token)
        if joins:
            cells[-1].append(token)
        else:
            cells.append([token])
    return [" ".join(cell) for cell in cells] if len(cells) > 1 else []


#: Numbers the law spells out (idiom.NUMBER_WORDS, every language).
_NUMBER_WORDS = idiom.ALL_NUMBER_WORDS


def _extract_states(extract: str, value: float) -> bool:
    """Whether the extract states `value` — as such, or as a percentage (108 % for 1.08).

    A multiplier above 1 is also stated by its increase: «majoré de 50 %» is
    the 1.5 of a × 1.5 (four prime d'activité derivations of the 5 Nov batch
    were refused for writing it so rather than a × (1 + 0.5)).
    """
    targets = [value, value * 100]
    if value > 1 and re.search(r"major|augment|increase", extract, re.IGNORECASE):
        targets.append((value - 1) * 100)
    return any(
        math.isclose(figure, target, rel_tol=1e-9, abs_tol=1e-9)
        for figure in _figures_in(extract)
        for target in targets
    )


def _derivation_summary(draft: ProposalDraft, hits: list[RetrievalHit]) -> str:
    """«a / b with a = 347.83 (AKW, artikel 12), b = 286.45 (AKW, artikel 12)» — for the reviewer."""
    citations = {h.chunk_id: h.citation for h in hits}
    parts = [
        f"{op.name} = {op.value:g} ({citations.get(op.citation_chunk_id) or op.citation_chunk_id})"
        for op in draft.operands
    ]
    return f"{draft.derivation} with " + ", ".join(parts)


def _stating_passage(content: str, value: float, limit: int = 300) -> str | None:
    """The first sentence of `content` that states `value`, for a retry's feedback.

    Told only «operand b's extract does not state 730», the model quoted the
    same sentence of CSS D. 622-7 again; the figure is in another one («égal
    à 1/ 730e de la moyenne des revenus», $bhl_max_amt2, 5 Nov batch).
    """
    for sentence in re.split(r"(?<=[.;])\s+|\n+", content):
        sentence = sentence.strip()
        if sentence and _extract_states(sentence, value):
            return sentence if len(sentence) <= limit else sentence[:limit] + "…"
    return None


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
    # A schedule derives one of its figures (the AGIRC-ARRCO CET share a * b,
    # a threshold of 12 monthly ceilings): the result must be one of them,
    # exactly — a schedule's figures are not replaced by the result, so a
    # figure 0.1 % off its own arithmetic would reach the queue (round(x, n)
    # states a rounding). A scalar's typed figure may be 0.1 % off: the
    # result replaces it (_round_like_held).
    figures = (
        [f for band in draft.value_brackets for f in (band.threshold, band.rate, band.amount) if f is not None]
        if draft.value_brackets is not None
        else [draft.value_scalar]
        if draft.value_scalar is not None
        else []
    )
    if not figures:
        return ["derivation: no value to derive"], [], None
    if not draft.operands:
        return ["derivation: no operands quoted"], [], None
    issues: list[str] = []
    offsets: list[tuple[int, int] | None] = []
    values: dict[str, float] = {}
    for op in draft.operands:
        where = f"operand {op.name}"
        if op.name in values:
            issues.append(f"derivation: {where} is listed twice")
            offsets.append(None)
            continue
        values[op.name] = op.value
        # Same rule as the main citation (quotes.check_quote).
        check = quotes.check_quote(hits, op.citation_chunk_id, op.supporting_extract, verify)
        op.citation_chunk_id = check.chunk_id
        if check.status == "not_retrieved":
            issues.append(issue_text.operand_not_retrieved(op.name))
            offsets.append(None)
            continue
        offsets.append(check.offsets)
        if not check.verified:
            issues.append(issue_text.operand_not_verbatim(op.name))
            if check.hint:
                issues.append(issue_text.operand_hint(op.name, check.hint))
        elif not _extract_states(op.supporting_extract, op.value):
            issues.append(f"derivation: {where}'s extract does not state {op.value:g}")
            content = getattr(quotes.hit_by_id(hits, op.citation_chunk_id), "content", "") or ""
            stating = _stating_passage(content, op.value)
            if stating:
                issues.append(f"derivation: {where}: its chunk states {op.value:g} in «{stating}» — quote that")
    if issues:
        return issues, offsets, None
    try:
        result = evaluate_derivation(draft.derivation or "", values)
    except ValueError as exc:
        return [f"derivation: {exc}"], offsets, None
    rel_tol = 1e-9 if draft.value_brackets is not None else 1e-3
    if not any(math.isclose(result, f, rel_tol=rel_tol, abs_tol=1e-12) for f in figures):
        proposed = (
            "any figure of the proposed schedule"
            if draft.value_brackets is not None
            else f"the proposed {draft.value_scalar:g}"
        )
        return [f"derivation: {draft.derivation} evaluates to {result:g}, not {proposed}"], offsets, None
    note = (
        f"derivation verified deterministically: {_derivation_summary(draft, hits)} = {result:g}; "
        "every operand extract is verbatim in its cited chunk and states its figure, so do NOT "
        "fail citation_supports_value for the value not being stated literally — judge whether "
        "these are the right operands and the right formula for the parameter"
    )
    return [], offsets, note


def _held_digits(held: ParameterValue | None) -> int:
    """Decimals of the amount EUROMOD holds: 0 for 51229, cents otherwise.

    A float cannot tell 1343.40 from 1343.4, so one decimal reads as cents.
    """
    value = held.value if held is not None else None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return 2
    return 0 if float(value).is_integer() else 2


def _rate_digits(held: ParameterValue | None) -> int | None:
    """Decimals of a `/1` rate EUROMOD holds, when four to eight; else None."""
    value = held.value if held is not None else None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    digits = -Decimal(repr(float(value))).normalize().as_tuple().exponent
    return digits if 4 <= digits <= 8 else None


def _round_like_held(
    unit: str, draft: ProposalDraft, held: ParameterValue | None, derived: float | None = None
) -> str | None:
    """Round a derived amount the way the published amount is: half-up, to the held precision.

    The law states the operands, the administration publishes the rounded
    result (the CAF's PAJE ceiling 29 169 × 1,8 = 52 504,2 is published as
    52 504; RSA 646,52 × 1,8 = 1 163,736 is paid as 1 163,74), and the
    rounding rule itself is rarely in the corpus. A `/1` rate held with four
    or more decimals is rounded to as many (AGIRC-ARRCO art. 36: «arrondis au
    centième», 12,954 % → 12,95 %, held 0.1295; three tscerpi rates of the
    5 Nov run were 0.12954 / 0.047244); a coarser rate is left alone, since
    0.0675 is a real change from a held 0.068. Returns the reviewer's note
    when the value changed.

    With `derived`, the verified derivation's own result is rounded, not the
    figure the model typed: the check accepts a result within 0.1 % of it,
    and RSA 646,52 × (1,28412 + 2 × 0,42804) = 1 383,68 was proposed as
    1 383,28 (5 Nov full run, $bsa00_amt9). Without a precision to round to,
    the result itself is proposed: the typed figure never stands.
    """
    if draft.value_scalar is None:
        return None
    if unit == "/1":
        digits = _rate_digits(held)
    elif unit.startswith("currency"):
        digits = _held_digits(held)
    else:
        digits = None
    if digits is None:
        if derived is None or derived == draft.value_scalar:
            return None
        note = f"note: derived {derived:g} proposed (the proposal said {draft.value_scalar:g})"
        draft.value_scalar = derived
        return note
    source = draft.value_scalar if derived is None else derived
    rounded = round_half_up(source, digits)
    if rounded == draft.value_scalar:
        return None
    note = (
        f"note: derived {source:g} rounded half-up to {rounded:g}, "
        f"{'whole units' if digits == 0 else f'{digits} decimals'} like the value held"
    )
    if round_half_up(draft.value_scalar, digits) != rounded:
        note += f" (the proposal said {draft.value_scalar:g})"
    draft.value_scalar = rounded
    return note


#: The magnitude range of a rate per unit: "/1" is a fraction, "/100" a rate
#: held in percentage points (FR `$bho_rl_rate2` = 0.45 for 0,45 %).
_RATE_BOUNDS = {"/1": (-1.0, 1.0), "/100": (-100.0, 100.0)}


def _values_sane(unit: str, draft: ProposalDraft) -> bool:
    """Unit-range and bracket-order sanity.

    The /1 range catches a percentage left unnormalised (11 for 0.11) — a
    magnitude test, so a negative rate is in range: the housing-benefit
    participation rate «Majoration par personne à charge -0,06%» is one.
    """
    if draft.value_brackets is not None:
        thresholds = [b.threshold for b in draft.value_brackets]
        if thresholds != sorted(thresholds) or len(set(thresholds)) != len(thresholds):
            return False
        if unit in _RATE_BOUNDS:
            low, high = _RATE_BOUNDS[unit]
            return all(b.rate is None or low <= b.rate <= high for b in draft.value_brackets)
        return True
    if draft.value_scalar is not None and unit in _RATE_BOUNDS:
        low, high = _RATE_BOUNDS[unit]
        return low <= draft.value_scalar <= high
    return draft.value_scalar is not None


# Public name for the other packages (the eval used the private one).
extract_states = _extract_states
