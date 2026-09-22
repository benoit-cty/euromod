-- Nomergon: the job table that is the only channel between the workstation
-- (validation UI, developer CLIs, MCP server) and the worker. ADR 0004.
--
-- Applied idempotently by `nomergon init-db` and by the worker at startup; also
-- mounted into the dev stack's docker-entrypoint-initdb.d. Roles, grants and
-- row-level security live in roles.sql (they name cluster-level roles).

CREATE SCHEMA IF NOT EXISTS ops;

-- One row per job. The UI inserts, the worker claims and completes.
--   priority: higher first; the `encode` lane uses 100, everything else 0
--   status:   queued -> running -> succeeded | failed | cancelled
--   payload:  structured per job_type (validated by the worker, see
--             nomergon/jobs.py); the UI only ever describes a job
--   progress: the latest `@progress {json}` line the subprocess printed
--   result:   job-type specific (encode: {"halfvec": "[...]"}; impact: the
--             report; workflow: {"item_ids": [...]})
CREATE TABLE IF NOT EXISTS ops.jobs (
    id               bigserial PRIMARY KEY,
    job_type         text NOT NULL CHECK (job_type IN (
                         'workflow', 'ingest', 'embed', 'translate', 'translate-params',
                         'encode', 'eval', 'draft-golden', 'impact')),
    payload          jsonb NOT NULL DEFAULT '{}'::jsonb,
    priority         smallint NOT NULL DEFAULT 0,
    status           text NOT NULL DEFAULT 'queued' CHECK (status IN (
                         'queued', 'running', 'succeeded', 'failed', 'cancelled')),
    submitted_by     text NOT NULL DEFAULT current_user,
    submitted_at     timestamptz NOT NULL DEFAULT now(),
    started_at       timestamptz,
    finished_at      timestamptz,
    worker_id        text,
    cancel_requested boolean NOT NULL DEFAULT false,
    progress         jsonb,
    result           jsonb,
    error            text
);
CREATE INDEX IF NOT EXISTS jobs_queued_idx ON ops.jobs (priority DESC, id) WHERE status = 'queued';
CREATE INDEX IF NOT EXISTS jobs_submitted_idx ON ops.jobs (submitted_by, submitted_at DESC);
CREATE INDEX IF NOT EXISTS jobs_running_idx ON ops.jobs (worker_id) WHERE status = 'running';

-- Log lines and progress events, appended by the worker, polled by the UI
-- (`WHERE job_id = $1 AND id > $last ORDER BY id`). stream: stdout | stderr |
-- system (worker-side notes: started, killed, exit code) | progress (`data`
-- holds the parsed JSON, `line` the raw text). Pruned after 30 days.
CREATE TABLE IF NOT EXISTS ops.job_events (
    id       bigserial PRIMARY KEY,
    job_id   bigint NOT NULL REFERENCES ops.jobs(id) ON DELETE CASCADE,
    at       timestamptz NOT NULL DEFAULT now(),
    stream   text NOT NULL CHECK (stream IN ('stdout', 'stderr', 'system', 'progress')),
    line     text NOT NULL,
    data     jsonb
);
CREATE INDEX IF NOT EXISTS job_events_job_idx ON ops.job_events (job_id, id);
-- The 30-day prune deletes by age; keep it an index range scan, not a table walk.
CREATE INDEX IF NOT EXISTS job_events_at_idx ON ops.job_events (at);

-- Heartbeat. One row per worker process; a `running` job whose worker's
-- heartbeat is stale is marked failed at the next worker start (no requeue).
CREATE TABLE IF NOT EXISTS ops.workers (
    worker_id      text PRIMARY KEY,
    hostname       text NOT NULL,
    started_at     timestamptz NOT NULL DEFAULT now(),
    heartbeat_at   timestamptz NOT NULL DEFAULT now(),
    current_job_id bigint,
    device         text,                  -- 'cuda:NVIDIA GeForce ...' | 'cpu'
    version        text
);

-- The models the worker is configured to serve (WORKER_MODELS), published at
-- startup. The UI's model picker reads this and offers nothing else.
CREATE TABLE IF NOT EXISTS ops.worker_models (
    model        text PRIMARY KEY,           -- provider-prefixed: 'jrc/mistral-small-3.2'
    kind         text NOT NULL CHECK (kind IN ('llm', 'embedding')),
    is_default   boolean NOT NULL DEFAULT false,
    published_by text NOT NULL,              -- worker_id
    published_at timestamptz NOT NULL DEFAULT now()
);
