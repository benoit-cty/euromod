"""The encode lane survives a database restart (code audit D12)."""

from __future__ import annotations

import threading

from nomergon import encoder


class _Conn:
    def __init__(self, fail: bool) -> None:
        self.fail = fail
        self.closed = False

    def close(self) -> None:
        self.closed = True


def test_the_lane_reconnects_after_a_dead_connection(monkeypatch):
    stop = threading.Event()
    opened: list[_Conn] = []

    def connect(url):
        conn = _Conn(fail=not opened)  # the first connection dies, the second works
        opened.append(conn)
        return conn

    claims = []

    def claim(conn, worker_id):
        claims.append(conn)
        if conn.fail:
            raise RuntimeError("terminating connection due to administrator command")
        stop.set()
        return None

    monkeypatch.setattr(encoder.db, "connect", connect)
    monkeypatch.setattr(encoder.db, "claim_encode_job", claim)
    lane = encoder.EncodeLane.__new__(encoder.EncodeLane)
    threading.Thread.__init__(lane)
    lane.cfg = type("Cfg", (), {"database_url": "x", "worker_id": "w", "encode_poll_seconds": 0.01})()
    lane.stop_event = stop
    lane.backend = object()  # skip the model load
    lane.extra_backends = {}
    lane.load_error = None
    lane._next_load_attempt = 0.0

    lane.run()

    assert len(opened) == 2
    assert opened[0].closed  # the dead connection was dropped
    assert claims == opened
