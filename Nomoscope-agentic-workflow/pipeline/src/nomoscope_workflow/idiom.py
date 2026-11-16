"""Legal idiom the deterministic checks read, by language, in one place.

The cross-reference followers, the same-act lookup, the income-year
applicability proof and the derivation's spelled-out numbers read the way a
legal text is written. Most of it is French (the FR corpus is where those
rules were needed); until 16 Nov 2026 the patterns sat inside the generic
modules that use them (code audit 4). They are grouped here, labelled by
language, so a country adds its idiom next to France's instead of inside
retrieval or the critique. Patterns that do not match another language's
text are harmless there: the rules simply find nothing.
"""

from __future__ import annotations

import re

# --- French (fr) -------------------------------------------------------------

#: «article R. 522-2», «articles L. 531-2 et L. 531-3», «art. D. 633-3»: a
#: code article number as the text of a French code writes it.
FR_CODE_ARTICLE_REF = re.compile(r"\b([LRD])\.?\s?(\d+(?:-\d+)+)\b")
#: «… du même code»: the code named last.
FR_SAME_CODE = "même code"
#: «l'article 1er», «aux articles 3 et 4», «à l'article 2 du présent décret»:
#: an article of the act itself. A number followed by another act («de la loi
#: du …», «du code …») is that act's, and skipped.
FR_SAME_ACT_REF = re.compile(r"\barticles?\s+(\d+)(?:\s?er)?\b(?!\s*[-.]\d)", re.IGNORECASE)
FR_OTHER_ACT_AFTER = re.compile(
    r"^\s*(?:,\s*)?(?:du|de la|de l'|de l’|des)\s+(?!présente?\b|même décret|même arrêté)",
    re.IGNORECASE,
)
#: Stock openings of a French applicability clause. A finance-act article ends
#: with one — "II. - Les A et B du I s'appliquent à l'impôt sur le revenu dû au
#: titre de l'année 2024 et des années suivantes" — and it governs everything
#: above it, however far away that is.
FR_APPLICABILITY = re.compile(
    r"(s'appliquent?|applicables?|à compter de|au titre de|pour l'imposition|"
    r"aux revenus (?:perçus|réalisés))",
    re.IGNORECASE,
)

# --- Numbers the law spells out, per language ---------------------------------

#: «dans la limite de trois fois ce plafond» (CSS D622-7) states the operand 3
#: of a derivation as surely as «3» would; two derivations of the 5 Nov run
#: were refused for it.
NUMBER_WORDS: dict[str, dict[str, float]] = {
    "fr": {
        "deux": 2.0, "trois": 3.0, "quatre": 4.0, "cinq": 5.0, "six": 6.0, "sept": 7.0,
        "huit": 8.0, "neuf": 9.0, "dix": 10.0, "onze": 11.0, "douze": 12.0,
        "double": 2.0, "triple": 3.0, "moitié": 0.5, "quart": 0.25,
    },
    "en": {"two": 2.0, "three": 3.0, "four": 4.0, "five": 5.0, "half": 0.5, "twice": 2.0},
}
#: Every language's words: an extract is checked whatever its language.
ALL_NUMBER_WORDS: dict[str, float] = {w: v for words in NUMBER_WORDS.values() for w, v in words.items()}
