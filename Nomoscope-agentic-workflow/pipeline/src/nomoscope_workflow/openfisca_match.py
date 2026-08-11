"""Suggest EUROMOD <-> external-corpus links (params.parameter_links).

Step 3 of the build order in Param_Schema/openfisca_france_usage.md. Two
producers, both writing the same table:

- `fingerprint_candidates` — the deterministic signal. Both sides hold
  multi-year numeric histories; a link is proposed when the same value appears
  in the same year on both sides for at least `min_years` years. No language
  dependence, so it generalises to any country package.
- `seed_links` — hand-curated pairs from a JSON file, stored as
  `match_method='manual'`. Needed wherever no fingerprint can exist: derived
  constants (EUROMOD's `$tsc_group2_lim` is 3x the monthly PSS, hence
  `factor`), and parameters whose EUROMOD series is flat while the external
  one is a bracket component.

Nothing here is authoritative: every row is a *suggestion* until a human sets
`validated_by`. The eval golden set (nomokrisis-eval build-openfisca-dataset)
reads these links and re-derives the expected value from `temporal_basis`, so a
wrong link surfaces as a bad case in review, never as a silent scoring error.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import psycopg

# EUROMOD system year Y is compared against the external date key Y + offset.
# OpenFisca dates income-tax parameters by income year while the EUROMOD FR
# connector exports the schedule applied in the system year (on the previous
# year's income), so the same parameter can line up one year apart.
DEFAULT_OFFSETS = (0, -1, 1)


@dataclass(frozen=True)
class LinkCandidate:
    parameter_id: int
    model_target: str
    external_parameter_id: int
    path: str
    component: str
    factor: float
    year_offset: int
    matched_years: int
    euromod_years: int
    score: float
    match_method: str = "fingerprint"
    note: str | None = None


_FINGERPRINT_SQL = """
WITH em AS (
    SELECT p.id AS parameter_id, p.model_target, mv.system_year AS yr, mv.value_numeric AS v
    FROM params.parameters p
    JOIN params.model_values mv ON mv.parameter_id = p.id
    WHERE p.country = %(country)s
      AND mv.value_numeric IS NOT NULL
      AND mv.system_year IS NOT NULL
      AND mv.value_numeric <> 0
), em_total AS (
    SELECT parameter_id, count(DISTINCT yr) AS n FROM em GROUP BY 1
), ext AS (
    SELECT ep.id AS external_parameter_id, ep.path, ev.component,
           extract(year FROM ev.valid_from)::int AS yr, ev.value_numeric AS v
    FROM params.external_parameters ep
    JOIN params.external_corpora ec ON ec.id = ep.corpus_id
    JOIN params.external_values ev ON ev.external_parameter_id = ep.id
    WHERE ec.country = %(country)s AND ec.kind = %(kind)s AND ev.value_numeric IS NOT NULL
)
SELECT em.parameter_id, em.model_target, ext.external_parameter_id, ext.path, ext.component,
       %(factor)s::float8 AS factor, %(offset)s::int AS year_offset,
       count(DISTINCT em.yr) AS matched_years, max(em_total.n) AS euromod_years
FROM em
JOIN em_total ON em_total.parameter_id = em.parameter_id
JOIN ext ON ext.yr = em.yr + %(offset)s
        AND abs(ext.v * %(factor)s - em.v) <= %(tol)s * greatest(abs(em.v), 1)
