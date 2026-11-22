"""A machine translation goes stale when its source text changes (needs the stack up).

Everything happens inside one transaction that is rolled back.
"""

from __future__ import annotations

import os

import psycopg
import pytest
from nomotheca_ingest.core import translate

DB_URL = os.environ.get("EUROMOD_DATABASE_URL", "postgresql://jrc:jrc@localhost:5434/legislation")


@pytest.fixture
def conn():
    try:
        connection = psycopg.connect(DB_URL, connect_timeout=2)
    except psycopg.OperationalError:
        pytest.skip("database not reachable")
    yield connection
    connection.rollback()
    connection.close()


def _translated_source(conn):
    row = conn.execute(
        """
        SELECT s.id, s.version_id FROM unit_texts e JOIN unit_texts s ON s.id = e.translation_of
        WHERE e.authenticity = 'machine_translation' AND e.lang = 'en'
          AND e.metadata ? 'source_content_hash'
        LIMIT 1
        """
    ).fetchone()
    if row is None:
        pytest.skip("no machine translation in this database")
    return row


def test_a_reparsed_source_is_translated_again(conn):
    source_id, version_id = _translated_source(conn)
    pending = {t.version_id for t in translate.iter_texts_needing_translation(conn)}
    assert version_id not in pending

    # what a reparse that changes the text does to the source row
    conn.execute("UPDATE unit_texts SET content_hash = 'changed' WHERE id = %s", (source_id,))
    stale = [t for t in translate.iter_texts_needing_translation(conn) if t.version_id == version_id]
    assert [t.id for t in stale] == [source_id]
    assert translate.count_texts_needing_translation(conn) >= 1

    # re-translating replaces the stale row in place, and the version is done again
    before = conn.execute("SELECT id FROM unit_texts WHERE version_id = %s AND lang = 'en'", (version_id,)).fetchone()[
        0
    ]
    text_id = translate.store_translation(conn, stale[0], "Fresh text.", target_lang="en", engine="test")
    assert text_id == before
    content, chunks = conn.execute(
        "SELECT t.content, count(c.id) FROM unit_texts t JOIN chunks c ON c.unit_text_id = t.id "
        "WHERE t.id = %s GROUP BY t.content",
        (text_id,),
    ).fetchone()
    assert content == "Fresh text." and chunks == 1
    assert version_id not in {t.version_id for t in translate.iter_texts_needing_translation(conn)}
