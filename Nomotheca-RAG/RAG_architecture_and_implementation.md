---
title: "Architecture and implementation of the RAG"
subtitle: "Nomotheca: the legislation library behind Nómos"
format:
  typst:
    toc: true
    toc-depth: 2
    grid:
      body-width: 6in
      margin-width: 0.4in
      gutter-width: 0.15in
---

**Audience:** the EUROMOD team at JRC.B.2, national-team colleagues and project stakeholders.
Deployment and hosting questions are covered separately in
[it_needs_for_deployment.md](../docs/it_needs_for_deployment.md).

**Purpose:** explain *why* Nómos is built around a RAG, *what logic* it follows and *how* it
works, at the level needed to trust its output and discuss its evolution, without going into
the code.

---

## In one page

- **The job.** Every year, EUROMOD's fiscal parameters (tax bands, benefit amounts,
  contribution rates) must be checked against new national legislation, in the national
  language. Nómos proposes each update with the article that supports it. A human decides.
- **Why a RAG.** A language model (LLM) on its own answers from memory: it does not know
  which year it is talking about, cannot show a source, and sometimes invents numbers. A
  **RAG** (*Retrieval-Augmented Generation*) first *retrieves* the relevant legal text from our
  own database and only then lets the model *generate* an answer, which it must support with
  a word-for-word quote. Code checks the quote, not the model.
- **The logic.** The library is **built on demand**: we fetch the legislation EUROMOD parameters
  actually depend on, not whole legal systems. Every text is **archived with its origin** and
  **dated**, so the question "what did the law say on 1 July 2025?" has exactly one answer.
- **How it searches.** Three complementary searches run together: *by citation* (last year's
  article), *by keywords* (exact legal terms) and *by meaning* (vectors computed by the
  **BGE-M3** model). Their results are merged into one ranked list.
- **Why BGE-M3.** Open, free, multilingual (Lithuanian and Dutch included), able to read a whole
  article at once, and runnable **inside JRC** to reduce cost. Newer open models covering all
  24 EU languages can be **compared with it on our own golden set** (§5.4–5.5).
- **Runs anywhere.** The same model runs on an NVIDIA **GPU** (fast) or on a plain **CPU**
  (slower, no special hardware). Both produce the same vectors.
- **English for everyone.** Every foreign-language article can get an **English machine
  translation**, stored next to the original, so any analyst can read any country. The
  translation helps people read and search. The evidence is always the original text.
- **Pilot.** France, Ireland, Lithuania, the Netherlands and Spain: five languages, five very
  different ways of publishing law.

{{< pagebreak >}}

## 1. Why build a RAG?

### 1.1 The problem we are automating

EUROMOD simulates taxes and benefits for every EU member state. For each country and each
*system year* it holds several hundred numeric parameters: the thresholds of the income-tax
scale, the amount of the child benefit, the ceiling of social contributions, and so on. When a
country passes its annual finance act, or a ministry publishes the new benefit amounts, someone
has to find the right article, read it in the national language, extract the figure and
transcribe it.

That work is slow and needs care, and much of it is repetitive: most of the time the parameter
already cites last year's article, and the task is only to read *the current version* of that
same article. This is the part Nómos automates. Judging whether a figure is right stays with
the analyst.

### 1.2 Why not simply ask an LLM?

Large language models read legal text well in many languages. But asked directly, they answer
**from what they memorised during training**, and that fails in four ways that matter to us:

1. **No notion of "in force on a date".** A model's memory stops at a cut-off date and mixes
   several years together. EUROMOD needs the value for a precise system year.
2. **No source.** An answer from memory cannot be checked. An analyst would have to redo the
   research anyway.
3. **Invented figures.** Models sometimes produce a plausible-looking number that no law
   contains (a "hallucination"). In a fiscal model, a wrong-but-plausible number is the worst
   kind of error.
4. **Uneven language coverage.** Their knowledge of Lithuanian or Dutch legislation is far
   thinner than of French or English.

![The same question asked to an LLM alone and to an LLM grounded by the RAG.](figures/rag-report/01_why_rag.svg){width=100%}

