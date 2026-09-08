# Nómos

Assisted update of EUROMOD fiscal parameters from legislation: a legislation store (Nomotheca),
an agentic proposal workflow with a human validation UI (Nomoscope), and an evaluation pipeline
(Nomokrisis) sharing one database. This file is the opinionated glossary; the wider reference
with pointers into the code is [vocabulary.md](vocabulary.md).

## Language

### Corpus

**Instrument**:
A law, code, act, order or other document stored as one citable whole in the legislation store.
_Avoid_: text, act (as a generic), document (when the stored whole is meant)

**Contributed document**:
A document a reviewer adds by hand, from a URL or a file, outside any country adapter. It becomes an instrument like any other.
_Avoid_: upload, manual document, external document, attachment

**Known official source**:
A national legal portal whose URLs a country adapter can turn into its own national id, so the document is ingested by that adapter instead of as a contributed document.
_Avoid_: recognised URL, native source

**Country Report**:
The EUROMOD document describing a country's modelled tax-benefit system for one release. It describes the model, not the law.
_Avoid_: CR corpus, report

**Kind**:
What a document is in the hierarchy of norms, stated by the reviewer for a contributed document: statute, government regulation, ministerial order, administrative guidance, or other. Each jurisdiction labels these in its own words (loi, décret, arrêté, circulaire, doctrine…).
_Avoid_: type, nature, category

### Trust

**Source-trust class**:
What a document's text may be used for: *evidence*, *guidance* or *context*. Every instrument has exactly one.
_Avoid_: tier, authority level, source type

**Evidence**:
Text that a proposal may cite in support of a value. National legislation is evidence.
_Avoid_: proof, source

**Guidance**:
Text a proposal may cite, but which is not the law: circulars, administrative doctrine, official commentary. A value supported only by guidance is shown as such to the reviewer.
_Avoid_: doctrine (as the class name), secondary source, soft law

**Context**:
Text that may inform how a question is framed but may never be cited in support of a value. Country Reports are context.
_Avoid_: background, reference material

**Supporting extract**:
The passage a proposal quotes from a chunk, which must appear character for character in that chunk.
_Avoid_: quote, snippet, evidence text

### Time

**Validity**:
The date range during which one version of a legal unit is the text in force. For a contributed document the reviewer states its start.
_Avoid_: effective period, in-force dates, applicability

**System year**:
The EUROMOD year a parameter value is stated for. For income-year parameters it names the assessment year, not the income year.
_Avoid_: tax year, as-of year

### Roles

**Reviewer**:
The human who accepts or rejects proposals in the validation UI and who adds contributed documents.
_Avoid_: user, validator, operator, national team (a specific EUROMOD role)
