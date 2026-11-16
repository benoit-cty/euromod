"""A job slot survives a database it cannot reach yet (no DB)."""

from __future__ import annotations

import threading
from pathlib import Path

from nomergon import worker
from nomergon.config import WorkerConfig


def test_a_slot_whose_first_connect_fails_keeps_polling(tmp_path: Path, monkeypatch) -> None:
    attempts: list[int] = []
    stop = threading.Event()

    def unreachable(_url: str):
        attempts.append(1)
        if len(attempts) >= 3:
            stop.set()
        raise OSError("database not reachable")

    monkeypatch.setattr(worker.db, "connect", unreachable)
    cfg = WorkerConfig(repo_root=tmp_path, poll_seconds=0.01)
    slot = worker.JobSlot(cfg, stop, worker.Heartbeat(cfg, stop), 1)
    slot.run()  # in this thread: an exception would fail the test
    assert len(attempts) >= 3
