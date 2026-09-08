# 10: Guidance-only counted in the evaluation

**What to build:** An evaluation author running the evaluation pipeline gets, per case, whether the proposed or accepted value was supported by guidance only, stored in the eval schema alongside the existing KPIs and grouped by the same per-language, per-model views. This is the data on which the "guidance ranks equal to legislation" decision is to be revisited.

Decision record: docs/adr/0001.

**Blocked by:** 09 (guidance visible on proposals).

**Status:** done

- [x] The per-case eval record gains a guidance-only field read from the review item's flag; scoring is unchanged
- [x] The per-language, per-model comparison view exposes the guidance-only count and share
- [x] The eval tests cover a case with the flag set and one without; the mock offline run still completes
- [x] The report command prints the guidance-only share per run

## Comments

**2026-09-08 — implemented.** `CaseResult.guidance_only`, the eval.results column and the run_summary count/share, printed by `report`. The mock offline run still completes (verified against the live eval schema).
