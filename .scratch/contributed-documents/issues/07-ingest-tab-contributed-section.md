# 07: Contributed document section in the Ingest tab

**What to build:** In the validation UI's Ingest tab, a reviewer opens a "Contributed document" section, pastes a URL or picks a file with the file picker, and fills jurisdiction, language, title, kind (labels follow the jurisdiction) and validity start date. On entering a URL or file, the UI calls the `route` mode: for a contributed outcome it prefills title and date from the suggestions; for an adapter outcome it announces "recognised as <source>, switching to the legislation ingester", hides the contributed fields and runs the instrument command; for a refusal it shows the hint. The run button stays disabled until required fields are set. The run streams its log lines and can be cancelled like an instrument run, and on success an embeddings build run starts automatically in the same environment the Embeddings sub-tab uses, so the document is retrievable when the reviewer returns to the queue.

**Blocked by:** 04 (URL, HTML and PDF inputs), 05 (route URLs to known official sources).

**Status:** done

- [x] The Rust ingest command spec gains `document` and `route` commands mapped to the CLI subcommands, with the same log streaming and cancellation as instrument runs; a Rust unit test in the style of the embedding-environment tests pins the argument mapping
- [x] A successful document run schedules an embeddings build run; a Rust test pins that a failed run does not
- [x] The Svelte section has URL field, file picker (dialog plugin), jurisdiction select, language select constrained to the store's configured languages, title, kind select with jurisdiction labels, validity date; the run button is disabled until the required fields are set
- [x] Route pre-check on input: prefill for contributed, announce-and-switch with hidden fields for adapter, hint for refused
- [x] Log lines and cancellation behave as for instrument runs
- [x] Manual check on the running app: contribute the Unedic circular PDF by file and the BOFiP page by URL, watch the embeddings run start, then find one of their chunks through the Database tab's search

## Comments

**2026-09-08 — implemented.** Contributed-document sub-tab in IngestTab.svelte; `document` and `route` in the Rust command spec with the argv mapping and the follow-up embeddings run pinned by unit tests.
