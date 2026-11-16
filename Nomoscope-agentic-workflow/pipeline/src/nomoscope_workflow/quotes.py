"""The verbatim-quote rule — the anti-hallucination guarantee — in one module.

Every path that accepts a quote ends here: the proposal's main citation and
each derivation operand (pipeline.critique) and every quote in a chat answer
(chat.resolve_quote). A quote is verified character-for-character against
the chunk it finally names (`verify_extract`, whitespace-tolerant, with the
split-ligature and edge-punctuation rules below); resolution and re-pointing
only ever choose WHICH retrieved chunk is checked, never bypass the check.

Until 16 Nov 2026 the resolve -> repoint -> verify -> hint sequence was
written twice in pipeline.py (main citation, operands) and a third, weaker
copy lived in chat.py without the ligature and punctuation rules (code
audit 2.1).
"""

from __future__ import annotations

import difflib
import re
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from typing import Protocol

import psycopg

from . import issues as issue_text


class Quotable(Protocol):
    """What the resolution rules read from a retrieved chunk."""

    chunk_id: str
    citation: str | None
    content: str


Verify = Callable[[str, str], "tuple[int, int] | None"]


def verify_extract(
    conn: psycopg.Connection, chunk_id: str, extract: str
) -> tuple[int, int] | None:
    """Locate a supposedly-verbatim extract inside the cited chunk.

    Returns (char_start, char_end) offsets into unit_texts.content — the
    anti-hallucination check: no offsets, no verified citation. Whitespace
    runs are treated as equivalent so line-wrapping differences don't fail
    an otherwise verbatim quote, and so is whitespace a PDF extraction put
    between two letters of one word: DSS/2B/2025/38 reads «prestati ons»
    (a split "ti" ligature), and every quote of its BMAF sentence failed on
    the 5 Nov re-run with the right amount proposed. Between digits it is
    never ignored: «25 %» must not match two table cells «2» and «5».
    Punctuation at the quote's two ends is not part of the check either.
    """
    row = conn.execute(
        "SELECT content, char_start FROM chunks WHERE id = %s::uuid", (chunk_id,)
    ).fetchone()
    if row is None or not extract:
        return None
    span = quote_span(row["content"], extract)
    base = row["char_start"] or 0
    return (base + span[0], base + span[1]) if span is not None else None


def quote_span(content: str, extract: str) -> tuple[int, int] | None:
    """Where `extract` sits in `content` under verify_extract's rules, else None."""
    if not extract:
        return None
    idx = content.find(extract)
    if idx >= 0:
        return (idx, idx + len(extract))
    for quote in dict.fromkeys((extract, extract.strip(_QUOTE_EDGE_PUNCTUATION))):
        if not quote.strip():
            continue
        pattern = re.compile(r"\s+".join(re.escape(part) for part in quote.split()))
        match = pattern.search(content) or re.search(_split_word_pattern(quote), content)
        if match:
            return (match.start(), match.end())
    return None


#: Punctuation a quote may end (or start) on that the text does not: the model
#: closes «… deux personnes ; 3° A 16,5 %» on a full stop, or wraps it in «».
#: Stripped from the ends only — every word in between must still match.
_QUOTE_EDGE_PUNCTUATION = " \t\n.;:,«»\"“”'’"


def _split_word_pattern(extract: str) -> str:
    """`extract` as a regex in which whitespace may also fall between two letters."""
    parts: list[str] = []
    for word in extract.split():
        letters = [re.escape(c) + (r"\s*" if c.isalpha() and n.isalpha() else "") for c, n in zip(word, word[1:])]
        parts.append("".join(letters) + re.escape(word[-1]))
    return r"\s+".join(parts)


def closest_passage(content: str, extract: str) -> str | None:
    """The passage of a chunk that a non-verbatim extract was trying to quote.

    Feedback for the retry, never a substitute for the check: models "tidy"
    legal French (la contribution → la contribution sociale, a dropped «à
    charge», an added closing »), and told only "not verbatim" they repeat the
    same quote. The span runs from the first to the last stretch of 6+
    characters the extract shares with the chunk, widened to whole words;
    None when under half the extract matches or the matches are scattered.
    """
    if not extract.strip():
        return None
    matcher = difflib.SequenceMatcher(None, content, extract, autojunk=False)
    blocks = [b for b in matcher.get_matching_blocks() if b.size >= 6]
    if sum(b.size for b in blocks) < len(extract) / 2:
        return None
    start, end = blocks[0].a, blocks[-1].a + blocks[-1].size
    if end - start > 2 * len(extract) + 100:
        return None
    while start > 0 and not content[start - 1].isspace():
        start -= 1
    while end < len(content) and not content[end].isspace():
        end += 1
    return content[start:end]


def resolve_chunk_by_extract(hits: Sequence[Quotable], extract: str) -> str | None:
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
    matches = [h.chunk_id for h in hits if h.content and quote_span(h.content, needle)]
    return matches[0] if len(matches) == 1 else None