### 1.3 What a RAG changes

A RAG splits the work in two:

- **Retrieve.** Our code, not the model, searches a database of official legislation for
  the few passages relevant to *this* parameter, in *this* country, **in force on this date**.
- **Generate.** The model reads only those passages and proposes a value. It must return
  the passage it relied on, **quoted word for word**, together with its reference.

A program then searches for that quote, character for character, inside the cited passage in
the database. If it is not there, the proposal is rejected, however confident the model sounds.
This is the project's main protection against hallucination, and it relies on the retrieval
database: without a stored, identified passage there would be nothing to check the quote
against.

So the RAG is not an optional add-on. It provides the **dates**, the **citations** and the
**verifiable quotes**, the three things an LLM on its own cannot.

{{< pagebreak >}}

## 2. The logic behind our RAG

### 2.1 Mostly a lookup, sometimes a search

The key observation, made at the start of the project, is that **updating a parameter is mostly
a lookup, not an open-ended search**. Most parameters already carry a legal reference from last
year ("CGI art. 197"). The question is then: *give me that article as it read on date X*. Search
engines are only needed for the harder cases: a new act, a renumbered article, a parameter with
no reference, or a value set each year by a separate decree the statute only refers to.

Three designs were weighed:

| Design | Idea | Why not / why yes |
|------|------|----------|
| A. Full library upfront | Download and index all fiscal law of five countries first | Most of it would never be used; huge ingestion cost; endless refresh work |
| B. No library, live web | An agent reads official websites at run time | Most portals cannot show *past* versions; results change between runs; anti-bot blocks mid-run |
| **C. Library built on demand** (chosen) | Fetch what parameters need, archive it, date it, reuse it | Dated, reproducible, cheap; the library grows where EUROMOD lives |

We chose **C**. JRC confirmed at kick-off that an exhaustive legal corpus is not a
deliverable: only the legislation EUROMOD needs.

### 2.2 Five principles

1. **Archive first.** Every downloaded document is stored exactly as received, with its
   address, date and a digital fingerprint, *before* anything is extracted from it. No text
   enters the library without a provable origin. If a reading error is found later, the text
   is re-read from the archive without downloading again.
2. **Dated versions, never overwritten.** When an article changes, the old version is closed on
   the day the new one starts. Both stay. Asking "as of 1 July 2025" selects exactly one.
3. **Legislation is evidence; the rest is context.** Every document carries a *trust class*:
   **evidence** (laws, decrees, orders), **guidance** (circulars, tax-administration doctrine,
   citable but flagged as guidance on every proposal) and **context** (EUROMOD Country Reports,
   never citable). Country Reports describe the model itself, so citing them to support the
   model would be circular. They are still used to translate EUROMOD acronyms into official
   national names.
4. **Scoped by territory.** A Spanish regional parameter (Aragón) can only be supported by
   Spanish national law or Aragón's own acts, never by another region's decree with the same
   number.
5. **One shared core, one adapter per country.** About 80 % of the code is the same for every
   country. What differs (the portal, the file format, the numbering of articles) is isolated
   in a small country adapter. Adding a country means writing an adapter; the rest stays as
   it is.

### 2.3 The big picture

![From official portals to a validated EUROMOD parameter. The RAG is the left half; the agentic workflow and the validation UI use it.](figures/rag-report/02_big_picture.svg){width=100%}

When a search finds nothing usable, the usual cause is **a missing act**, not a weak model.
For example, the French social-security ceiling is fixed each year by a ministerial order that
no finance act contains. A component called the **scout** then identifies the missing act
(by its official identifier) and hands it to the normal ingestion path. The act is archived,
dated and indexed like any other, and the search runs again. Web search results are only used
to find *which* act to fetch. They are never used as evidence.

{{< pagebreak >}}

## 3. How it works

### 3.1 Ingestion: from a portal to the library

![The ingestion steps. Orange steps belong to the country adapter, blue ones to the shared core, green ones run later as batch jobs.](figures/rag-report/03_ingestion.svg){width=100%}

