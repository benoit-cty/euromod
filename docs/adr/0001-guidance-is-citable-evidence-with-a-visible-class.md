---
status: accepted
date: 2026-09-08
---

# Administrative guidance is citable evidence, labelled by a source-trust class

The pilot's rule was "Legislation is King": only national legislation could be cited by
`propose`/`critique`, Country Reports were context, and administrative guidance (circulars,
BOFiP doctrine) was not ingested at all. Reviewers now add such documents by hand as
contributed documents, and many EUROMOD values (unemployment insurance, quotient rules) exist
only in them. We decided that guidance **is** citable evidence, on equal footing in retrieval,
but that every instrument carries a **source-trust class** (`evidence`, `guidance`, `context`)
stored in its own column, that each citation carries that class, that the critique records an
informational finding when a proposal is supported by guidance only, and that the UI shows it.
Accept is not blocked by that finding.

## Considered options

- Guidance as evidence indistinguishable from statute: simplest, but silently erases the
  hierarchy of norms from every decision record and from the evaluation data.
- Guidance as context only, like Country Reports: retrievable for framing, never citable.
  Rejected because it would make the feature useless for exactly the values it exists for.
- Route guidance-only proposals to `provisional` with Accept blocked: rejected because for a
  circular-governed scheme the circular is the operative text and there is no statute to add.

## Consequences

- The Country Report exclusion in evidence retrieval becomes `source_trust_class <> 'context'`
  instead of a compare on `instrument_type = 'country_report'`; existing databases need a
  backfill migration.
- The class is derived mechanically from the kind the reviewer states (statute, government
  regulation, ministerial order are evidence; administrative guidance and "other" are
  guidance). "Other" deliberately never grants evidence-level trust.
- The evaluation pipeline can count guidance-only acceptances per language and model, which is
  the data on which the equal-ranking choice should be revisited.
