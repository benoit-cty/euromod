# 09: Guidance visible on proposals

**What to build:** When a proposal's every citation comes from a `guidance` instrument, the critique's mechanical pass adds an informational issue "supported by guidance only" without changing the verdict or the routing, the review item carries a guidance-only flag, and the validation UI's detail panel shows a badge on the item and a class marker on each citation. Accept stays available. A reviewer looking at any decision record can therefore see whether the value rests on legislation or on guidance, which keeps the "Legislation is King" rule visible without blocking circular-governed schemes.

Decision record: docs/adr/0001. Glossary: CONTEXT.md (guidance, evidence, supporting extract).

**Blocked by:** 01 (source-trust class on every instrument).

**Status:** done

- [x] The critique's mechanical checks add the informational issue exactly when all citations are `guidance`; mixed and evidence-only proposals get none; verdict and routing are unchanged; DB-free tests in the style of the workflow tests cover the three cases
- [x] The review item exposes a guidance-only flag derived from its citations, preserved through the queue round-trip
- [x] The detail panel shows a badge on guidance-only items and the class on each citation; Accept remains enabled
- [x] The mock proposer and mock hits default to `evidence`, so existing mock runs are unaffected
- [x] Manual check: contribute a guidance document that answers a parameter, run the workflow on it with the mock model, and see the badge on the queue item

## Comments

**2026-09-08 — implemented.** `pipeline.guidance_only` + `GUIDANCE_ONLY_ISSUE`, the item flag, and the badge in DetailPanel. Verified live with a mock run: routing=changed, critique verdict=pass, the informational issue present, guidance_only=true.
