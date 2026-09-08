---
status: accepted
date: 2026-09-08
---

# Légifrance ELI URLs are resolved to their DILA id, with a browser fallback, and never fetched for text

The project never fetches text from legifrance.gouv.fr: it is DataDome-protected, and the FR
adapter reads DILA JSON from Tricoteuses keyed by an 18-character `JORFTEXT`/`LEGIARTI` id.
ELI-form Légifrance URLs (`/eli/arrete/2020/12/28/CCPD2036946A/jo/texte`) carry a NOR, not a
DILA id, and no offline lookup exists (Tricoteuses is id-keyed, Moulineuse indexes by code and
article). Légifrance itself redirects an ELI URL to `/jorf/id/JORFTEXT…`. We decided the
contributed-document router resolves such URLs in three tiers: match `instruments.eli` in our
own database; otherwise follow the HTTP redirect with browser-like headers; otherwise, on a
DataDome 403, open the URL in a headless browser (Playwright) to read the final URL. The
resolved id is handed to the existing FR adapter. **Only the id is taken**; no Légifrance HTML
is ever parsed or stored, so the canonical-citation-URL role of Légifrance is unchanged.

## Considered options

- Refuse ELI URLs and ask the reviewer to paste the id: rejected because ELI is the form
  reviewers and official documents actually cite, and the redirect is available.
- Treat the page as a contributed document: rejected because it would fetch Légifrance for
  text and store the same act under two identities once the adapter ingests it.

## Consequences

- Playwright and a Chromium build become an optional extra of the ingester, used only by the
  FR resolver; the CPU-only default environment must keep working without it.
- The FR resolver stub gains its first real implementation (ELI or NOR URL to DILA id); the
  scout, which today drops ELI-only URLs silently, can reuse it later.