1. **Resolve.** A human-readable reference ("CGI art. 197, in force 2025") is turned into the
   exact identifier the national system uses (`LEGIARTI…` in France, a `BWBR…` number in the
   Netherlands, a `BOE-A-…` in Spain).
2. **Fetch.** The official file is downloaded from the national open-data source. We never
   crawl: every download starts from a known identifier.
3. **Archive.** The raw bytes are stored with their origin (see §2.2).
4. **Parse.** The national format (XML, JSON, HTML) is converted into one common structure:
   act → articles → dated versions → text.
5. **Load.** Versions are placed on the timeline and each article's text is cut into
   **chunks**, which can be searched by keyword straight away.
6. **Enrich**, later and in bulk: each chunk gets its **embedding** (§4) and, where useful, an
   **English translation** (§6). These run as jobs on the worker and may lag behind loading
   without blocking keyword search.

Re-running an ingestion is harmless: anything already present is recognised and left as it is.

### 3.2 Chunks: the unit of search and of citation

A **chunk** is normally one whole article (or, for a long article, one part of it), preceded by
a short breadcrumb header such as *"Code général des impôts > Art. 197"*. Chunks follow the
legal structure instead of cutting every N words, for two reasons:

- an article is the unit lawyers cite and analysts recognise;
- the chunk's identifier becomes **the reference stored on the proposal** (`jrc_database_id`),
  with the exact position of the quote inside the text. A reviewer can open the exact
  passage from the validation UI.

When a value and its conditions sit in two chunks of the same article, the neighbouring chunk
is brought along automatically.

### 3.3 Retrieval: three searches, one list

![Filters are applied first, then three searches run and are merged.](figures/rag-report/06_hybrid_search.svg){width=100%}

**Before any search**, candidates are restricted to texts *in force on the reference date*, *in
the right country (and region)*, *in the law's language* and *not of trust class "context"*.
Then:

1. **Citation fast path.** If last year's parameter cites an article, go straight to its
   current version. Spelling variations ("art 197 CGI", "CGI, art. 197") are tolerated. This
   covers the common case in one lookup.
2. **Keyword search.** The classic full-text search, in the law's own language: words are
   reduced to their stem (*impôts → impôt*) and accents are ignored. It is precise on exact legal
   terms (*plafond*, *barème*, *décote*).
3. **Meaning search.** Each chunk and each question is turned into a list of 1 024 numbers (an
   *embedding*) that captures its meaning. Texts that say the same thing in different words end
   up close together. This finds the right article when the parameter's name and the law's
   wording differ.

The two ranked lists are merged by **Reciprocal Rank Fusion**: a chunk ranked high by *both*
methods goes to the top. The best few chunks, plus their neighbours, are handed to the model.

The query itself is prepared carefully (the "framing" step of the workflow). A EUROMOD
parameter is a cryptic identifier such as `$tin_upthres1`, so framing uses its native-language
label, the vocabulary of the Country Report (which maps EUROMOD acronyms to official names) and
last year's citation.

{{< pagebreak >}}

## 4. The database: how the tables fit together

### 4.1 Five nested levels of legal content

![The five nested levels of the legislation database, with a French example on the right.](figures/rag-report/04_db_levels.svg){width=100%}

Each level answers one question and only that one:

| Table | Answers | Example |
|------|--------|--------|
| `instruments` | Which law, code or decree? | *Code général des impôts* |
| `legal_units` | Which article, as a stable "slot"? | CGI, art. 197 |
| `legal_unit_versions` | What did it say **between which dates**? | art. 197, 16 Feb 2025 → 21 Feb 2026 |
| `unit_texts` | **In which language** is this text? Original or translation? | French (authentic), English (machine translation) |
| `chunks` | Which passage is searched and cited? | the article with its header |

Separating *structure* (the article), *time* (its versions) and *language* (its texts) means
that none of them overwrites another. A new version does not erase the old one, and a
translation does not replace the original.

### 4.2 Time: one answer per date