GROUP BY 1, 2, 3, 4, 5
HAVING count(DISTINCT em.yr) >= %(min_years)s
"""


def fingerprint_candidates(
    conn: psycopg.Connection,
    country: str,
    kind: str = "openfisca",
    min_years: int = 3,
    tol: float = 1e-6,
    factors: tuple[float, ...] = (1.0,),
    offsets: tuple[int, ...] = DEFAULT_OFFSETS,
) -> list[LinkCandidate]:
    """Value-fingerprint candidates, best (factor, offset) kept per pair.

    Scored `matched_years / euromod_years`: a series that agrees on every year
    it has scores 1.0 whether it holds 4 points or 18. Ties break on the raw
    number of matched years, so the longer corroboration wins.
    """
    best: dict[tuple[int, int, str], LinkCandidate] = {}
    for factor in factors:
        for offset in offsets:
            rows = conn.execute(
                _FINGERPRINT_SQL,
                {
                    "country": country,
                    "kind": kind,
                    "min_years": min_years,
                    "tol": tol,
                    "factor": factor,
                    "offset": offset,
                },
            ).fetchall()
            for (
                parameter_id, model_target, external_parameter_id, path, component,
                used_factor, year_offset, matched, em_years,
            ) in rows:
                candidate = LinkCandidate(
                    parameter_id=parameter_id,
                    model_target=model_target,
                    external_parameter_id=external_parameter_id,
                    path=path,
                    component=component,
                    factor=used_factor,
                    year_offset=year_offset,
                    matched_years=matched,
                    euromod_years=em_years,
                    score=round(matched / em_years, 4) if em_years else 0.0,
                    note=(
                        None if used_factor == 1 and year_offset == 0
                        else f"factor {used_factor:g}, year offset {year_offset:+d}"
                    ),
                )
                key = (parameter_id, external_parameter_id, component)
                current = best.get(key)
                if current is None or (candidate.score, candidate.matched_years) > (
                    current.score, current.matched_years
                ):
                    best[key] = candidate
    return sorted(
        best.values(), key=lambda c: (-c.score, -c.matched_years, c.model_target, c.path)
    )


def seed_links(conn: psycopg.Connection, path: Path, country: str, kind: str = "openfisca") -> tuple[list[LinkCandidate], list[str]]:
    """Curated pairs from a JSON file: `{"entries": [{model_target, openfisca_path, ...}]}`.

    Entries naming a parameter that is not in params.parameters (the handful of
    hand-authored parameter files that were never ingested) are reported as
    skipped rather than failing the run — the golden-set builder reads those
    from disk and does not need a link row.
    """
    doc = json.loads(path.read_text(encoding="utf-8"))
    links: list[LinkCandidate] = []
    skipped: list[str] = []
    for entry in doc.get("entries", []):
        target = entry.get("model_target")
        of_path = entry["openfisca_path"]
        component = entry.get("component", "value")
        if component == "brackets":
            skipped.append(f"{target or entry.get('parameter_file')}: whole-schedule entry, no single component")
            continue
        if not target:
            skipped.append(f"{entry.get('parameter_file')}: file-only parameter, not in params.parameters")
            continue
        row = conn.execute(
            "SELECT id FROM params.parameters WHERE model_target = %s", (target,)
        ).fetchone()
        if row is None:
            skipped.append(f"{target}: not in params.parameters")
            continue
        ext = conn.execute(
            """
            SELECT ep.id FROM params.external_parameters ep
            JOIN params.external_corpora ec ON ec.id = ep.corpus_id
            WHERE ec.country = %s AND ec.kind = %s AND ep.path = %s
            """,
            (country, kind, of_path),
        ).fetchone()
        if ext is None:
            skipped.append(f"{target}: no external parameter {of_path}")
            continue
        links.append(
            LinkCandidate(
                parameter_id=row[0],
                model_target=target,
                external_parameter_id=ext[0],
                path=of_path,
                component=component,
                factor=float(entry.get("factor", 1)),
                year_offset=int(entry.get("year_offset", 0)),
                matched_years=0,
                euromod_years=0,
                score=1.0,
                match_method="manual",
                note=entry.get("note"),
            )
        )
    return links, skipped


def store_links(conn: psycopg.Connection, links: list[LinkCandidate]) -> int:
    """Upsert suggestions. A row already validated by a human is left alone."""
    written = 0
    with conn.transaction():
        for link in links:
            written += conn.execute(
                """
                INSERT INTO params.parameter_links
                    (parameter_id, external_parameter_id, component, match_method,
                     score, factor, year_offset, note)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (parameter_id, external_parameter_id, component) DO UPDATE SET
                    match_method = EXCLUDED.match_method,
                    score = EXCLUDED.score,
                    factor = EXCLUDED.factor,
                    year_offset = EXCLUDED.year_offset,
                    note = EXCLUDED.note
                WHERE params.parameter_links.validated_by IS NULL
                """,
                (
                    link.parameter_id, link.external_parameter_id, link.component,
                    link.match_method, link.score, link.factor, link.year_offset, link.note,
                ),
            ).rowcount
    return written
