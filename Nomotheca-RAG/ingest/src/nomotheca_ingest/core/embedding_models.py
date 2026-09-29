"""Registry of the embedding models Nómos can build vectors with.

One entry per `embedding_models` row. The id is the row's primary key and the
`embeddings.model_id` its vectors are stored under, so several models live side
by side in one table and the evaluation compares them on the same chunks
(`nomokrisis-eval run-embeddings --embedding-model-id N`). BGE-M3 keeps id 1
and stays the default; nothing else changes unless a run asks for another id.

Every model is stored at STORED_DIM (the `halfvec(1024)` column):

- a larger Matryoshka-trained model (Qwen3-Embedding-4B/8B) is truncated to its
  first 1024 dimensions and re-normalised, which is how those models are meant
  to be shortened;
- a smaller one (768-d EmbeddingGemma, gte-multilingual) is zero-padded. Padding
  a unit vector with zeros changes neither its norm nor any cosine, so ranking
  is exactly the model's own.

Query and passage texts are encoded differently for most modern models (an
instruction or a "query: " prefix on the query side only). The prompts live
here, in one place, so the passage build and the query encoder can never
disagree — mixing a prompted query with an unprompted corpus silently costs
several points of recall.
"""

from __future__ import annotations

from dataclasses import dataclass, field

STORED_DIM = 1024

#: The instruction for instruction-tuned models. English on purpose: Qwen3 and
#: E5-instruct were trained with English instructions over multilingual text,
#: and their authors recommend keeping the instruction in English whatever the
#: query language. Written for what the framing step actually sends: a
#: parameter's native-language label and description, not a question.
LEGAL_RETRIEVAL_TASK = (
    "Given the description of a tax-benefit parameter, retrieve the article of national "
    "legislation that sets its value"
)


@dataclass(frozen=True, slots=True)
class EmbeddingModelSpec:
    """How to load one model and how to phrase its inputs."""

    id: int
    key: str
    hf_id: str
    native_dim: int
    max_seq_length: int
    licence: str
    query_prompt: str = ""
    document_prompt: str = ""
    trust_remote_code: bool = False
    #: Truncating to STORED_DIM is only legitimate for Matryoshka-trained models.
    matryoshka: bool = False
    #: fp16 is numerically safe for this model (bf16-trained decoders can
    #: overflow in fp16; they stay fp32 unless the GPU does bf16).
    fp16_safe: bool = True
    notes: str = ""
    extra: dict[str, object] = field(default_factory=dict)

    def registry_row(self) -> dict[str, object]:
        """Column values for the `embedding_models` row."""
        return {
            "id": self.id,
            "name": self.key,
            "provider": "self-hosted",
            "native_dim": self.native_dim,
            "stored_dim": STORED_DIM,
            "config": {
                "hf_id": self.hf_id,
                "context": self.max_seq_length,
                "query_prompt": self.query_prompt,
                "document_prompt": self.document_prompt,
                "dim_fit": self.dim_fit,
                "licence": self.licence,
            },
        }

    @property
    def dim_fit(self) -> str:
        if self.native_dim == STORED_DIM:
            return "native"
        return "truncate" if self.native_dim > STORED_DIM else "zero-pad"