![Dated versions of one article. The reference date picks exactly one version.](figures/rag-report/05_timeline.svg){width=100%}

The database **forbids** two versions of the same article from overlapping in time. It is a
rule of the database itself, so no program can break it by mistake. As a result, a
point-in-time question is a simple filter and never an approximation. Evaluation runs can also
be **frozen** on a labelled set of downloads, so that comparing two models months apart compares
the models, not two different states of the library.

France adds one complication, handled by the workflow rather than the database: income tax is
assessed on the *previous* year's income. EUROMOD system 2025 therefore needs the scale applied
to 2024 income, which is enacted in the 2025 finance act.

### 4.3 The supporting tables

| Group | Tables | Role |
|----|------|----------|
| **Where from** | `jurisdictions`, `sources` | Countries (and Spanish regions as child territories) and the official portals we read |
| **Provenance** | `fetch_runs`, `fetch_snapshots` | Each ingestion run and every raw file it downloaded, with URL, date and fingerprint. Append-only: nothing is ever deleted or changed |
| **Search** | `embeddings`, `embedding_models`, `lang_fts_config` | One vector per chunk *per model* (so several models can be compared side by side), and the keyword-search settings for each language |
| **Links between acts** | `instrument_relations` | "Finance act 2025 amends CGI art. 197": kept for traceability, never used to decide what is in force |
| **Who cites what** | `citation_registry` | Which EUROMOD parameters rely on which article, to answer "if this article changes, which parameters are affected?" and to prevent deleting a cited text |

EUROMOD parameters themselves are **not** stored in this database. They live in their own schema
and point to legislation **by reference only**, through the chunk identifier.

{{< pagebreak >}}

## 5. The embedding model: BGE-M3

### 5.1 What an embedding model does

An embedding model reads a text and returns a fixed-length list of numbers (for BGE-M3, 1 024
of them) such that **texts with similar meaning get similar numbers**. Comparing the numbers of
a question with those of every chunk gives the "meaning search" of §3.3. The same model must be
used for the library and for the questions, otherwise the numbers are not comparable.

### 5.2 Why we chose BGE-M3

**BGE-M3** (from the Beijing Academy of Artificial Intelligence, `BAAI/bge-m3`) was chosen
against the project's own constraints:

| Requirement | Why it matters here | BGE-M3 |
|------|--------|--------|
| **Multilingual** | Five pilot languages today, the 24 official languages of the 27 member states tomorrow; keyword search is weakest in Lithuanian (no stemmer available) | Trained on 100+ languages, including Lithuanian, Dutch, Spanish, French and Irish |
| **Long input** | A legal article can be long; cutting it loses context | Reads up to ~8 000 tokens: most articles fit as one chunk |
| **Runs at JRC** | No legal text or query should have to leave JRC while the model-hosting policy is open | Open weights, runs on JRC hardware, no external API |
| **Free and open licence** | Redistribution to JRC and reuse by other services | MIT licence |
| **Modest hardware** | Must run on a standard GPU or even on CPU | ~570 M parameters; ~4 GB of GPU memory |
| **Strong retrieval quality** | Finds the right article | Among the best open multilingual retrieval models at selection time |

The database keeps one vector per chunk **per model**, so alternatives can be added side by
side and compared without changing the design (§5.4–5.5). Changing the default model means
recomputing every vector, which is why we stay with BGE-M3 unless the evaluation shows a clear
gain.

### 5.3 CPU or GPU: the same result, different speed

![One model, two kinds of hardware, the same vectors.](figures/rag-report/07_cpu_gpu.svg){width=100%}

All model work happens in one place, the **worker** (*Nomergon*). Analysts' workstations never
load the model. The worker exists in two builds from the same recipe:

- **GPU build (NVIDIA).** The model runs with PyTorch on CUDA; the GPU is detected
  automatically. About 4 GB of video memory is enough, and older cards are supported (they
  run in full precision). Embedding a whole country's corpus takes **hours**.
