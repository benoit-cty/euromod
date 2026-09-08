# 01: Source-trust class on every instrument

**What to build:** Every instrument in the legislation store carries a source-trust class (`evidence`, `guidance`, `context`), and evidence retrieval excludes by class rather than by the `country_report` type string. A pipeline operator on a fresh stack sees Country Report chunks still never returned as evidence, and every retrieval hit and citation in a run trace shows the class of the instrument it came from. An existing database gains the column through a migration with a backfill, without a volume reset.

Decision record: docs/adr/0001. Glossary: CONTEXT.md (source-trust class, evidence, guidance, context).

**Blocked by:** None (can start immediately).

**Status:** ready-for-agent

- [ ] The schema file adds the class column to instruments with a check constraint over the three values and a NOT NULL default of `evidence`
- [ ] A numbered migration file under the database directory adds the column to an existing database and backfills `context` for the country-report type and `evidence` for everything else
- [ ] The instrument IR has a class field; the loader writes it; the Country Report path sets `context`; every country adapter leaves the default `evidence`
- [ ] Evidence retrieval SQL (citation fast path and hybrid search) excludes `context` by class; the Country Report search still finds only `context`
- [ ] Retrieval hits and citations in the workflow schema carry the class; the mock retrieval hits and mock proposer default to `evidence`
- [ ] Existing ingester, workflow and eval tests stay green; Country Report parse tests assert the `context` class
- [ ] Manual check on a fresh stack: `docker compose down -v && up`, ingest one FR instrument and one Country Report, run one workflow target, confirm the trace shows the class on hits and contains no CR chunk as evidence
