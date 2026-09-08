# 05: Route URLs to known official sources

**What to build:** Before a contributed-document run, a URL is classified into one of three outcomes: contributed, adapter (a jurisdiction and national id the existing legislation ingester accepts), or refused with a reviewer-facing hint. A `route` CLI mode prints the outcome as one JSON line, including the suggested title and validity date from ticket 04 for the contributed outcome, so the UI can announce a switch or show a hint before starting. The `document` subcommand applies the same routing again when the run starts and hands adapter outcomes to the existing instrument path, so the library never trusts the caller's classification. At this stage a Légifrance ELI URL without a DILA id is refused with "paste the JORFTEXT id or upload the saved file".

Glossary: CONTEXT.md (known official source).

**Blocked by:** 03 (contribute a file from the CLI), 04 (URL, HTML and PDF inputs).

**Status:** ready-for-agent

- [ ] One routing function covers ES (`BOE-A-…`), NL (`BWBR…`), IE (`<year>/act/<n>`), LT (`TAR.…` and 32-hex ids) and FR (`JORFTEXT…`, `LEGIARTI…` in the path), with tests on each portal's URL shapes
- [ ] FR whole-code `LEGITEXT…` URLs are refused with a hint, mirroring the scout's exclusion; a test pins it
- [ ] ELI-form Légifrance URLs are refused with the paste-the-id hint; a test pins it (ticket 06 replaces this)
- [ ] Unknown domains return the contributed outcome
- [ ] The `route` CLI mode prints exactly one JSON line with the outcome, the adapter arguments or hint, and the suggestions; a CLI test covers it
- [ ] The `document` subcommand re-applies routing and delegates adapter outcomes to the instrument path with the adapter's arguments
- [ ] Manual check: a BOE URL and an e-seimas URL route to their adapters and ingest; a BOFiP URL routes to contributed