- **CPU build.** No graphics card and no CUDA libraries needed, so the image is much smaller.
  On Intel processors the model runs through **OpenVINO**, Intel's optimised runtime (which can
  also use the Intel integrated GPU or NPU). Embedding the whole corpus takes **days**, but a
  single search question is still encoded in about a second.

Both builds produce **the same vectors** in the same table. The choice between them is about
budget and speed and has no effect on results. The usual pattern: bulk embedding on a GPU
(overnight batches), everyday searching on whichever machine is available.

### 5.4 Alternatives that cover all EU languages

The 27 member states have **24 official languages**. The two that most models handle worst are
**Irish** and **Maltese**. Both countries also publish their law in English, so English
retrieval is a safety net there, but a model for 27 countries should still read them.

Since BGE-M3 was released (early 2024), open models trained for multilingual retrieval have
improved a lot. The candidates below all have **open weights and run inside JRC**. They are
registered in Nomotheca, so any of them can be built and compared with one command:

| Model | Size | Reads up to (tokens) | Licence | EU languages | Why consider it |
|---|---|---|---|---|---|
| **BGE-M3** (current) | 0.57 B | 8 000 | MIT | 23 of 24 (no Maltese) | The baseline |
| **Qwen3-Embedding-0.6B** | 0.6 B | 32 000 | Apache 2.0 | all 24 (per its authors) | Same size and vector length as BGE-M3, clearly ahead on the public multilingual benchmark |
| **Qwen3-Embedding-4B / 8B** | 4 B / 8 B | 32 000 | Apache 2.0 | all 24 (per its authors) | The best open models on that benchmark. They need a newer GPU (§5.6) |
| **Arctic-Embed-L v2** (Snowflake) | 0.57 B | 8 000 | Apache 2.0 | as BGE-M3 | Same architecture as BGE-M3, further tuned for retrieval: a drop-in swap |
| **multilingual-E5-large-instruct** | 0.56 B | 512 | MIT | as BGE-M3 | Strong, but reads about one page: long articles are cut |
| **EmbeddingGemma** (Google) | 0.3 B | 2 000 | Gemma terms | 100+ languages | Small and fast. Licence terms to check, and the download needs registration |
| **gte-multilingual-base** (Alibaba) | 0.3 B | 8 000 | Apache 2.0 | 70+ languages | The cheapest option |

On the public multilingual benchmark (MMTEB: general-purpose texts, not law), the Qwen3 family
scores well above BGE-M3: roughly 64 for the 0.6B and 70 for the 8B, against 60 for BGE-M3.
Two cautions apply. A general-purpose ranking does not carry over automatically to national tax
and social-security law. And some top-ranked models (from NVIDIA and Jina, for example) are
**licensed for non-commercial use only**, which rules them out for JRC production. That is why
we measure on our own task (§5.5) before changing anything.

Models behind an external API (OpenAI, Google, Mistral, Cohere) could be compared the same way,
but only if JRC policy allows sending legislation and queries outside.

### 5.5 Comparing models on our own task

The comparison uses the **golden set** of the evaluation pipeline (Nomokrisis): parameters for
which a human has verified which article states the value. Each one becomes a search test:

1. **The question** is exactly what Nómos sends when it looks for that parameter (the framing
   step of §3.3): its label and description in the law's language, plus Country Report
   vocabulary.
2. **The answer** is the article (or articles) the verified case names, looked up in the library
   on the right date and in the right country.
3. **Each model ranks all the country's texts** in force on that date. We record where the right
   article appears: first, in the top 3, or in the top 15.

The scores are simple and deterministic, with no AI judge:

- **hit@1**: the right article is the first result;
- **hit@3**: it is in the top 3, the results the hybrid search always passes on to the language
  model;
- **hit@15**: it is somewhere in what the language model reads;
- **MRR**: the average of 1 ÷ rank (1 means always first, 0.5 always second).

All models answer the same 64 questions over the same texts, and a question counts only if every
model was asked it. Keyword search and the full hybrid search are scored alongside, to check
that a better embedding also improves what Nómos actually retrieves.

RESULTS_PLACEHOLDER

### 5.6 Do we need a bigger GPU?

