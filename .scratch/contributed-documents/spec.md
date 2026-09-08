# Contributed documents in the Ingest tab

Status: ready-for-agent
Created: 2026-09-08
Glossary: CONTEXT.md (contributed document, known official source, kind, source-trust class, evidence, guidance, context, validity, reviewer)
Decisions: docs/adr/0001-guidance-is-citable-evidence-with-a-visible-class.md, docs/adr/0002-legifrance-eli-urls-resolve-through-a-browser-fallback.md

## Problem Statement

A reviewer knows exactly which text fixes a EUROMOD value: a Unedic circular, an arrêté, a BOFiP doctrine page. Today the legislation store can only be fed through a country adapter keyed by a national id, or through a CLI-only Country Report path that takes a pre-converted Markdown file. There is no way to hand the system a URL or a PDF from the validation UI. The reviewer ends up reading the document by hand and typing values, and the pipeline keeps returning `not_found` for parameters whose operative text is administrative guidance that was never ingested.

## Solution

The Ingest tab gains a "Contributed document" section. The reviewer pastes a URL or picks a file (PDF, HTML, plain text, Markdown), states the jurisdiction, the language, the title, the document's kind, the start of its validity, and optionally the ingested instrument it implements, then starts the run. The ingester fetches or reads the document, archives the raw bytes, extracts and structures the text, loads it as an instrument with a source-trust class, and chains an embeddings build so the document is retrievable immediately. When the URL belongs to a known official source, the tab says so, hides the contributed-document fields, and runs the existing legislation ingester for that adapter instead; Légifrance ELI URLs are resolved to their DILA id first. From then on, proposals may cite the document, and every citation, critique report and review item shows whether its support is legislation or guidance.

## User Stories

1. As a reviewer, I want to paste a URL in the Ingest tab, so that a document I found online enters the legislation store without leaving the UI.
2. As a reviewer, I want to pick a local file (PDF, HTML, text, Markdown) in the Ingest tab, so that a document I saved from a protected portal can be ingested.
3. As a reviewer, I want to state the jurisdiction the document belongs to, so that it is retrievable for that country's parameters and indexed with its language configuration, even when the language alone is ambiguous (French in France and Belgium).
4. As a reviewer, I want to state the document's language, so that full-text search and translation treat it correctly without a detector guessing wrong.
5. As a reviewer, I want the title prefilled from the page title, the PDF metadata or the file name, so that I only correct it rather than type it.
6. As a reviewer, I want to state the document's kind in my country's own words (loi, décret, arrêté, circulaire, doctrine, other), so that the system knows where it sits in the hierarchy of norms.
7. As a reviewer, I want the source-trust class to follow from the kind mechanically, so that I never have to reason about trust levels at upload time.
8. As a reviewer, I want "other" to be treated as guidance, so that an unnamed document can never be granted statute-level trust by accident.
9. As a reviewer, I want to state the date from which the document is in force, prefilled from a date found in the title or URL, so that point-in-time retrieval returns it for the right system years.
10. As a reviewer, I want to be refused when the validity date is missing, so that no version enters the store with an invented legal date.
11. As a reviewer, I want to search the instruments already ingested and pick the one this document implements, so that the provenance is recorded.
12. As a reviewer, I want "none" to be a valid answer to the implements question, with a hint that the statute can be ingested from the same tab, so that a missing statute does not block the upload.
13. As a reviewer, I want to see the run's log lines streaming in the tab, exactly as instrument runs do, so that I know what the ingester is doing.
14. As a reviewer, I want to cancel a running contributed-document run, so that a wrong upload stops early.
15. As a reviewer, I want the run to end with an embeddings build for the new chunks, so that the document is retrievable by the vector leg as soon as the run finishes.
16. As a reviewer, I want to be told "already present" when I add a document whose content is unchanged, so that duplicates never pile up.
17. As a reviewer, I want a re-added document with changed content to become a new version that closes the previous one, so that the history of a page that was updated in place is preserved.
18. As a reviewer, I want the same page linked with two different fragments to remain one instrument, so that BOFiP anchors do not create duplicates.
19. As a reviewer, I want an HTML page to be ingested without its navigation and footer, so that chunks contain the doctrine and not the portal chrome.
20. As a reviewer, I want a document with headings to be split into one legal unit per heading, so that a citation names the section the value lives in.
21. As a reviewer, I want a PDF with no detectable structure to be ingested as one unit, so that unstructured circulars still enter the store.
22. As a reviewer, I want the tab to recognise a Légifrance, e-tar, BOE, eISB or wetten URL, tell me it is switching to the legislation ingester, and hide the contributed-document fields, so that official acts are ingested cleanly through their adapter and I am not asked for fields the adapter supplies.
23. As a reviewer, I want a Légifrance ELI URL to be resolved to its JORFTEXT id, so that the arrêté cited in an official document can be ingested from the form reviewers actually cite.
24. As a reviewer, I want the resolution to try our own database first, then the HTTP redirect, then a headless browser, so that DataDome does not stop an ingestion that only needs an id.
25. As a reviewer, I want a whole-code Légifrance URL to be refused with a hint, so that a 2 000-article code is not ingested by accident.
26. As a reviewer, I want an unresolvable official URL to be refused with "paste the id or upload the saved file", so that I know what to do next.
27. As a reviewer, I want each citation on a review item to show whether it comes from legislation or from guidance, so that I know what a proposal rests on.
28. As a reviewer, I want a review item supported only by guidance to carry a visible badge and an informational critique finding, so that "Legislation is King" stays visible in every decision record.
29. As a reviewer, I want Accept to remain available on a guidance-only item, so that circular-governed schemes can be updated.
30. As a reviewer, I want Country Reports to remain uncitable, so that the model is never used as evidence for itself.
31. As a pipeline operator, I want the Country Report exclusion in evidence retrieval to become a class rule, so that any future context-class corpus is excluded without touching SQL.
32. As a pipeline operator, I want guidance chunks ranked equal to legislation, so that values that exist only in circulars are not hidden.
33. As a pipeline operator, I want the same library function behind the CLI, the TUI and the UI, so that a future cache-miss workflow can contribute documents without a UI.
34. As a pipeline operator, I want the raw bytes of every contributed document archived with their sha256 and origin before anything is parsed, so that the archive-first rule holds for this path too.
35. As a pipeline operator, I want the contributed source rows created idempotently per jurisdiction, so that no seed change is needed before the first upload.
36. As a pipeline operator, I want existing databases to gain the source-trust class column through a migration with a backfill, so that a running installation does not need a volume reset.
37. As a pipeline operator, I want the browser fallback to be an optional extra, so that the CPU-only default environment and the UI keep working without Chromium installed.
38. As an evaluation author, I want guidance-only acceptances countable per language and model, so that the equal-ranking decision can be revisited on data.
39. As a scout maintainer, I want the Légifrance resolver reusable, so that ELI-only URLs the scout finds can later be turned into ids instead of being dropped.

