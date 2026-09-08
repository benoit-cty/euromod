# 10: Guidance-only counted in the evaluation

**What to build:** An evaluation author running the evaluation pipeline gets, per case, whether the proposed or accepted value was supported by guidance only, stored in the eval schema alongside the existing KPIs and grouped by the same per-language, per-model views. This is the data on which the "guidance ranks equal to legislation" decision is to be revisited.

Decision record: docs/adr/0001.

**Blocked by:** 09 (guidance visible on proposals).

**Status:** ready-for-agent

- [ ] The per-case eval record gains a guidance-only field read from the review item's flag; scoring is unchanged
- [ ] The per-language, per-model comparison view exposes the guidance-only count and share
- [ ] The eval tests cover a case with the flag set and one without; the mock offline run still completes
- [ ] The report command prints the guidance-only share per run