**For embeddings, no.** Measured on the development workstation, a 2017 NVIDIA GTX 1080 Ti with
11 GB of memory, shared with the worker:

| | BGE-M3 | Qwen3-Embedding-0.6B |
|---|---|---|
| Video memory used | ~4.3 GB | ~5.4 GB |
| Speed (whole articles) | ~7.5 articles/s | SPEED_QWEN |
| All authentic pilot texts (~23 000 articles) | under 1 hour | TIME_QWEN |
| One search question | tens of milliseconds | tens of milliseconds |

The library is built on demand, so it grows with the parameters, not with the whole legal
system. At the pilot's density, 27 countries would be about 120 000 authentic articles: **one
night** of embedding on this card. After that, only new or amended articles are embedded again.
The 0.6-billion-parameter class (every drop-in candidate above) therefore runs comfortably on
the existing GPU, and a plain CPU is enough to encode everyday search questions.

Two limits of this card are worth knowing:

- **No fast half-precision mode.** Newer GPUs run models in 16-bit precision at about twice the
  speed and half the memory. The 1080 Ti predates that: we measured 16-bit to be **four times
  slower** than 32-bit, so it runs everything in 32-bit.
- **The large models do not fit.** Qwen3-Embedding-4B needs about 16 GB in 32-bit, the 8B about
  32 GB. They need a recent card with 16-bit support: **16 to 24 GB for the 4B, 24 GB or more for
  the 8B** (an NVIDIA L4 or RTX 4090 class card, for example). They also cost 7 to 13 times more
  computation per article.

So a bigger GPU becomes worthwhile only in two cases: if the comparison shows that a **4B or 8B
model** brings a gain the 0.6B class does not, or if Nómos starts running its **language
models** locally instead of through an API. Language models, not embeddings, are what need
large GPUs.

{{< pagebreak >}}

## 6. Translation into English

### 6.1 Why translate

The EUROMOD team works in English, but the law of four of the five pilot countries is not
written in English. A reviewer asked to accept a Lithuanian or Dutch figure needs to understand
the article that supports it. So every article version can receive an **English machine
translation**, produced by an LLM as a batch job on the worker.

![The original and its English translation are stored side by side; each has its own role. The Lithuanian wording is illustrative.](figures/rag-report/08_translation.svg){width=100%}

### 6.2 How it is done

- The translation is stored **next to** the original, as a second text of the same article
  version, labelled *machine translation*, with its source language and the engine that
  produced it. The original is never modified.
- The translator is instructed to **never alter numbers, amounts, dates or legal
  identifiers**, to keep the article's structure and numbering, and to keep official act names
  in the original language.
- The English text is cut into chunks and embedded like any other, so it can be searched.
- The job is repeatable: articles already translated are skipped, and a changed original can
  be re-translated.

### 6.3 What it is used for, and what not

| Used for | Not used for |
|---|---|
| Reading any country's source in the validation UI, next to the original | **Evidence.** The quote supporting a proposal is always checked in the **original, authentic** text |
| Searching all countries at once in English from the UI's database tab | Replacing an official translation where one exists (those are stored as *official translation*) |
| Measuring whether searching in the original language or in English finds the right article more often (a question the contract asks) | |

Each proposal also carries the model's English rendering of its quote, so the reviewer reads
the key sentence in English without opening the source.

**The other direction.** EUROMOD's own parameter labels are in English, while keyword search
works in the law's language. The workflow therefore also translates each parameter's label
*into* the law's language ("tax-exempt income amount" → *neapmokestinamųjų pajamų dydis*),
so that keyword search uses the same words as the law.

{{< pagebreak >}}

## 7. The pilot countries

The contract asked for five member states that **differ in language and in how accessible their
law is**. The pilot covers:

