"""Draft a difficulty rung and hazard flags for a golden case, from its ground truth.

Why this module exists
----------------------
`difficulty` used to be assigned as ``"table" if brackets else "plain"`` in three
separate builders — which measured "is this a bracket schedule", not difficulty.
On the first full run 58 of 67 cases landed in one bucket and the field separated
nothing: plain 53% routing vs combine 50%. A field that cannot discriminate
cannot explain a headline.

Two rules keep the replacement honest:

1. **Labels come from the ground truth, never from a run.** Nothing here may
   look at what a model answered. A ladder fitted to outcomes is unfalsifiable —
   it would report that hard cases are the ones we got wrong.
2. **The drafter only claims what it can see.** It reads the expected value, the
   ground-truth citations and the parameter's `temporal_basis`. Three hazards are
   invisible to it — `mid_year_change` (needs the year's legislative history),
   `unit_conversion` (needs to know the period the law states, not the one
   EUROMOD stores) and `budget_act_window` (needs the act's passage date). Those
   stay for a human, which is why `draft_labels` returns its reasoning: a
   reviewer has to be able to disagree with a specific claim.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from nomoscope_workflow.schema import TemporalBasis

#: An expected value that is a formula rather than a number: a $-reference to
#: another parameter, or arithmetic. EUROMOD stores ~75% of FR parameters this
#: way ("$PSS * 4"), and reproducing one means resolving a second parameter and
#: computing — squarely `derive`, however plainly the law states its half of it.
_FORMULA_RE = re.compile(r"[$*/+]|(?<=\d)\s*-\s*(?=\d)")

#: "CGI, art. 197" -> "CGI". Citations are pinpoints into an instrument; two
#: pinpoints into the SAME instrument is one document to read, so only distinct
#: instruments make a case `combine`.
_INSTRUMENT_RE = re.compile(r"^(.*?)(?:,\s*(?:art|article|§|sec|s)\b.*)?$", re.IGNORECASE)


@dataclass
class DraftedLabels:
    """A proposal for one case, plus the reasoning a reviewer needs to reject it."""

    difficulty: str
    hazards: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)


def instrument_of(citation: str) -> str:
    """The instrument a pinpoint citation points into, normalised for comparison."""
    match = _INSTRUMENT_RE.match(citation.strip())
    return (match.group(1) if match else citation).strip().casefold()


def is_formula(value: object) -> bool:
    """True for an expected value EUROMOD stores as an expression.

    Period suffixes are stripped first: "109.50#w" is a plain weekly rate, not
    arithmetic, and the '/' hiding in no suffix should not promote it to derive.
    """
    if not isinstance(value, str):
        return False
    return bool(_FORMULA_RE.search(value.split("#", 1)[0]))


def draft_labels(
    *,
    value: object,
    citations: list[str] | None = None,
    temporal_basis: TemporalBasis | str | None = None,
    is_bracket_table: bool = False,
) -> DraftedLabels:
    """Propose a rung and hazard flags. See the module docstring for the limits.

    The rungs are ordered by the work they demand, and the highest applicable one
    wins: a bracket schedule whose entries are formulas is `table`, because
    getting every bracket right subsumes getting one expression right.
    """
    citations = citations or []
    instruments = {instrument_of(c) for c in citations if c.strip()}
    reasons: list[str] = []
    hazards: list[str] = []

    if is_bracket_table or isinstance(value, list):
        difficulty = "table"
        reasons.append("expected value is a bracket schedule: every bracket must be right")
    elif is_formula(value):
        difficulty = "derive"
        reasons.append(f"expected value {value!r} is an expression, not a number")
    elif len(instruments) > 1:
        difficulty = "combine"
        reasons.append(f"ground truth cites {len(instruments)} distinct instruments")
    else:
        difficulty = "verbatim"
        reasons.append(
            "one instrument, a literal value — nothing here says it takes more than "
            "reading one provision"
        )

    if str(getattr(temporal_basis, "value", temporal_basis)) == TemporalBasis.INCOME_YEAR.value:
        hazards.append("income_year")
        reasons.append("temporal_basis is income_year: system year Y states income year Y-1")

    # A code article that fixes a value by pointing at another act (the PSS
    # arrêté behind $tscsepi_uplim) is the failure mode the gap-fill scout was
    # built for: retrieval lands on the pointer and never follows it.
    if len(instruments) > 1:
        hazards.append("cross_instrument")
        reasons.append("the value is stated across instruments, so one hit is not enough")
    elif is_formula(value) and isinstance(value, str) and "$" in value:
        hazards.append("cross_instrument")
        reasons.append(f"{value!r} defers to another parameter, defined by another act")

    return DraftedLabels(difficulty=difficulty, hazards=hazards, reasons=reasons)