def repoint_misquoted(hits: Sequence[Quotable], cited: str, extract: str) -> str | None:
    """A quote absent from the retrieved chunk it cites, found in ONE other: that chunk.

    The model swaps ids between retrieved chunks: on the 5 Nov run «Taux plein
    96,62 % 458,34» (instruction DSS/2B/2025/38) cited a chunk of R. 522-2,
    and RSA's «128, 412 %» a Wallis-et-Futuna article — eleven right values
    refused. The quote is still verified, against the chunk it now names.
    """
    current = next((h for h in hits if h.chunk_id == cited), None)
    if current is None or not current.content or quote_span(current.content, extract):
        return None
    resolved = resolve_chunk_by_extract([h for h in hits if h.chunk_id != cited], extract)
    return resolved


def resolve_chunk_id(hits: Sequence[Quotable], cited: str, extract: str) -> str | None:
    """A cited id that is not a retrieved chunk: by its extract, else by its citation.

    The model often writes the citation string in the id field («LEGITEXT…,
    art. D622-7»), and then misquotes too (the 4 Nov $bhl_max_amt2 run dropped
    the «e» of «1/ 730e»): resolving by the extract fails, the feedback said
    only "not retrieved", and the retry never saw the passage. When exactly
    one retrieved chunk carries that citation it is the chunk meant — the
    extract is still verified against it, and a misquote now gets its hint.
    """
    resolved = resolve_chunk_by_extract(hits, extract)
    if resolved is not None:
        return resolved
    named = [h.chunk_id for h in hits if h.citation and h.citation == (cited or "").strip()]
    return named[0] if len(named) == 1 else None


def misquote_hint(hits: Sequence[Quotable], chunk_id: str, extract: str) -> str | None:
    """The retry's feedback for a non-verbatim extract: what the chunk really says."""
    content = next((h.content for h in hits if h.chunk_id == chunk_id), "")
    passage = closest_passage(content or "", extract or "")
    if passage is None:
        return None
    return issue_text.misquote_hint(passage)


@dataclass(slots=True)
class QuoteCheck:
    """Outcome of checking one quote against the retrieved chunks.

    `chunk_id` is the chunk finally checked (after resolution/re-pointing);
    `status` is "verified", "misquoted" (not verbatim in that chunk) or
    "not_retrieved" (no retrieved chunk could be named); `notes` say how the
    id was corrected, `hint` quotes the passage a misquote was aiming at.
    """

    chunk_id: str
    status: str
    offsets: tuple[int, int] | None = None
    hint: str | None = None
    resolved_from: str | None = None
    notes: list[str] = field(default_factory=list)

    @property
    def verified(self) -> bool:
        return self.status == "verified"


def check_quote(hits: Sequence[Quotable], cited: str, extract: str, verify: Verify) -> QuoteCheck:
    """Resolve, re-point, verify and hint — the one sequence for every quote.

    1. an id that is not a retrieved chunk is resolved by its extract, else
       by its citation (`resolve_chunk_id`), when exactly one chunk qualifies;
    2. an id that IS retrieved but does not hold the quote is re-pointed to
       the ONE other retrieved chunk that does (`repoint_misquoted`);
    3. the quote is verified against the chunk now named (`verify`);
    4. a failed quote gets the passage it was trying to copy (`misquote_hint`).
    """
    cited = (cited or "").strip()
    hit_ids = {h.chunk_id for h in hits}
    check = QuoteCheck(chunk_id=cited, status="not_retrieved")
    if cited not in hit_ids and extract:
        resolved = resolve_chunk_id(hits, cited, extract)
        if resolved is not None:
            check.notes.append(
                f"citation_chunk_id {cited!r} is not a retrieved chunk; resolved to {resolved} — "
                "the only retrieved chunk that contains the supporting_extract verbatim or carries "
                "that citation"
            )
            check.resolved_from, check.chunk_id = cited, resolved
    if check.chunk_id not in hit_ids:
        return check
    repointed = repoint_misquoted(hits, check.chunk_id, extract)
    if repointed is not None:
        check.notes.append(
            f"citation_chunk_id {check.chunk_id!r} does not contain the supporting_extract; "
            f"re-pointed to {repointed}, the only retrieved chunk that does"
        )
        check.resolved_from = check.resolved_from or check.chunk_id
        check.chunk_id = repointed
    check.offsets = verify(check.chunk_id, extract)
    if check.offsets is not None:
        check.status = "verified"
    else:
        check.status = "misquoted"
        check.hint = misquote_hint(hits, check.chunk_id, extract)
    return check


def misquoted_only(issues: list[str]) -> bool:
    """Whether a failed critique objects to nothing but a misquote.

    Such a proposal earns one attempt past MAX_PROPOSAL_ATTEMPTS: its
    feedback quotes the passage it tried to copy, and the attempt after
    `locate` is otherwise the last — RSA forfait logement «calculé pour
    trois personnes ou plus lorsque …» for «… pour trois personnes lorsque
    …» was refused with the right passage in hand ($bsa00_hp_amt5, 5 Nov).
    The extract check itself is unchanged.
    """
    objections = [i for i in issues if not i.startswith("note:")]
    return bool(objections) and all(issue_text.code_of(i) in issue_text.MISQUOTE for i in objections)
