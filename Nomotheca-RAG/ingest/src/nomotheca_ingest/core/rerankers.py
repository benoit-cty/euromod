"""Registry of the cross-encoder rerankers Nómos can score retrieval candidates with.

A reranker reads the query and one candidate chunk TOGETHER and returns a
relevance score, where the embedding model and full-text search each score them
apart and RRF only merges their ranks. It is a second pass over the fused
candidates (retrieval.hybrid_search), never a search of its own: its cost grows
with the pool it is given, not with the corpus.

Nothing in production uses one yet; `nomokrisis-eval run-embeddings --reranker
<key>` measures whether it would help (the `rerank` leg).
"""

from __future__ import annotations

from dataclasses import dataclass

#: Instruction for instruction-aware rerankers, the same task the embedding
#: registry states (English, as their authors recommend).
LEGAL_RERANK_TASK = (
    "Given the description of a tax-benefit parameter, judge whether the passage is the article of "
    "national legislation that sets its value"
)

_QWEN3_PREFIX = (
    "<|im_start|>system\nJudge whether the Document meets the requirements based on the Query and "
    'the Instruct provided. Note that the answer can only be "yes" or "no".<|im_end|>\n'
    "<|im_start|>user\n"
)
_QWEN3_SUFFIX = "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"


@dataclass(frozen=True, slots=True)
class RerankerSpec:
    """How to load one cross-encoder and how to phrase its (query, passage) pair."""

    key: str
    hf_id: str
    licence: str
    max_length: int = 1024
    query_template: str = "{query}"
    document_template: str = "{document}"
    notes: str = ""

    def pair(self, query: str, document: str) -> tuple[str, str]:
        return (
            self.query_template.format(query=query, task=LEGAL_RERANK_TASK),
            self.document_template.format(document=document),
        )


RERANKERS: tuple[RerankerSpec, ...] = (
    RerankerSpec(
        key="bge-reranker-v2-m3",
        hf_id="BAAI/bge-reranker-v2-m3",
        licence="Apache-2.0",
        notes="BGE-M3's own backbone (XLM-R, 0.57 B) trained as a cross-encoder; multilingual.",
    ),
    RerankerSpec(
        key="qwen3-reranker-0.6b",
        # The official checkpoint is a causal LM scored on its "yes" logit; this
        # is the same weights converted to a sequence classifier so a plain
        # CrossEncoder loads it. Scores are identical.
        hf_id="tomaarsen/Qwen3-Reranker-0.6B-seq-cls",
        licence="Apache-2.0",
        query_template=_QWEN3_PREFIX + "<Instruct>: {task}\n<Query>: {query}\n",
        document_template="<Document>: {document}" + _QWEN3_SUFFIX,
        notes="Qwen3 family, 119 languages; instruction-aware.",
    ),
)

_BY_KEY = {spec.key: spec for spec in RERANKERS}


def get_reranker(key: str) -> RerankerSpec:
    spec = _BY_KEY.get(key)
    if spec is None:
        msg = f"Unknown reranker {key!r}; known: {', '.join(_BY_KEY)}"
        raise KeyError(msg)
    return spec