| Country | Official source we read | What makes it interesting |
|------|----------|--------------|
| **France** (French) | DILA open data (LEGI + JORF), via the Tricoteuses daily mirror. Ids `JORFTEXT…`, `LEGIARTI…`, ELI | Richest data, with dated consolidated versions of every code article. Légifrance itself is protected by anti-bot measures, so we read the open-data dumps instead. Income tax is dated by *income year* |
| **Ireland** (English, Irish) | Irish Statute Book (eISB), with the Oireachtas API to locate acts. Ids like `1997/act/39`, ELI | Common-law drafting (Acts, sections, Statutory Instruments); no translation needed; acts mostly available as enacted rather than consolidated |
| **Lithuania** (Lithuanian) | Register of Legal Acts (TAR), via the national open-data API. `TAR…` document ids | Official API with dated consolidations; no stemmer for keyword search, so meaning search matters most; never-amended acts have no consolidation and are read from the original |
| **Netherlands** (Dutch) | Basiswettenbestand (BWB), the official consolidated XML behind wetten.overheid.nl. `BWBR…` ids | Dated consolidations per act; no ELI; some formulas published as images |
| **Spain** (Spanish) | BOE consolidated-legislation open-data API. `BOE-A-…` ids | Best machine-readable access; adds a **regional** layer: the autonomous communities set their own income-tax rates and allowances, so regions are child territories of Spain |

Belgium is already provided for in the design (its laws are authentic in French *and* Dutch at
the same time, which the database accepts) but is not part of the pilot ingestion.

Adding a sixth country is mostly work on its source: a short analysis of its official portal,
a few configuration rows, and a country adapter (resolve, fetch, parse). The database, the search
and the workflow stay as they are.

## 9. Adding a country

A _skill_ has been prepared in `.claude/skills/add-country/SKILL.md` so a coding agent could handle the task of adding a new country with a single command: `/add-country Belgium`.

## 10. Interface

The Nomoscope UI display the state of the database:
![The Nomoscope UI display the state of the database](figures/rag-report/ui_database.png){width=100%}

Here we can see that the embeddings cover all articles, but we are missing translations for Spain and Netherlands.

It's possible to start them from the 'Ingest' panel.

This panel also allow for custom ingest of a webpage or a PDF:
![The Nomoscope UI display the ingestion of a custom document](figures/rag-report/ui_ingest_document.png){width=100%}

So the RAG database is not limited to the document the AI find. Not even to laws related to Euromod, it could be used for other purpose of the JRC.

## Conclusion

Nomotheca is the foundation of Nómos: a library of national legislation and a search engine on top of it. It gives the agentic workflow what a language model cannot provide by itself: the law **as it read on a given date**, an **identified passage** to cite and a **stored text** against which every quote is verified. That is what turns a proposed parameter value into something an analyst can check in seconds, instead of a claim to believe.

Four choices make it trustworthy and keep it practical:

- **Built on demand, archived first.** The library holds what EUROMOD parameters depend on, each text kept with its origin and its dates, so any answer can be reproduced.
- **Hybrid search.** Citation lookup, keywords and meaning (embeddings) run together, so the right article is found whether the parameter's name matches the law's wording or not.
- **Open and local.** The model, the archive and the database run inside JRC, on a GPU or on a plain CPU. No legal text has to leave.
- **Original text as evidence, English as help.** The translation lets any analyst read any country. The proof is always in the authentic text.

The library is also not tied to EUROMOD. The same pipeline ingests any web page or PDF, and a new country is one adapter away (§9), so it can serve other JRC uses.

The main limit is coverage: the pilot library is only as complete as the acts ingested so far. When a search finds nothing, the first thing to check is a missing act or a missing translation, not the model. The next step is to measure retrieval on the golden set (Nomokrisis) and extend the library to more member states.

CONCLUSION_PLACEHOLDER

{{< pagebreak >}}

## Annex A - Vocabulary

The complete glossary is [docs/vocabulary.md](../docs/vocabulary.md). The terms below are the
ones needed for this report.

### Project names

| Term | Meaning |
|---|--------|
| **Nómos** | The whole project (Greek *νόμος*, "law"). |
| **Nomotheca** | The legislation library and its ingester: the RAG described here ("library of laws"). |
| **Nomosync** | The ingestion part of Nomotheca: fetch → archive → parse → chunk → load. |
| **Nomoscope** | The agentic workflow that proposes parameter values, and the validation UI. |
| **Nomokrisis** | The evaluation pipeline that scores the whole chain against a verified *golden set*. |
| **Nomergon** | The worker: the only process that runs models, holds credentials and reaches the internet. |

