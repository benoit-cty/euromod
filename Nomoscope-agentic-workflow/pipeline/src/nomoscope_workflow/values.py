"""EUROMOD values as numbers: one arithmetic evaluator, one normaliser.

Until 16 Nov 2026 four places parsed values (paramdb, the eval's scoring, the
derivation check, the benchmark) and disagreed: `8,17%` parsed in paramdb
only, `100%*$MMS` in scoring only, and there were two AST evaluators (code
audit 2.1). Now:

* `eval_arith(tree, leaf)` — the one safe evaluator: + - * / and unary sign
  over whatever `leaf` accepts (numbers for scoring; operand names, calendar
  constants and round() for a derivation, which adds its whitelist on top);
* `percent_literal` — `8.17%` / `8,17%` -> 0.0817;
* `normalise_value` — a raw EUROMOD value (`$PSS * 4#m`, `4,1%`, `100%*$MMS`)
  to (magnitude, period), resolving $-references through a constants map.
"""

from __future__ import annotations

import ast
import operator
import re
from collections.abc import Callable, Mapping
from dataclasses import dataclass

_BINOPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}


def eval_arith(node: ast.AST, leaf: Callable[[ast.AST], float]) -> float:
    """Evaluate + - * / and unary +/- over leaves; anything else goes to `leaf`.

    `leaf` returns the value of a node the arithmetic does not handle (a
    number, a name, a call) or raises ValueError. ZeroDivisionError propagates.
    """
    if isinstance(node, ast.Expression):
        return eval_arith(node.body, leaf)
    if isinstance(node, ast.BinOp) and type(node.op) in _BINOPS:
        return _BINOPS[type(node.op)](eval_arith(node.left, leaf), eval_arith(node.right, leaf))
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        value = eval_arith(node.operand, leaf)
        return -value if isinstance(node.op, ast.USub) else value
    return leaf(node)


def number_leaf(node: ast.AST) -> float:
    """The leaf of a plain arithmetic expression: numeric literals only."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
        return float(node.value)
    raise ValueError(f"unsupported expression node: {ast.dump(node)}")


_PERCENT_LITERAL = re.compile(r"^\s*([-+]?\d+(?:[.,]\d+)?)\s*%\s*$")


def percent_literal(value: str | None) -> float | None:
    """`8.17%` (or `8,17%`) -> 0.0817: EUROMOD's spelling of a rate, as a fraction.

    12 significant digits round away the binary noise of the division (8.17 /
    100 is not 0.0817 in floating point), far below any EUROMOD precision.
    """
    if not isinstance(value, str):
        return None
    match = _PERCENT_LITERAL.match(value)
    if not match:
        return None
    return float(f"{float(match.group(1).replace(',', '.')) / 100.0:.12g}")


#: EUROMOD period suffix -> factor converting the magnitude to the monthly
#: basis (FR_parameter_matching.md §1.1). '#c' (capital) has no time basis;
#: like '#m' it is left unconverted.
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
#: A percent literal anywhere in the expression ('4.1%', '4,1%', '100%*$MMS').
_PERCENT_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*%")
_CONST_RE = re.compile(r"\$([A-Za-z_]\w*)")


@dataclass(frozen=True)
class NormalisedValue:
    """A numeric magnitude plus the period basis its raw form stated, if any."""

    magnitude: float
    period: str | None = None  # 'm', 'y', … (no '#'); None = basis unstated

    def monthly(self) -> float:
        return self.magnitude * PERIOD_TO_MONTHLY.get(self.period or "m", 1.0)


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
    resolve through `constants` (casefolded name without '$' -> number or raw
    string, resolved recursively with a cycle guard); a reference's own period
    suffix is dropped — EUROMOD formulas operate on the stored magnitude.
    Returns None for 'n/a', unknown constants, multiplicative unit suffixes
    ('×1000'), a period marker inside an expression ('242#w*$sw_weeks') or
    anything else that is not a scalar.
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
    # expression ('242#w*$sw_weeks'): '#' opens a comment in Python's grammar,
    # so ast.parse would silently evaluate the prefix. Refuse instead.
    if "#" in text:
        return None
    text = _PERCENT_RE.sub(lambda m: f"(({m.group(1).replace(',', '.')})/100)", text)

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
        magnitude = eval_arith(ast.parse(text, mode="eval"), number_leaf)
    except (ValueError, SyntaxError, ZeroDivisionError):
        return None
    return NormalisedValue(magnitude, period)
