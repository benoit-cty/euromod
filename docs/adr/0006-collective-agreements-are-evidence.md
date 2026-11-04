---
status: accepted
date: 2026-11-03
---

# Collective agreements are evidence, like the law

Some EUROMOD parameters are set by the social partners, not by the State. In France that covers
the AGIRC-ARRCO complementary pension contributions (ANI du 17 novembre 2017, art. 37: CEG
2,15 % / 2,70 %, CET 0,35 %), APEC and the cadres' prévoyance. No statute states those rates.
On the 3 Nov 2026 FR benchmark, 14 of 34 `not_found` runs asked for exactly such an agreement.
The scout's web search found the agreements' Légifrance `/conv_coll/` pages, but the FR id filter
dropped them, and the corpus had no way to hold them.

We decided that a collective agreement is **evidence**: the same trust class as a law, citable and
ranked like one, with no guidance finding. It is the operative text for the rates it sets, and the
critique's verbatim-extract check applies to it unchanged.

## Considered options

- **Guidance** (the class a contributed "other" document gets today). Rejected: the critique would
  report a guidance-only finding on every AGIRC-ARRCO proposal, although no higher norm exists to
  add.
- **`national_team` curation** (skip the run). Rejected: these values are written down, published
  and change every year, which is exactly what the pipeline exists to track.
- **Evidence, typed apart.** Chosen: `instrument_type = 'collective_agreement'`, so the eval can
  still count agreement-backed proposals per country.

## Consequences

- FR reads the DILA **KALI** base as its own source, `FR-KALI`. DILA publishes KALI only as dumps
  (one global tarball plus daily increments), and the Tricoteuses mirror has JORF and LEGI only.
  So the adapter keeps a local copy of the dump tree under `NOMOTHECA_KALI_DIR` (the worker's
  `kali-cache` volume, ~1.8 GB). `cli kali-sync` keeps it current, and an ingest syncs on its own
  when the copy is older than 12 h. Each document is archived as DILA JSON, the same shape
  Tricoteuses serves, so the LEGI parser reads it and `reparse` replays it.
- The scout keeps `KALITEXT`/`KALIARTI` ids and asks for the agreement when the social partners
  set the value. A `KALICONT` (a whole convention, hundreds of texts) is refused, like `LEGITEXT`.
- A contributed document gains the `collective_agreement` level in every country (FR
  `accord_collectif`, ES `convenio_colectivo`, NL `cao`, IE `employment_agreement`, LT
  `kolektyvine_sutartis`), and that level maps to evidence. "Other" stays guidance.
- Not covered: decisions of a body's board that are not agreements, such as the AGS rate set by
  the AGS board. They still go in as contributed documents, with the kind the reviewer states.
