# RAG Pipeline

Legislation database + archive-first ingester (project codename **Nomotheca**, ingest codename **Nomosync**). Design docs: [10_retrieval-strategy-challenge.md](10_retrieval-strategy-challenge.md) (why lazy RAG), [11_database-model.md](11_database-model.md) (schema), [12_ingestion-architecture.md](12_ingestion-architecture.md) (shared core / country adapter split).

## Start the stack

From the repo root (PostgreSQL + pgAdmin + Phoenix, schema and seed auto-applied):

```sh
docker compose up
```

- pgAdmin: http://localhost:5050
- Phoenix (LLM traces / evals): http://localhost:6006

## Start the ingest

```sh
cd Nomotheca-RAG/ingest
uv run python -m nomotheca_ingest.cli tui
```

Or non-interactively (jurisdiction is a generic positional — same commands for every country):

```sh
uv run python -m nomotheca_ingest.cli instrument fr JORFTEXT000051168007 -d postgresql://jrc:jrc@localhost:5434/legislation
uv run python -m nomotheca_ingest.cli instrument lt TAR.C677663D2202 -d postgresql://jrc:jrc@localhost:5434/legislation
uv run python -m nomotheca_ingest.cli country-report fr ../country_reports/Y16_CR_FR.md -d postgresql://jrc:jrc@localhost:5434/legislation
```

## Country coverage

| Country | Adapter | Fetch source | Sources analysis |
|---|---|---|---|
| FR | `countries/fr/` | Tricoteuses git mirror (DILA LEGI/JORF JSON), by direct id | [France_sources_analysis.md](France_sources_analysis.md) |
| LT | `countries/lt/` | data.gov.lt Spinta API over TAR (`Dokumentas` + `Suvestine` dated consolidations) | [Lithuania_sources_analysis.md](Lithuania_sources_analysis.md) |
| NL / ES / IE / BE | — (seed rows only) | candidates catalogued | [fiscal_law_sources.md](fiscal_law_sources.md) |

**Adding a country** is an adapter under `ingest/src/nomotheca_ingest/countries/<cc>/` plus a registry entry — core never changes. The step-by-step process (source analysis → seed rows → adapter → tests → end-to-end check, with the known gotchas) is captured in the [`add-country` skill](../.claude/skills/add-country/SKILL.md).

## Tests

```sh
cd Nomotheca-RAG/ingest
uv run pytest            # all
uv run pytest -k lt      # one country's parser/fetcher tests
```