## Implementation Decisions

### Ingester library and CLI

- A new module in the ingester's country-agnostic core exposes one library function that takes either a URL or a local file path plus the reviewer's fields (jurisdiction, language, title, kind, valid_from, optional implemented instrument) and a database URL, and performs fetch or read, archive, parse, load, and relation write. A separate pure function turns bytes plus content type plus the reviewer's fields into the same parsed-document IR the loader already consumes. The CLI gains a `document` subcommand wired to the library function, with the same `--database-url` and progress-line conventions as the other subcommands.
- Fetching happens in Python, never in the UI. The UI passes the URL or the file path.
- Archive-first: the raw bytes are stored as a fetch snapshot with content type, origin URL (or a `file://` URI for uploads) and sha256, under a fetch run with the `manual` trigger, before parsing.
- Identity: one source row per jurisdiction, code `<CC>-CONTRIB`, id system `contributed`, created idempotently on first use. The instrument's national id is the canonical URL (scheme and host lowercased, fragment dropped, trailing slash normalised) for a URL, and `file:<sha256>` for an uploaded file. A second run with the same national id and the same content hash is a no-op reported as "already present". A different content hash creates a new legal unit version starting at the new valid_from and closes the previous version, through the loader's existing version chaining.
- Kind is stored in the instrument's type column, using the jurisdiction's own label (for FR: loi, decret, arrete, circulaire, doctrine, other), consistent with what the FR parser already stores for adapter-ingested acts. The list of kinds and their labels per jurisdiction lives in one table in the core, keyed by the hierarchy-of-norms level (statute, government regulation, ministerial order, administrative guidance, other).
- Source-trust class is a new column on instruments with a check constraint over `evidence`, `guidance`, `context`. Mapping from kind: statute, government regulation and ministerial order map to evidence; administrative guidance and other map to guidance. Country Reports map to context. Adapter-ingested instruments default to evidence. The instrument IR gains the class field and the loader writes it.
- Schema: the column is added to the schema file for fresh volumes, and a numbered migration file under the database directory adds the column, backfills context for the country-report type and evidence for everything else, and sets the NOT NULL default. The retrieval SQL that excluded country reports by instrument type now excludes by class.
- Structure: HTML and Markdown are split into one legal unit per heading, with the preamble before the first heading as its own unit, reusing the heading-driven builder the Country Report path already has (generalised so both callers share it). Plain text and PDFs are one unit unless a numbered-paragraph or heading pattern is detected, in which case the same builder applies. Chunking is the existing character chunker. Context headers read "title > heading".
- HTML: only the main content block is kept (the `main` or `article` element, else the largest text block); the raw page goes to the snapshot and to the unit text's HTML column. PDF text extraction uses a plain-text extractor added as a core dependency; no layout-aware tooling.
- Language is the reviewer's declared language, stored on the unit text with `authentic` authenticity. Title is stored under that language key. The existing translate step then produces the English rendering when run.
- Implemented-instrument link: one instrument relation of type `implements` from the contributed document to the chosen instrument. Retrieval and the critique ignore the relation in this version; it is provenance.
- After load, the library function reports the count of new chunks; the CLI exits successfully; the UI chains an embeddings build run using the same environment selection as the Embeddings sub-tab.

