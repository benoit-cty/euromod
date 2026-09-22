# Nomergon-worker package

Status: done (2026-09-22)
Files owned: Nomergon-worker/**, docker-compose.yml

Nomergon-worker package: ops schema apply, serve loop, encode lane, heartbeat, model publishing, Dockerfile, compose service

Contract: [../contracts.md](../contracts.md). Design: [../spec.md](../spec.md).

## Comments
- 2026-09-22, integration: a full disk during the image build took Postgres down mid-run and the worker died on an event insert, leaving the job `running`. Fixed: every bookkeeping write in `runner.py` is non-fatal (`_write`/`_note`), the cancel flag read is non-fatal, the final status is retried on a fresh connection for up to five minutes (`worker._finish_with_retry`), the heartbeat reconnects. Regression test `test_a_failing_database_does_not_kill_the_job`.