### Legal and data-source terms

| Term | Meaning |
|---|--------|
| **Instrument** | A law, code, decree or order considered as a whole. |
| **Consolidated version** | The text of an article as it reads after all amendments up to a date, as opposed to the amending act itself. Point-in-time answers come from consolidated versions. |
| **Validity** | The date range during which a version is in force. |
| **Hierarchy of norms** | Statute → government decree → ministerial order → guidance. Many EUROMOD figures are not in the statute but in an annual decree or order it refers to. |
| **ELI** | *European Legislation Identifier*: a standard web address for a legal act. Unevenly deployed across countries, so we never depend on it. |
| **National id** | The identifier each national system actually uses (`LEGIARTI…`, `BWBR…`, `BOE-A-…`, `TAR…`). |
| **Archive-first / snapshot** | The raw downloaded file, stored with origin and fingerprint before being read. |
| **Trust class** | *evidence* (legislation), *guidance* (circulars, doctrine: citable but flagged) or *context* (Country Reports: never citable). |
| **Authenticity** | Whether a text is the *authentic* original, an *official translation* or a *machine translation*. |

### RAG and search terms

| Term | Meaning |
|---|--------|
| **RAG** | *Retrieval-Augmented Generation*: retrieve relevant documents first, then let an LLM answer from them. Ours is **built on demand** rather than crawled upfront. |
| **LLM** | *Large Language Model*: the AI model that reads the retrieved text and proposes a value. |
| **Chunk** | The piece of text that is searched and cited, usually one article with a header. |
| **Embedding / vector** | A list of numbers (1 024 for BGE-M3) representing a text's meaning. Similar meanings get similar numbers. |
| **BGE-M3** | The open multilingual embedding model we use (§5). |
| **Embedding benchmark** | The side-by-side test of embedding models on questions built from the golden set (§5.5). |
| **hit@k / MRR** | Search scores: the right article is in the top *k* results / the average of 1 ÷ its rank. |
| **Full-text (keyword) search** | Word-based search in the law's language, with stemming and accent-insensitive matching. |
| **Hybrid search** | Keyword and meaning searches run together and merged. |
| **RRF** | *Reciprocal Rank Fusion*: the rule that merges ranked lists, favouring chunks ranked high in both. |
| **Citation fast path** | Going straight to the article last year's parameter cited, before any search. |
| **Scout** | The component that, when nothing is found, identifies the missing act so it can be ingested. |
| **Verbatim check** | The code check that the model's quote appears character for character in the cited chunk. The core anti-hallucination rule. |
| **Hallucination** | A model output not supported by the source, such as an invented figure. |
| **GPU / CPU** | Graphics processor (fast for models) / ordinary processor (slower, no special hardware). |
| **OpenVINO** | Intel's runtime that makes models run fast on Intel CPUs. |

### EUROMOD terms

| Term | Meaning |
|---|--------|
| **System year** | The year a EUROMOD country system represents (`FR_2025`). One workflow run checks one system year. |
| **Reference date (`as_of`)** | The date used to select the law in force. EUROMOD reflects the law as of 30 June, so reference dates are mid-year. |
| **Income year** | For French income tax, system year Y applies the scale for income year Y−1. |
| **Country Report** | EUROMOD's annual description of each country system. Used for vocabulary, never as evidence. |
| **Parameter target** | The address of a parameter, e.g. `euromod://FR/tin_fr/def_const/$tin_upthres1` (country / policy / function / parameter). |

---

**Further reading (technical):** [10_retrieval-strategy-challenge.md](10_retrieval-strategy-challenge.md)
(the choice of an on-demand RAG), [11_database-model.md](11_database-model.md) (database design),
[12_ingestion-architecture.md](12_ingestion-architecture.md) (shared core and country adapters),
and the per-country source analyses in this folder.
