# 11: Hand-verified walkthrough of the three reference inputs

**What to build:** On a fresh stack, the three reference inputs from the interview go through the whole feature end to end and any gap found is fixed: the Unedic circular as a contributed PDF of kind circulaire, the arrêté ELI URL resolved through the FR adapter, the BOFiP page as a contributed HTML page of kind doctrine with its fragment dropped. The feature is documented for reviewers and operators.

**Blocked by:** 06 (Légifrance ELI resolution), 07 (contributed document section in the Ingest tab), 08 (implements link), 09 (guidance visible on proposals).

**Status:** ready-for-agent

- [ ] Fresh stack: `docker compose down -v && up`, migration not needed; then the migration is also applied to a pre-feature database dump to confirm the backfill
- [ ] Unedic circular: contributed from the UI by file, kind circulaire, class guidance, linked to a statute, embedded, retrievable, and a mock workflow run on an unemployment-insurance parameter shows the guidance badge
- [ ] Arrêté ELI URL: recognised as Légifrance, resolved to its JORFTEXT id, ingested by the FR adapter with class evidence; a second submission resolves on the database tier
- [ ] BOFiP page: contributed by URL, main content only, fragment dropped, one instrument for two anchors, kind doctrine, class guidance
- [ ] Any defect found is fixed in this ticket with a regression test at the relevant seam
- [ ] The ingester README and the UI README gain a "Contributed documents" section covering the fields, the routing outcomes, the Légifrance extra and the class rules; CLAUDE.md's key constraints mention the source-trust class rule in one line
