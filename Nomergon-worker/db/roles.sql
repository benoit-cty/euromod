-- Least-privilege roles for a shared deployment (it_needs_for_deployment.md §4).
-- Run once by a DBA after every schema has been applied (schema.sql,
-- params_schema.sql, eval_schema.sql, ops_schema.sql). Idempotent.
--
--   nomos_admin     owner of the schemas, runs migrations (not created here)
--   nomos_worker    the worker: full DML everywhere
--   nomos_reviewer  group role (NOLOGIN): what the validation UI, the MCP
--                   server and a developer's read-only tooling may do
--   <analyst>       one LOGIN role per analyst, IN ROLE nomos_reviewer
--
-- The UI writes exactly three things: a human decision (through
-- params.decide_review_item, SECURITY DEFINER, so it needs no UPDATE on the
-- queue), a job request, and a golden-case verdict. Everything else is a read.

DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'nomos_worker') THEN
        CREATE ROLE nomos_worker LOGIN;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'nomos_reviewer') THEN
        CREATE ROLE nomos_reviewer NOLOGIN;
    END IF;
END $$;

-- ---------------------------------------------------------------- worker ----
GRANT CONNECT ON DATABASE legislation TO nomos_worker;
GRANT USAGE ON SCHEMA public, params, eval, ops TO nomos_worker;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public, params, eval, ops TO nomos_worker;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public, params, eval, ops TO nomos_worker;
ALTER DEFAULT PRIVILEGES IN SCHEMA public, params, eval, ops
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO nomos_worker;
ALTER DEFAULT PRIVILEGES IN SCHEMA public, params, eval, ops
    GRANT USAGE, SELECT ON SEQUENCES TO nomos_worker;

-- -------------------------------------------------------------- reviewer ----
GRANT CONNECT ON DATABASE legislation TO nomos_reviewer;
GRANT USAGE ON SCHEMA public, params, eval, ops TO nomos_reviewer;
GRANT SELECT ON ALL TABLES IN SCHEMA public, params, eval, ops TO nomos_reviewer;
ALTER DEFAULT PRIVILEGES IN SCHEMA public, params, eval, ops GRANT SELECT ON TABLES TO nomos_reviewer;

-- a decision: only through the function (inserts the audit row and updates the
-- queue item in one transaction; refuses if the item is unknown)
GRANT EXECUTE ON FUNCTION params.decide_review_item(text, jsonb, jsonb) TO nomos_reviewer;

-- a job: insert, read, cancel one's own
GRANT INSERT ON ops.jobs TO nomos_reviewer;
GRANT UPDATE (cancel_requested) ON ops.jobs TO nomos_reviewer;
GRANT USAGE, SELECT ON SEQUENCE ops.jobs_id_seq TO nomos_reviewer;

-- a golden-case verdict
GRANT UPDATE (verified, reviewed_by, reviewed_at, review_note, updated_at) ON eval.golden_cases TO nomos_reviewer;

-- ------------------------------------------------------ row-level security ----
ALTER TABLE ops.jobs ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS jobs_worker_all ON ops.jobs;
CREATE POLICY jobs_worker_all ON ops.jobs TO nomos_worker USING (true) WITH CHECK (true);
DROP POLICY IF EXISTS jobs_reviewer_read ON ops.jobs;
CREATE POLICY jobs_reviewer_read ON ops.jobs FOR SELECT TO nomos_reviewer USING (true);
DROP POLICY IF EXISTS jobs_reviewer_submit ON ops.jobs;
CREATE POLICY jobs_reviewer_submit ON ops.jobs FOR INSERT TO nomos_reviewer
    WITH CHECK (submitted_by = current_user AND status = 'queued' AND worker_id IS NULL);
DROP POLICY IF EXISTS jobs_reviewer_cancel ON ops.jobs;
CREATE POLICY jobs_reviewer_cancel ON ops.jobs FOR UPDATE TO nomos_reviewer
    USING (submitted_by = current_user) WITH CHECK (submitted_by = current_user);

-- ------------------------------------------------------------- analysts ----
-- One login per analyst. Example (replace name and password):
--   CREATE ROLE alice LOGIN PASSWORD '…' IN ROLE nomos_reviewer;
-- The MCP server and any read-only developer tooling use a login of the same
-- shape; nothing but the worker ever holds nomos_worker.
