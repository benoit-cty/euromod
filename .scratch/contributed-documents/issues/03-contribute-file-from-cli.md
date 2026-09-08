# 03: Contribute a local Markdown or text file from the CLI

**What to build:** A reviewer at the command line runs the new `document` subcommand with a local Markdown or plain-text file, a jurisdiction, a language, a title, a kind and a validity start date, and the document enters the legislation store as a contributed document: the raw bytes archived first with their sha256 and a `file://` origin under a `manual` fetch run, the `<CC>-CONTRIB` source created idempotently, the instrument keyed `file:<sha256>` with the kind stored as its type and the class derived from the kind, units built by the shared builder, one authentic unit text in the declared language, chunks for retrieval. Running it again with the same file reports "already present"; running it with a changed file and a later date creates a new version and closes the previous one. The same library function is what the TUI and the UI will call.

Glossary: CONTEXT.md (contributed document, kind, validity, reviewer). Decision record: docs/adr/0001.

**Blocked by:** 01 (source-trust class), 02 (shared heading builder).

**Status:** done

- [x] A core library function accepts a file path plus jurisdiction, language, title, kind, valid_from and a database URL, and performs archive, parse, load in that order
- [x] A pure parse function turns bytes, content type and the reviewer's fields into the parsed-document IR; tests in the style of the Country Report tests cover identity, kind, class, unit hierarchy, validity, language and authenticity for a Markdown file and a plain-text file
- [x] Kinds and their labels per jurisdiction live in one core table keyed by hierarchy-of-norms level; FR labels are loi, decret, arrete, circulaire, doctrine, other; statute, government regulation and ministerial order map to `evidence`, administrative guidance and other map to `guidance`; a test pins the mapping and the "other is guidance" rule
- [x] Missing valid_from is refused with a clear message; no row is written
- [x] The `<CC>-CONTRIB` source row (id system `contributed`) is created on first use and reused afterwards
- [x] Same national id and same content hash: no-op, reported as already present; different content hash: new version from the new valid_from, previous version closed, with tests on the version key behaviour
- [x] The `document` CLI subcommand exposes these options and the shared `--database-url` and progress conventions; a CLI help test in the style of the existing ones covers it
- [x] Manual check: contribute a small Markdown file for FR, confirm instrument, units, unit text and chunks in the database, and that the workflow's retrieval can return one of its chunks for a matching query

## Comments

**2026-09-08 — implemented.** `core/contributed.py` + the `document` CLI subcommand. Verified end to end against the running stack: instrument, units, authentic fr text and chunks in the DB, and the workflow's retrieval returned one of its chunks.
