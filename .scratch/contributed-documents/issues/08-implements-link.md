# 08: Link the document to the statute it implements

**What to build:** While filling the contributed-document section, a reviewer can search the instruments already in the store by title or national id and pick the one this document implements, or leave it at "none" with a hint that the statute can be ingested from the same tab. On the run, the ingester writes one `implements` relation from the contributed document to the chosen instrument. Retrieval and the critique ignore the relation; it is provenance visible in the Database tab.

**Blocked by:** 07 (contributed document section in the Ingest tab).

**Status:** ready-for-agent

- [ ] The library function and the `document` subcommand accept an optional implemented-instrument id and write an `implements` instrument relation after loading; a test on the IR pins the relation
- [ ] A read-only Tauri query returns instruments matching a title or national id fragment for a jurisdiction, excluding `context` class instruments
- [ ] The Svelte section has a search box with results, a "none" default and the ingest hint
- [ ] Re-running the same document with a different link updates the relation rather than duplicating it
- [ ] Manual check: link the Unedic circular to an ingested Code du travail instrument and see the relation in the Database tab