### URL routing and official sources

- A single routing function takes a URL and returns one of three outcomes: contributed (proceed with the contributed path), adapter (jurisdiction plus national id plus the adapter's ingest arguments), or refused (with a reviewer-facing hint). Per-country patterns: ES `BOE-A-…`, NL `BWBR…`, IE `<year>/act/<n>`, LT `TAR.…` or 32-hex id, FR `JORFTEXT…`/`LEGIARTI…` in the URL path; FR `LEGITEXT…` (whole codes) is refused with a hint, mirroring the scout.
- Légifrance ELI-form URLs are resolved to a DILA id in three tiers, in order: exact match on the instruments' ELI column in our database; an HTTP request with browser-like headers following redirects and reading the final URL; on a 403, a headless browser (Playwright) opening the URL and reading the final URL. Only the final URL is used; no page content is parsed or stored. This resolver becomes the FR resolver's first real implementation and is exposed so the scout can reuse it later.
- Playwright and its browser are an optional extra of the ingester (`legifrance`); when the extra is absent the third tier is skipped and the outcome is refused with the hint.
- The UI calls the routing function before starting a run (through the CLI with a `route` mode that prints the outcome as one JSON line) so it can announce the switch and hide fields. The CLI applies the same routing again when the run starts, so the library never trusts the UI's classification.

### Pipeline and UI surfaces

- Retrieval hits and citations carry the source-trust class read from the instrument. The mock proposer and the mock retrieval hits default to evidence.
- The critique's mechanical pass adds an informational issue "supported by guidance only" when every citation on the proposal is of class guidance. It does not affect the verdict or routing.
- The review item exposes whether it is guidance-only, and the UI detail panel shows a badge on the item and on each citation. Accept is not blocked.
- The Ingest tab gains a "Contributed document" sub-section with a URL field, a file picker (through the dialog plugin already in use), jurisdiction and language selects, title, kind select whose labels follow the jurisdiction, valid_from, and an instrument search box backed by a new read-only Tauri query over instruments by title or national id, with "none". The run button is disabled until required fields are set. When routing returns adapter, the section shows "recognised as <source>, switching to the legislation ingester", hides the contributed fields and runs the instrument command; when routing returns refused, it shows the hint.
- The Rust command spec gains a `document` command mapped to the CLI `document` subcommand, with the same log streaming and cancellation as instrument runs, and a follow-up embeddings run started when the document run succeeds.
- The evaluation pipeline records, per case, whether the accepted or proposed value was guidance-only, so it can be grouped with the existing per-language, per-model views.

## Testing Decisions

- A good test exercises the seam's observable output for a realistic input and never inspects internal helpers: a parsed-document IR for given bytes, a routing outcome for a given URL, a critique issue for given hits, a command spec for a given payload.
- Ingester parse seam: tests in the style of the Country Report tests feed a small generated PDF, an HTML page with navigation and a main block, a Markdown file and a plain-text file, and assert instrument identity (source code, national id normalisation, fragment dropping), kind, class, unit hierarchy, validity, language and authenticity, plus the no-op and new-version behaviour of the version key.
- Ingester routing seam: tests cover each country's URL shapes, the two Légifrance id-bearing shapes, the whole-code refusal, and the ELI resolution tiers with an injected resolver callable standing in for the HTTP and browser tiers, including the absent-extra case.
- CLI: help-text tests in the style of the existing CLI tests confirm the `document` subcommand exposes its options and the route mode prints one JSON line.
- Pipeline: tests in the style of the DB-free workflow tests build retrieval hits with classes and assert the guidance-only issue appears exactly when all citations are guidance, that the verdict is unchanged, and that the review item flag is set.
- UI: a Rust unit test in the style of the embedding-environment tests confirms the `document` payload maps to the right CLI arguments and that a successful document run schedules an embeddings run.
- No DB-backed test seam. The schema change, the loader write and the retrieval class filter are verified by hand on a fresh stack.

## Out of Scope

- Language detection; the reviewer declares the language.
- A "supersedes" relation between contributed documents; overlapping validity is accepted in this version.
- Country Reports through the tab; they stay on the CLI-only path, now with class context.
- Drag-and-drop, DOCX or ODT input.
- Layout-aware PDF extraction and table reconstruction.
- Any change to retrieval ranking by class.
- Blocking Accept on guidance-only items or a new routing status.
- Wiring the Légifrance resolver into the scout; only its reusability is required.
- Choosing a relation type other than `implements`.

## Further Notes

- The Unedic circular, the arrêté ELI URL and the BOFiP page from the interview are the three reference inputs; each should be walked through by hand on a fresh stack once the tickets land: the circular as a contributed PDF of kind circulaire, the arrêté through the ELI resolution into the FR adapter, the BOFiP page as a contributed HTML page of kind doctrine with the fragment dropped.
- Playwright bypassing DataDome is purpose-limited to reading a redirect target; the ADR states this and the code should keep the limit visible (no content is returned from the resolver).
- The parsed-document builder shared with the Country Report path is the one refactor that touches existing behaviour; the Country Report tests must stay green.