MODELS: tuple[EmbeddingModelSpec, ...] = (
    EmbeddingModelSpec(
        id=1,
        key="bge-m3",
        hf_id="BAAI/bge-m3",
        native_dim=1024,
        max_seq_length=8192,
        licence="MIT",
        notes="Production default. XLM-R base: 100 languages incl. Irish; Maltese is not in its pretraining.",
    ),
    EmbeddingModelSpec(
        id=2,
        key="qwen3-embedding-0.6b",
        hf_id="Qwen/Qwen3-Embedding-0.6B",
        native_dim=1024,
        max_seq_length=32768,
        licence="Apache-2.0",
        query_prompt=f"Instruct: {LEGAL_RETRIEVAL_TASK}\nQuery: ",
        fp16_safe=False,
        matryoshka=True,
        notes="Same size and dimension as BGE-M3; 119 languages incl. all 24 EU official languages.",
    ),
    EmbeddingModelSpec(
        id=3,
        key="qwen3-embedding-4b",
        hf_id="Qwen/Qwen3-Embedding-4B",
        native_dim=2560,
        max_seq_length=32768,
        licence="Apache-2.0",
        query_prompt=f"Instruct: {LEGAL_RETRIEVAL_TASK}\nQuery: ",
        fp16_safe=False,
        matryoshka=True,
        notes="16 GB in fp32: needs a 24 GB card, or bf16 on a Turing+/Ampere GPU.",
    ),
    EmbeddingModelSpec(
        id=4,
        key="qwen3-embedding-8b",
        hf_id="Qwen/Qwen3-Embedding-8B",
        native_dim=4096,
        max_seq_length=32768,
        licence="Apache-2.0",
        query_prompt=f"Instruct: {LEGAL_RETRIEVAL_TASK}\nQuery: ",
        fp16_safe=False,
        matryoshka=True,
        notes="Top open model on MMTEB at release; ~16 GB in bf16, a 24 GB+ Ampere card.",
    ),
    EmbeddingModelSpec(
        id=5,
        key="arctic-embed-l-v2",
        hf_id="Snowflake/snowflake-arctic-embed-l-v2.0",
        native_dim=1024,
        max_seq_length=8192,
        licence="Apache-2.0",
        query_prompt="query: ",
        matryoshka=True,
        notes="XLM-R base like BGE-M3 (drop-in size), retrieval-tuned; same language coverage.",
    ),
    EmbeddingModelSpec(
        id=6,
        key="multilingual-e5-large-instruct",
        hf_id="intfloat/multilingual-e5-large-instruct",
        native_dim=1024,
        max_seq_length=512,
        licence="MIT",
        query_prompt=f"Instruct: {LEGAL_RETRIEVAL_TASK}\nQuery: ",
        notes="Strong multilingual baseline, but 512 tokens: long articles are truncated.",
    ),
    EmbeddingModelSpec(
        id=7,
        key="embeddinggemma-300m",
        hf_id="google/embeddinggemma-300m",
        native_dim=768,
        max_seq_length=2048,
        licence="Gemma terms of use",
        query_prompt="task: search result | query: ",
        document_prompt="title: none | text: ",
        fp16_safe=False,
        matryoshka=True,
        notes="Gated on Hugging Face (accept the Gemma terms, then HF_TOKEN). Small and fast.",
    ),
    EmbeddingModelSpec(
        id=8,
        key="gte-multilingual-base",
        hf_id="Alibaba-NLP/gte-multilingual-base",
        native_dim=768,
        max_seq_length=8192,
        licence="Apache-2.0",
        trust_remote_code=True,
        notes="305M encoder, 70+ languages; the cheap option.",
    ),
)

_BY_KEY = {spec.key: spec for spec in MODELS}
_BY_ID = {spec.id: spec for spec in MODELS}
DEFAULT_MODEL = _BY_ID[1]


def get_model(key_or_id: str | int) -> EmbeddingModelSpec:
    """Look a model up by registry key ('qwen3-embedding-0.6b') or id (2)."""
    if isinstance(key_or_id, int) or str(key_or_id).isdigit():
        spec = _BY_ID.get(int(key_or_id))
    else:
        spec = _BY_KEY.get(str(key_or_id))
    if spec is None:
        known = ", ".join(f"{s.id}={s.key}" for s in MODELS)
        msg = f"Unknown embedding model {key_or_id!r}; known: {known}"
        raise KeyError(msg)
    return spec


def fit_dimension(vector: list[float], spec: EmbeddingModelSpec) -> list[float]:
    """Bring a normalised native vector to STORED_DIM (see module docstring)."""
    if len(vector) == STORED_DIM:
        return vector
    if len(vector) < STORED_DIM:
        return vector + [0.0] * (STORED_DIM - len(vector))
    if not spec.matryoshka:
        msg = f"{spec.key} is {len(vector)}-d and not Matryoshka-trained; cannot truncate to {STORED_DIM}"
        raise ValueError(msg)
    head = vector[:STORED_DIM]
    norm = sum(x * x for x in head) ** 0.5 or 1.0
    return [x / norm for x in head]
