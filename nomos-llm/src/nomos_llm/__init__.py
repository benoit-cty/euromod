"""Shared base of the Nómos packages: LLM provider access and the one .env.

* `nomos_llm.providers` — provider-prefixed model strings, request settings,
  `run_agent` (used by the workflow and by the ingest package's translator);
* `nomos_llm.env` — the repo-root `.env` loader and the default database URL.
"""
