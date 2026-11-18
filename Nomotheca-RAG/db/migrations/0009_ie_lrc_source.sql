-- 0009 — the Law Reform Commission's Revised Acts as an IE source.
--
-- eISB serves acts as enacted only; the LRC publishes the consolidated text of
-- about 580 acts, the Social Welfare Consolidation Act 2005 among them
-- (ingest: `cli instrument ie 2005/act/26/revised`). Fresh volumes get the
-- row from seed.sql. Idempotent.

INSERT INTO sources (jurisdiction_id, code, name, base_url, id_system, supports_eli, supports_point_in_time, fetch_skill, terms)
VALUES ((SELECT id FROM jurisdictions WHERE code = 'IE'), 'IE-LRC',
        'Law Reform Commission, Revised Acts', 'https://revisedacts.lawreform.ie', 'eisb',
        true, false, 'skills/ie-eisb',
        '{"note": "administrative consolidation of about 580 acts, one HTML page per act, current state only; a section is dated by its latest F-note. Covers the Social Welfare Consolidation Act 2005, not the Taxes Consolidation Act 1997"}')
ON CONFLICT (code) DO NOTHING;
