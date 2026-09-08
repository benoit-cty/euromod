"""Spain's autonomous communities as child jurisdictions of ``ES``.

One table, three keys for the same region, because three systems name it
differently and none can be inferred from another:

- **ISO 3166-2** (``ES-AR``) — the jurisdiction code ``jurisdictions.code``
  stores; the ELI path carries it in lower case (``boe.es/eli/es-ar/l/…``);
- **NUTS-2** (``ES24``) — what EUROMOD embeds in regional parameter names
  (``$bsarg_rg24_basic_amt``, ``$bchrg_reg24_lim1``, ``$tin_depallrg24_amt1``);
- **BOE ``departamento``** — the consolidated API's label for the enacting
  body (``Comunidad Autónoma de Aragón``).

This module is the single source of the mapping. ``db/seed.sql`` and
``db/migrations/0002_es_autonomous_communities.sql`` carry the same rows as
SQL, and ``tests/test_es_regions.py`` fails when either drifts from here.

Why child jurisdictions rather than a tag on ``ES`` (ADR 0003): evidence
retrieval scopes a run to a list of jurisdiction codes — state law plus the
parameter's own community — so Aragón's parameter can never be "supported" by
a verbatim quote from Asturias's decree. That false positive passes the
character-for-character extract check, because the quote is real; only the
scoping can exclude it.
"""

from __future__ import annotations

import re
import unicodedata
from typing import NamedTuple


class AutonomousCommunity(NamedTuple):
    """One community: jurisdiction code, EUROMOD region key, BOE naming."""

    code: str  # ISO 3166-2, also jurisdictions.code
    nuts2: str  # NUTS-2 code, the two digits appear in EUROMOD parameter names
    name: str
    departamento: str  # BOE <departamento> text for acts the community enacts
    langs: tuple[str, ...]  # official languages (BOE publishes the Castilian text)


# ``departamento`` strings marked (*) are BOE's naming convention and were not
# read off a live payload yet — no consolidated act of that community was
# needed so far. The ELI segment is matched first, so a wrong string here can
# only affect the departamento fallback, never an act that carries an ELI.
AUTONOMOUS_COMMUNITIES: tuple[AutonomousCommunity, ...] = (
    AutonomousCommunity("ES-AN", "ES61", "Andalucía", "Comunidad Autónoma de Andalucía", ("es",)),
    AutonomousCommunity("ES-AR", "ES24", "Aragón", "Comunidad Autónoma de Aragón", ("es",)),
    AutonomousCommunity("ES-AS", "ES12", "Principado de Asturias", "Comunidad Autónoma del Principado de Asturias", ("es",)),
    AutonomousCommunity("ES-CB", "ES13", "Cantabria", "Comunidad Autónoma de Cantabria", ("es",)),
    AutonomousCommunity("ES-CL", "ES41", "Castilla y León", "Comunidad Autónoma de Castilla y León", ("es",)),  # (*)
    AutonomousCommunity("ES-CM", "ES42", "Castilla-La Mancha", "Comunidad Autónoma de Castilla-La Mancha", ("es",)),
    AutonomousCommunity("ES-CN", "ES70", "Canarias", "Comunidad Autónoma de Canarias", ("es",)),
    AutonomousCommunity("ES-CT", "ES51", "Cataluña", "Comunidad Autónoma de Cataluña", ("es", "ca")),
    AutonomousCommunity("ES-EX", "ES43", "Extremadura", "Comunidad Autónoma de Extremadura", ("es",)),
    AutonomousCommunity("ES-GA", "ES11", "Galicia", "Comunidad Autónoma de Galicia", ("es", "gl")),
    AutonomousCommunity("ES-IB", "ES53", "Illes Balears", "Comunidad Autónoma de las Illes Balears", ("es", "ca")),
    AutonomousCommunity("ES-MC", "ES62", "Región de Murcia", "Comunidad Autónoma de la Región de Murcia", ("es",)),
    AutonomousCommunity("ES-MD", "ES30", "Comunidad de Madrid", "Comunidad de Madrid", ("es",)),
    AutonomousCommunity("ES-NC", "ES22", "Comunidad Foral de Navarra", "Comunidad Foral de Navarra", ("es", "eu")),
    AutonomousCommunity("ES-PV", "ES21", "País Vasco", "Comunidad Autónoma del País Vasco", ("es", "eu")),
    AutonomousCommunity("ES-RI", "ES23", "La Rioja", "Comunidad Autónoma de La Rioja", ("es",)),
    AutonomousCommunity("ES-VC", "ES52", "Comunitat Valenciana", "Comunitat Valenciana", ("es", "ca")),  # (*)
    AutonomousCommunity("ES-CE", "ES63", "Ceuta", "Ciudad de Ceuta", ("es",)),  # (*)
    AutonomousCommunity("ES-ML", "ES64", "Melilla", "Ciudad de Melilla", ("es",)),  # (*)
)

_BY_CODE = {ac.code: ac for ac in AUTONOMOUS_COMMUNITIES}
_BY_NUTS2 = {ac.nuts2: ac for ac in AUTONOMOUS_COMMUNITIES}

# BOE's ``ambito`` code for autonomous-community acts ("Autonómico"); state
# acts carry "1" ("Estatal").
AMBITO_AUTONOMICO = "2"

# The jurisdiction segment of a BOE ELI: ``/eli/es-ga/dleg/2011/07/28/1``.
ELI_JURISDICTION_RE = re.compile(r"/eli/(es-[a-z]{2})/", re.IGNORECASE)


def by_code(code: str) -> AutonomousCommunity | None:
    """Look a community up by ISO 3166-2 code (``ES-AR``)."""
    return _BY_CODE.get(code.upper())


def by_nuts2(nuts2: str) -> AutonomousCommunity | None:
    """Look a community up by NUTS-2 code (``ES24``)."""
    return _BY_NUTS2.get(nuts2.upper())


def _fold(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value.strip().casefold())
    return " ".join("".join(c for c in decomposed if not unicodedata.combining(c)).split())


_BY_DEPARTAMENTO = {_fold(ac.departamento): ac for ac in AUTONOMOUS_COMMUNITIES}


def jurisdiction_for(
    *,
    url_eli: str | None,
    departamento: str | None,
    ambito_codigo: str | None,
    default: str,
) -> str:
    """Return the jurisdiction code an act belongs under.

    The ELI's jurisdiction segment wins (it is the standardised key); BOE's
    ``departamento`` text is the fallback for the rare consolidated act without
    an ELI. A state act, or anything that names no community, keeps
    ``default`` (the adapter's ``ES``).

    An act BOE labels *Autonómico* whose community cannot be placed raises:
    filing it under ``ES`` would put a regional amount in the state-law scope
    of every Spanish run, which is exactly the false positive the child
    jurisdictions exist to exclude.
    """
    match = ELI_JURISDICTION_RE.search(url_eli or "")
    if match:
        community = by_code(match.group(1))
        if community is not None:
            return community.code
    if departamento:
        community = _BY_DEPARTAMENTO.get(_fold(departamento))
        if community is not None:
            return community.code
    if ambito_codigo == AMBITO_AUTONOMICO:
        msg = (
            f"autonomous-community act with unknown region: departamento={departamento!r}, "
            f"url_eli={url_eli!r}. Add the community to countries/es/regions.py (and to "
            "db/seed.sql + a migration) rather than filing it under ES."
        )
        raise ValueError(msg)
    return default
