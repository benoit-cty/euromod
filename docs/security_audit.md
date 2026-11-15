# Security audit — Nómos (EUROMOD parameter update prototype)

Date: 15 November 2026. Commit audited: `1880a77` plus the uncommitted working tree.

## Scope and method

The audit covers the whole repository: the four Python packages (`Nomotheca-RAG/ingest`, `Nomoscope-agentic-workflow/pipeline`, `Nomokrisis-evaluation_pipeline`, `Nomergon-worker`), the MCP server, the two Tauri desktop applications (`ui`, `rag-ui`), the SQL schemas and roles, the Docker/Compose files and the dependency lockfiles.

It is a source review, completed by three automated checks:

- a search of the tracked files and of the git history (235 commits) for credentials;
- `npm audit` on the two UI lockfiles;
- `pip-audit` on the locked dependency set of the worker image and of the MCP server.

No finding was exploited against the running stack. Where a finding rests on reading the code only, it says so. No code was changed.

Not covered: the Rust dependencies (`cargo audit` is not installed on this machine, see [Keeping dependencies up to date](#keeping-dependencies-up-to-date)), the content of the container images themselves, and JRC's network and hosting.

Two situations are distinguished throughout, because the severity differs:

- **Dev box**: the Compose stack as it runs today, one `jrc` superuser.
- **Shared deployment**: the target described in ADR 0004, with the roles of [roles.sql](../Nomergon-worker/db/roles.sql), several analysts and a worker that holds the provider keys.

## Summary

The design is sound where it matters most for the project: the workstation executes nothing, keys stay on the worker, SQL is parameterised everywhere, formulas and derivations are evaluated through a whitelisted AST and never `eval`, the two places that render HTML in the UIs escape their input, and no credential was found in the tracked files or in the git history.

The main weaknesses are at the edges of that design:

1. The job queue trusts its payload more than ADR 0004 intends. An analyst who can submit a job can make the worker read its own files and environment (the provider keys) into the corpus, fetch internal URLs, and run on any model whose key the worker holds.
2. The stack is published on every network interface with default credentials (`jrc`/`jrc` superuser, pgAdmin `admin`/`admin`, Phoenix without authentication).
3. The desktop applications connect to Postgres without TLS.
4. Dependencies have 42 known advisories on the Python side and 9 on the JavaScript side, and nothing checks them automatically.

| # | Finding | Dev box | Shared deployment |
|---|---------|---------|-------------------|
| 1 | An `ingest` job can read worker files and environment into the corpus | Medium | **High** |
| 2 | Stack published on all interfaces with default credentials | **High** | n/a (must not ship) |
| 3 | Desktop applications connect to Postgres without TLS | Low | **High** |
| 4 | Contributed URLs are fetched without restriction (SSRF) | Low | Medium |
| 5 | The model allow-list is not enforced by the worker | Low | Medium |
| 6 | Known vulnerabilities in dependencies | Medium | Medium |
| 7 | Worker container runs as root with every key in every subprocess | Low | Medium |
| 8 | Images and model downloads are not pinned; one model runs remote code | Low | Medium |
| 9 | The decision function stores the reviewer's item unchecked | Low | Medium |
| 10 | Any analyst can read every job payload and log, chats included | Low | Low |
| 11 | No content security policy in the two Tauri applications | Low | Low |
| 12 | KALI archive extraction does not reject `..` paths | Low | Low |
| 13 | Smaller points | Low | Low |

## Findings

### 1. An `ingest` job can read worker files and environment into the corpus

**Where:** [jobs.py](../Nomergon-worker/src/nomergon/jobs.py) (`IngestPayload.args` is a free list of strings), [cli.py](../Nomotheca-RAG/ingest/src/nomotheca_ingest/cli.py) (`document` takes "URL, or path to a file"), [contributed.py](../Nomotheca-RAG/ingest/src/nomotheca_ingest/core/contributed.py) (`read_input` reads any path).

**What:** The reviewer role may insert rows in `ops.jobs`. For an `ingest` job the worker passes `args` straight to the ingest CLI. With the `document` command, a first argument that does not start with `http` is read as a path on the worker. Any readable file is accepted (an unknown type falls back to `text/plain`), archived as a snapshot and loaded as unit texts, which every reviewer can then read with `SELECT`.

`/proc/self/environ` holds every provider key, because the container receives the whole `.env` through `env_file`. So an analyst login, or anyone who obtains one, can read the Azure, OpenRouter, Tavily and JRC gateway keys. This breaks the central promise of ADR 0004 ("keys exist on the worker only").

This was established by reading the code and was not exercised.

**Fix:**

- Replace `args: list[str]` with typed fields per command (identifier, URL, jurisdiction, kind, dates…), as the other payloads already do, and build the argv in the worker.
- Refuse a local path in a job. A file an analyst contributes should travel as content in the payload, the way `draft-golden` already sends `text`.
- Put `--` before positional values when building any argv, so that a value starting with `-` is never read as an option (`targets`, `country`, `notes`, `resume` are affected in the same way, with less impact).

### 2. Stack published on all interfaces with default credentials

**Where:** [docker-compose.yml](../docker-compose.yml). Confirmed on this machine: ports 5434, 5050, 6006 and 4317 listen on `0.0.0.0` and `[::]`.

**What:** Anyone on the same network can:

- connect to Postgres as the superuser `jrc`/`jrc`. A superuser can run programs in the database container (`COPY … FROM PROGRAM`), rewrite decisions and audit rows, and submit jobs, which leads to finding 1 and the provider keys;
- log in to pgAdmin as `admin@euromod.eu`/`admin`, where the database password is pre-loaded from the tracked [pgpass](../Nomotheca-RAG/db/pgadmin/pgpass);
- read every prompt and model answer in Phoenix, and post false traces to it, without any login.

Docker publishes ports ahead of the host firewall (`ufw` rules do not apply to them), so a firewall on the dev box does not help.

**Fix:**

- Bind the ports to the loopback interface: `"127.0.0.1:5434:5432"`, and likewise for 5050, 6006, 4317.
- Read `POSTGRES_PASSWORD` and the pgAdmin password from `.env` instead of the Compose file, with no default for a shared deployment.
- For the shared deployment: do not deploy pgAdmin; enable Phoenix authentication (`PHOENIX_ENABLE_AUTH`, `PHOENIX_SECRET`) or keep it on an internal network; apply `roles.sql` so that no application uses a superuser.

### 3. Desktop applications connect to Postgres without TLS

**Where:** `Client::connect(db_url, NoTls)` in [db.rs](../Nomoscope-agentic-workflow/ui/src-tauri/src/db.rs), [store.rs](../Nomoscope-agentic-workflow/ui/src-tauri/src/store.rs), [jobs.rs](../Nomoscope-agentic-workflow/ui/src-tauri/src/jobs.rs), [golden.rs](../Nomoscope-agentic-workflow/ui/src-tauri/src/golden.rs); `rag-ui` compiles the same files.

**What:** The `postgres` crate is built without a TLS connector, so the applications cannot encrypt the connection. On the dev box the database is local and this does not matter. In the shared deployment the analyst's password exchange, every decision and all the data cross the network in clear text, and the application would simply fail against a server that requires TLS.

The analyst's database URL, password included, is read from the `WORKFLOW_DATABASE_URL` environment variable, and falls back to `jrc:jrc@localhost:5434` when it is unset.

**Fix:** Add `postgres-native-tls` or `tokio-postgres-rustls` and connect with certificate verification; require `hostssl` in `pg_hba.conf` on the server. Remove the `jrc:jrc` fallback from release builds and keep the password in the operating system's keychain, or use an authentication the workstation already has (Kerberos/GSSAPI, client certificate).

The Python side uses psycopg, which follows `sslmode` in the URL: set `sslmode=verify-full` in `WORKER_DATABASE_URL` for the shared deployment.

### 4. Contributed URLs are fetched without restriction (SSRF)

**Where:** `read_input` and `fetch_in_browser` in [contributed.py](../Nomotheca-RAG/ingest/src/nomotheca_ingest/core/contributed.py).

**What:** An `ingest`/`document` job fetches any `http(s)` URL from inside the worker, follows redirects, and stores the response where reviewers can read it. The worker sits inside the hosting network, so this reaches addresses an analyst's workstation cannot: `http://phoenix:6006`, a cloud metadata service (`169.254.169.254`), internal JRC services. A `.pdf` URL that answers with HTML is also opened in a headless Firefox.

The scout's own web discoveries are restricted to listed official domains and URL patterns, which is good; the restriction is missing only on the path a reviewer (or a forged job) uses.

**Fix:** Before fetching, resolve the host and refuse loopback, private, link-local and container-network addresses; check again after each redirect. Consider a fixed egress proxy for the worker, which also gives JRC one place to log and limit outbound traffic. Set a maximum response size.

### 5. The model allow-list is not enforced by the worker

**Where:** [jobs.py](../Nomergon-worker/src/nomergon/jobs.py) (every `model` field is a free string), [runner.py](../Nomergon-worker/src/nomergon/runner.py).

**What:** `ops.worker_models` is what the UI offers, but the worker never checks a job's `model` against it. A job inserted directly can name any provider and model for which a key is present in the worker's environment. The consequences are cost (an expensive model, large `eval` runs), and legislation queries or draft documents sent to a provider JRC did not approve. There is also no limit on how many billed jobs a login may queue, nor on the `priority` it gives them.

**Fix:** In `parse_payload`, refuse a `model` that is not in `cfg.models` (plus `mock/…`). Add a check constraint or the RLS policy `priority <= 50` for reviewers, and a per-user cap on queued jobs.

### 6. Known vulnerabilities in dependencies

Result of the scans on 15 November 2026.

**Python, worker image** (110 locked packages, `cpu` extra; `torch` could not be audited because it comes from the PyTorch index):

| Package | Locked | Advisories | Fixed in | Relevance here |
|---------|--------|-----------:|----------|----------------|
| `pypdf` | 6.19.0 | 18 | 6.21.4 | **High**: parses PDFs fetched from the web and contributed by users |
| `transformers` | 5.0.0 | 4 | 5.10.0 (one without fix) | Medium: loads models from the Hugging Face hub |
| `pydantic-ai-slim` | 2.47.0 | 2 | 2.53.0 | Medium: every model call |
| `filelock` | 4.0.1 | 14 | 4.2.1 | Low |
| `opentelemetry-api` | 1.44.0 | 2 | 1.45.2 | Low |
| `certifi` | 2026.7.22 | 1 | 2026.10.18 | Low: root certificate list |
| `setuptools` | 84.0.0 | 1 | 84.1.0 | Low: build time |

**Python, MCP server:** `pyjwt` 2.13.0, 15 advisories, fixed in 2.15.0. It arrives through `mcp`; the server runs over stdio and does not use JWT, so the exposure is low.

**JavaScript:** `ui` has 9 advisories (5 high), `rag-ui` 5 (1 high). All are in the build chain (`vite` 5.4.21, `esbuild`, `postcss`, `nanoid`, `devalue`, `source-map-js`), none in the code shipped inside the application. The `vite`/`esbuild` one lets a web page read from the dev server while `npm run tauri dev` is running. Four are fixed by `npm audit fix`; the others need `vite` 7 and `@sveltejs/vite-plugin-svelte` 6.

**Rust:** not scanned.

**Fix:** see the upgrade commands in the last section. `pypdf` first.

### 7. Worker container runs as root with every key in every subprocess

**Where:** [Dockerfile](../Nomergon-worker/Dockerfile) (no `USER`), [runner.py](../Nomergon-worker/src/nomergon/runner.py) (`job_environment` copies the whole environment), `env_file` in [docker-compose.yml](../docker-compose.yml).

**What:**

- The worker and its jobs run as root, with a writable root filesystem and the default capabilities (confirmed with `docker inspect`). The jobs parse untrusted PDFs, HTML and XML and drive two headless browsers, so a parser or browser flaw gives root in the container.
- Every subprocess inherits every key, including ones it does not need (an `embed` job gets the Azure key).
- The local `.env` also carries keys the project no longer uses (`LANGCHAIN_API_KEY`, `LANGSMITH_API_KEY`, `GOOGLE_SEARCH_API_KEY`, `GOOGLE_AI_STUDIO_API_KEY`). They are injected into the container all the same. The file's mode is 664, readable by every local user.
- The database URL with its password is passed as `--database-url` on the command line of ingest jobs, visible in the process list. The job log redacts it correctly.

**Fix:** Add a non-root `USER` to the image, `cap_drop: [ALL]`, `security_opt: [no-new-privileges:true]`, and a read-only root filesystem with the two volumes and a `tmpfs` for `/tmp`. Pass each job only the variables its type needs. Remove the unused keys from `.env` (and revoke them if they are no longer needed anywhere), then `chmod 600 .env`. Let the ingest CLI read the URL from `EUROMOD_DATABASE_URL`, which the runner already sets.

### 8. Images and model downloads are not pinned; one model runs remote code

**Where:** [docker-compose.yml](../docker-compose.yml) (`dpage/pgadmin4:latest`, `arizephoenix/phoenix:latest`, `pgvector/pgvector:pg17`), [Dockerfile](../Nomergon-worker/Dockerfile) (`python:3.13-slim-bookworm`, `ghcr.io/astral-sh/uv:0.12`), [embedding_models.py](../Nomotheca-RAG/ingest/src/nomotheca_ingest/core/embedding_models.py).

**What:** `latest` and moving tags mean two builds of the same commit can differ, and a compromised or broken upstream image is pulled without review. Embedding models are downloaded from the Hugging Face hub with no `revision`, and model 8 (`Alibaba-NLP/gte-multilingual-base`) sets `trust_remote_code=True`: Python code from that repository runs in the worker, which holds the keys. An `embed` job with `model_id: 8` is enough to trigger the download.

A related trust point, not a defect: French texts come from `git.tricoteuses.fr`, a third-party mirror of DILA. The integrity of the French corpus depends on it. The snapshot archive records what was received, which is the right mitigation; a periodic comparison of a sample with Légifrance would complete it.

**Fix:** Pin every image to a version and a digest (`image@sha256:…`). Pin a `revision` (commit hash) for each embedding model in the registry, and either drop model 8 from the worker's registry or pin its revision after reading the code. For the shared deployment, pre-load the models into the `hf-cache` volume and set `HF_HUB_OFFLINE=1`.

### 9. The decision function stores the reviewer's item unchecked

**Where:** `params.decide_review_item` in [params_schema.sql](../Nomoscope-agentic-workflow/pipeline/db/params_schema.sql); grants in [roles.sql](../Nomergon-worker/db/roles.sql).

**What:** The function is the only way an analyst changes a queue row, which is right. But it stores `p_item` as given, and takes `decided_at` from the caller. An analyst who calls it with their own SQL client, rather than through the UI, can:

- replace the whole item — proposed value, citations, critique verdict — while recording a plain "accepted";
- accept an item the UI refuses to accept (the `provisional` routing is blocked in the UI only);
- decide again on an item that was already reviewed, and back-date the decision.

The reviewer name is safe (`session_user`). The audit table is append-only for the reviewer role, so the record of *who* decided holds; what is not guaranteed is that the item in the queue is the one the pipeline produced.

Also: `EXECUTE` on this function is not revoked from `PUBLIC` (it is for `edit_parameter`), and both functions set `search_path = params, public` without a trailing `pg_temp`. The column grant on `eval.golden_cases` lets a reviewer write any name in `reviewed_by`; only the UI sets it to `current_user`.

**Fix:** Have the function take the decision only (action, note, edited value) and compute the new item itself from the stored one; refuse `accepted` on a `provisional` item and a second decision without an explicit flag; set `decided_at = now()`. Add `REVOKE EXECUTE … FROM PUBLIC`, and `pg_temp` at the end of both `search_path` settings. Set `reviewed_by` in a trigger.

### 10. Any analyst can read every job payload and log, chats included

**Where:** policy `jobs_reviewer_read … USING (true)` in [roles.sql](../Nomergon-worker/db/roles.sql); `ops.job_events` has no row-level security.

**What:** A `chat` job's payload is the whole conversation, and a `draft-golden` job's payload may be a full document. Every analyst can read every other analyst's. Job logs are shared in the same way; a provider error printed on stderr lands there.

This may be the intended behaviour for a small team. It should be a stated decision.

**Fix (if not intended):** restrict the read policy to `submitted_by = current_user` for the `chat` type, and apply the same rule to `ops.job_events` through the job.

### 11. No content security policy in the two Tauri applications

**Where:** `"csp": null` in [ui tauri.conf.json](../Nomoscope-agentic-workflow/ui/src-tauri/tauri.conf.json) and [rag-ui tauri.conf.json](../Nomoscope-agentic-workflow/rag-ui/src-tauri/tauri.conf.json).

**What:** The two places that inject HTML were checked and are safe today: `SourceViewer.svelte` escapes the legal text before highlighting, and `rag-ui/src/lib/markdown.js` escapes everything first and only allows `http(s)` links. The shell plugin's default scope opens only `http(s)`, `mailto` and `tel` links. The capabilities are minimal.

With no CSP, a single future mistake in one of those renderers would let text from a web page or a model answer run script inside a window that can call every Tauri command, including the ones that record decisions.

**Fix:** set a policy such as `default-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src ipc: http://ipc.localhost`.

### 12. KALI archive extraction does not reject `..` paths

**Where:** `KaliStore._apply` and `_kept_relative` in [kali.py](../Nomotheca-RAG/ingest/src/nomotheca_ingest/countries/fr/kali.py).

**What:** Members are written by hand, and only regular files, which avoids the usual `extractall` problems with links. But the path kept after `kali/global/` is joined to the local tree without checking for `..`, and the deletion list is handled the same way. A crafted archive could write or delete a file outside the cache directory. This needs a compromised DILA server or mirror, so the likelihood is low.

**Fix:** resolve the target and refuse it unless it is inside `self.tree`.

### 13. Smaller points

- **XML parsing** uses the standard library's `ElementTree` on downloaded documents (ES, NL, IE, KALI). It does not load external entities, so there is no file disclosure; a deliberately nested document could exhaust memory. `defusedxml` removes the doubt at no cost.
- **No size or time limit on parsing.** A very large or malformed PDF can hold a job slot. The scout has subprocess timeouts; a job submitted directly has none.
- **Prompt injection.** Web search results and ingested texts reach the models. The exposure is well contained: web text is never evidence, the chat agent's tools only read, every quote is checked character for character against the corpus, and nothing is written to EUROMOD without a human. The residual risk is a misleading answer in the chat, not an action.
- **`pytest` is a runtime dependency** of `nomotheca-legislation-ingest` and therefore ships in the worker image. Move it to a dev group.
- **No `.dockerignore`.** The build context is the repository root, which contains `.env`. The Dockerfile copies four directories only, so the file is not in the image today; a `.dockerignore` listing `.env`, `.git`, `.venv*` and `node_modules` makes that robust.
- **Tracked files to tidy:** [2026-11-03-…txt](../2026-11-03-161253-we-will-do-a-demo-of-the-tool-in-two-weeks-the-t.txt) (an assistant session transcript at the repository root), `Nomotheca-RAG/ingest/_probe_tokenizer.py` (marked "safe to delete"), and `.claude/settings.json`, which allows `Bash(docker exec *)` to an AI assistant without confirmation — with a superuser database behind it, that is a broad permission to keep in a shared repository.
- **Old references in the local `.env`:** it still contains LangSmith keys, although the project states it does not use LangSmith.

## What was checked and found sound

- **No credential in git.** Neither the tracked files nor the history contain a key; `.env` is ignored and was never committed. The only tracked passwords are the documented dev defaults (`jrc`/`jrc`, `admin`/`admin`).
- **SQL injection.** Python uses bound parameters throughout; the few formatted statements insert fixed fragments, never input. The Rust code uses `$n` parameters; `format!` only inserts constant column lists.
- **No dynamic code execution.** No `eval`, `exec`, `pickle`, `yaml.load` or `shell=True`. Derivations and EUROMOD formulas go through AST evaluators limited to `+ - * /` (no power operator, so no arithmetic blow-up).
- **Subprocesses** are always argv lists started from the worker's own interpreter.
- **The workstation holds no key and starts no process**, as ADR 0004 requires; Tauri capabilities are limited to core, dialog and opening a link.
- **The MCP server** is read-only, over stdio, with parameterised queries.
- **Reviewer identity** in decisions and edits is `session_user`, which a caller cannot choose.
- **Job log redaction** of the database password works.

## Recommended order of work

Before any shared deployment:

1. Type the `ingest` payload and refuse local paths (finding 1); enforce the model list (5).
2. TLS between the desktop applications and Postgres; no default credential in a release build (3).
3. Apply `roles.sql`; no superuser for any application; Phoenix behind authentication; no pgAdmin (2).
4. Non-root, capability-free worker container; per-job environment (7).
5. Block internal addresses for contributed URLs (4).

Now, on the dev box (each is a small change):

6. Bind the published ports to `127.0.0.1` (2).
7. Upgrade `pypdf`, then the other flagged packages (6).
8. Remove unused keys from `.env`, `chmod 600 .env` (7).
9. Pin image versions (8).

Then: findings 9 to 13, and the automation below.

## Keeping dependencies up to date

The project has five Python lockfiles (`uv.lock`), two `package-lock.json`, two `Cargo.lock`, three public container images and one Dockerfile. All the lockfiles are tracked in git, which is the right basis: an update is always a reviewable diff of a lockfile.

Nothing updates or checks them automatically today (there is no CI workflow, no Dependabot or Renovate configuration).

### By hand

**Python (uv).** In each of `Nomergon-worker`, `Nomotheca-RAG/ingest`, `Nomoscope-agentic-workflow/pipeline`, `Nomokrisis-evaluation_pipeline`, `mcp-server`:

```bash
uv lock --upgrade                      # everything, within the ranges of pyproject.toml
uv lock --upgrade-package pypdf        # one package only
uv sync && uv run pytest               # install and test
```

`Nomergon-worker/uv.lock` is the one the worker image is built from (`uv sync --frozen`). It resolves the three other packages as path dependencies, so it must be re-locked whenever one of them changes its dependencies. Then rebuild and recreate the worker without restarting the database:

```bash
docker compose --profile gpu build worker
docker compose --profile gpu up -d --no-deps worker
```

To see what is outdated and what is vulnerable:

```bash
uv tree --outdated --depth 1
uv export --frozen --no-dev --extra cpu --no-emit-project --no-hashes -o /tmp/req.txt
uvx pip-audit -r /tmp/req.txt --no-deps --disable-pip
```

`torch` comes from the PyTorch index and is not covered by `pip-audit`; follow its release notes. The `cu126` wheels are tied to the GTX 1080 Ti, so upgrade `torch` deliberately and test an embedding build afterwards.

**JavaScript (npm).** In `Nomoscope-agentic-workflow/ui` and `rag-ui`:

```bash
npm outdated
npm update            # within the ^ranges of package.json
npm audit             # known vulnerabilities
npm audit fix         # the ones with a compatible fix
npm test && npm run build
```

Major versions (`vite` 5 → 7, `@sveltejs/vite-plugin-svelte` 4 → 6) need an edit of `package.json` and a manual check of the application. The `@tauri-apps/*` npm packages must stay on the same minor version as the Rust `tauri` crates: update both sides together.

**Rust (cargo).** In each `src-tauri`:

```bash
cargo update                          # within the ranges of Cargo.toml
cargo install cargo-audit --locked    # once
cargo audit                           # known vulnerabilities (RustSec)
cargo test
```

`cargo install cargo-outdated` adds `cargo outdated` for the versions beyond the declared ranges.

**Container images.** Replace `latest` with an explicit version in `docker-compose.yml`, then update that version on purpose:

```bash
docker compose pull && docker compose up -d
docker compose --profile gpu build --pull worker     # refreshes the Python base image
```

Scan the built image from time to time: `trivy image nomergon-worker` (or `docker scout cves nomergon-worker`). This also covers the system packages and the Playwright browsers, which no lockfile describes. Playwright downloads the browser build that matches its Python package, so upgrading `playwright` is what updates Chromium and Firefox.

**Models.** Once revisions are pinned in `embedding_models.py` (finding 8), a model update is a change of that hash, followed by a rebuild of the vectors for that `model_id`.

### Automatically

Two additions cover most of the work.

**1. Renovate or Dependabot on the repository.** Either one opens a pull request when a new version or a security fix exists. Both understand `uv.lock`, `package-lock.json`, `Cargo.lock`, Dockerfiles and Compose files. A minimal `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: uv
    directories:
      - /Nomergon-worker
      - /Nomotheca-RAG/ingest
      - /Nomoscope-agentic-workflow/pipeline
      - /Nomokrisis-evaluation_pipeline
      - /mcp-server
    schedule: { interval: weekly }
    groups:
      python: { patterns: ["*"], update-types: [minor, patch] }
  - package-ecosystem: npm
    directories:
      - /Nomoscope-agentic-workflow/ui
      - /Nomoscope-agentic-workflow/rag-ui
    schedule: { interval: weekly }
    groups:
      js: { patterns: ["*"], update-types: [minor, patch] }
  - package-ecosystem: cargo
    directories:
      - /Nomoscope-agentic-workflow/ui/src-tauri
      - /Nomoscope-agentic-workflow/rag-ui/src-tauri
    schedule: { interval: weekly }
  - package-ecosystem: docker
    directory: /Nomergon-worker
    schedule: { interval: weekly }
  - package-ecosystem: docker-compose
    directory: /
    schedule: { interval: weekly }
```

Grouping keeps it to a few pull requests a week. Also enable "Dependabot alerts" and "secret scanning" in the repository settings; they need no file. If the code moves to a JRC forge without Dependabot, Renovate does the same job and can be self-hosted.

Because the worker lockfile depends on the three other packages, a Python update pull request should re-lock `Nomergon-worker` as well. Renovate handles this with a `postUpgradeTasks` command; with Dependabot, do it by hand before merging.

**2. A CI workflow** that runs on every pull request and once a week:

- the test suites listed in `CLAUDE.md` (the mock-model ones need no key);
- `uvx pip-audit` on the export of each lockfile, `npm audit --audit-level=high`, `cargo audit`;
- `trivy image` on the built worker image, weekly.

The weekly run matters as much as the pull-request run: a vulnerability is usually published after the version was locked, with no change in the repository to trigger a check.

### Suggested routine

- **Weekly:** merge the grouped minor/patch pull requests once the tests pass.
- **On a security alert:** upgrade that package the same week; `pypdf`, `transformers`, `pydantic-ai`, `httpx`, `playwright` and `psycopg` are the ones that touch untrusted input or credentials.
- **Quarterly:** major versions (Vite, Svelte plugin, Tauri, Python base image, Postgres/pgvector image, torch), each with a full evaluation run before and after, since a model-library change can move the scores.
- **After every Python update:** rebuild the worker image, and recreate the worker with `--no-deps`.
