-- 0010 — the Staatscourant as an NL source.
--
-- BWB consolidates regulations; what a Minister only announces is not in it:
-- the half-yearly «Mededeling … gewijzigde bedragen» (gross AOW and Anw
-- amounts), and the explanatory note of a regulation (the maximum daily wage).
-- Ingest: `cli instrument nl stcrt-2024-39288`. Fresh volumes get the row from
-- seed.sql. Idempotent.

INSERT INTO sources (jurisdiction_id, code, name, base_url, id_system, supports_eli, supports_point_in_time, fetch_skill, terms)
VALUES ((SELECT id FROM jurisdictions WHERE code = 'NL'), 'NL-STCRT',
        'Staatscourant (officielebekendmakingen.nl)', 'https://zoek.officielebekendmakingen.nl', 'stcrt',
        false, false, 'skills/nl-bwb',
        '{"note": "publications as published, one XML per stcrt id; regulations and notices only. A later notice replaces the amounts without marking the older one. The explanatory note is filed as a guidance instrument"}')
ON CONFLICT (code) DO NOTHING;
