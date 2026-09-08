# 06: Légifrance ELI resolution in three tiers

**What to build:** A reviewer pastes a Légifrance ELI URL such as an arrêté cited by its `/eli/arrete/…/jo/texte` form, and the router turns it into the DILA `JORFTEXT` id so the existing FR adapter ingests the act cleanly from Tricoteuses. Resolution tries, in order: an exact match on the ELI column of instruments already in our database; an HTTP request with browser-like headers that follows the redirect and reads the final URL; on a DataDome 403, a headless browser (Playwright) opening the URL and reading the final URL. Only the final URL is ever used; no Légifrance page content is parsed or stored. Playwright is an optional `legifrance` extra of the ingester; without it the third tier is skipped and the outcome is the refusal hint. This is the FR resolver's first real implementation and is exposed for the scout to reuse later.

Decision record: docs/adr/0002.

**Blocked by:** 05 (route URLs to known official sources).

**Status:** ready-for-agent

- [ ] The FR resolver resolves an ELI-form URL (and a bare NOR) to a DILA id through the three tiers in order, stopping at the first that answers
- [ ] The database tier matches the stored ELI URL of an already-ingested instrument and returns its national id
- [ ] The HTTP tier sends browser-like headers, follows redirects, and extracts `JORFTEXT…` or `LEGIARTI…` from the final URL
- [ ] The browser tier is only attempted on a 403, only when the extra is installed, and returns nothing but the final URL
- [ ] The resolver never returns page content; a test asserts the resolver's result type carries only an id and the tier that produced it
- [ ] Routing tests inject a resolver callable standing in for the HTTP and browser tiers and cover: resolved on tier 1, tier 2, tier 3, extra absent, all tiers failing
- [ ] `pyproject` declares the `legifrance` extra; the default environment installs and runs without it
- [ ] Manual check: the arrêté ELI URL from the spec routes to the FR adapter and ingests as `arrete` with its ELI stored on the instrument; a second run resolves on the database tier without any network call
