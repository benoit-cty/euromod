"""The gap-fill scout: country tables, discovery, guidance publishers, web search."""

from __future__ import annotations

import ast
from datetime import date
from pathlib import Path

import httpx
import pytest

from nomoscope_workflow import scout as scout_mod
from nomoscope_workflow import scout_ingest, web
from nomoscope_workflow.config import WorkflowConfig
from nomoscope_workflow.query_encoder import ingest_dir
from nomoscope_workflow.scout import SCOUT_SYSTEM, ScoutResult, _evidence_block, merge_results
from nomoscope_workflow.scout_sources import COUNTRY_SOURCES, ID_HINTS, guidance_document

from workflow_fixtures import _record


def _adapter_url_source(adapter: Path) -> tuple[tuple[str, ...], str]:
    """The (domains, id_pattern source) one ingest adapter declares.

    Read out of the adapter's syntax tree rather than imported: `nomoscope_workflow`
    must not depend on `nomotheca_ingest` (see the test below), so the package is
    not installed in this environment — only its source tree is on disk.
    """
    tree = ast.parse(adapter.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        call = getattr(node, "value", None)
        if isinstance(call, ast.Call) and getattr(call.func, "id", "") == "UrlSource":
            fields = {kw.arg: kw.value for kw in call.keywords}
            # id_pattern is always `re.compile(r"...")`; take the raw source so
            # the comparison is on the pattern text, not on a compiled object.
            return tuple(ast.literal_eval(fields["domains"])), fields["id_pattern"].args[0].value
    raise AssertionError(f"{adapter} declares no UrlSource")


def test_scout_country_rules_are_complete_and_render_the_prompt():
    for country, rules in COUNTRY_SOURCES.items():
        assert rules.domains and rules.id_pattern
        # A country without an id hint would be asked for "exact official id",
        # which is how the LLM starts inventing identifiers.
        assert country in ID_HINTS
        SCOUT_SYSTEM.format(
            country=country, id_hint=ID_HINTS[country], act_kinds=rules.act_kinds
        )


def test_scout_lt_ids_are_harvested_from_e_seimas_urls():
    pattern = COUNTRY_SOURCES["LT"].id_pattern
    # Both TAR id generations, as they appear in portal URLs.
    legacy = "https://e-seimas.lrs.lt/portal/legalAct/lt/TAD/TAR.C677663D2202/asr"
    modern = "https://e-seimas.lrs.lt/portal/legalAct/lt/TAD/ce0f95d090d111e4bb408baba2bdddf3?jfwid=-1c37ov9nb"
    assert pattern.findall(legacy) == ["TAR.C677663D2202"]
    assert pattern.findall(modern) == ["ce0f95d090d111e4bb408baba2bdddf3"]
    # The consolidation index is what gets ingested: the as-published text alone
    # carries no value history.
    assert COUNTRY_SOURCES["LT"].ingest_suffix == "/asr"


def test_scout_fr_ids_still_exclude_whole_codes():
    pattern = COUNTRY_SOURCES["FR"].id_pattern
    assert pattern.findall(
        "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051521140"
    ) == ["LEGIARTI000051521140"]
    assert pattern.findall("https://www.legifrance.gouv.fr/codes/texte_lc/LEGITEXT000006069577") == []


def test_scout_fr_keeps_collective_agreements_but_not_whole_conventions():
    # ADR 0006: the AGIRC-ARRCO ANI is evidence; its /conv_coll/ ids used to be dropped.

    pattern = COUNTRY_SOURCES["FR"].id_pattern
    assert pattern.findall(
        "https://www.legifrance.gouv.fr/conv_coll/id/KALIARTI000036731900"
    ) == ["KALIARTI000036731900"]
    assert pattern.findall(
        "https://www.legifrance.gouv.fr/conv_coll/id/KALITEXT000036731682?idConteneur=KALICONT000046709421"
    ) == ["KALITEXT000036731682"]


def test_scout_portal_facts_still_match_the_adapters_that_own_them():
    """`domains` and `id_pattern` are copied from the ingester — check the copy.

    Which domains a member state publishes on and what its national ids look
    like are adapter facts: the ingester declares them as a
    `countries.base.UrlSource` and routes pasted URLs with them. The scout needs
    the same two facts one step earlier (restrict the web search to official
    domains, harvest ids out of the result URLs), and cannot share the
    declaration: the dependency between the two packages runs one way only —
    `nomotheca-ingest` may import `nomoscope-agentic-workflow` (its optional
    `translate` extra), never the reverse — and the scout reaches the ingester
    by subprocess precisely to keep it that way.

    So the table is duplicated on purpose, and this is what makes the two
    disagree loudly instead of silently. It reads the adapter's source text, so
    it runs in the default environment with the ingest package uninstalled; the
    mirror image lives in the ingest suite (`tests/test_routing.py`), because
    each suite has to catch the edit made on its own side.
    """
    directory = ingest_dir()
    if directory is None:
        # No ingest checkout, so no adapters to disagree with — and a scout with
        # nothing to ingest into cannot gap-fill at all.
        pytest.skip("no Nomotheca-RAG/ingest checkout next to this package")

    for country, rules in COUNTRY_SOURCES.items():
        adapter = directory / "src" / "nomotheca_ingest" / "countries" / country.lower() / "adapter.py"
        assert adapter.is_file(), f"{country} is in COUNTRY_SOURCES but has no adapter to ingest it"
        domains, id_pattern = _adapter_url_source(adapter)
        assert tuple(rules.domains) == domains, f"{country}: scout domains differ from {adapter}"
        assert rules.id_pattern.pattern == id_pattern, (
            f"{country}: scout id_pattern differs from {adapter}"
        )


def test_scout_evidence_block_carries_needs_and_skips_what_we_hold():
    block = _evidence_block(
        ["l'arrêté fixant le plafond de la sécurité sociale pour 2025"],
        ["CGI, art. 197", "CGI, art. 197"],
    )
    assert "plafond de la sécurité sociale pour 2025" in block
    assert "do NOT hunt these" in block
    assert block.count("CGI, art. 197") == 1  # de-duplicated


def test_scout_rounds_merge_without_duplicates():
    merged = merge_results([
        ScoutResult(mode="tavily", round=1, ingested=["A"], candidate_ids=["A", "B"],
                    needs=["the PSS arrêté"], reasoning="round one"),
        ScoutResult(mode="tavily", round=2, ingested=["C"], candidate_ids=["B", "C"],
                    needs=["the PSS arrêté", "art. L. 241-3"], reasoning="round two"),
    ])
    assert merged.round == 2
    assert merged.ingested == ["A", "C"]
    assert merged.candidate_ids == ["A", "B", "C"]
    assert merged.needs == ["the PSS arrêté", "art. L. 241-3"]
    assert merged.reasoning == "round one | round two"


def test_scout_rounds_merge_located_citations():
    merged = merge_results([
        ScoutResult(mode="tavily", round=1, located=["LIRPF Artículo 66"]),
        ScoutResult(mode="tavily", round=2, located=["LIRPF Artículo 66", "LIRPF Artículo 76"]),
    ])
    assert merged.located == ["LIRPF Artículo 66", "LIRPF Artículo 76"]
    assert "located" in merged.summary()


def test_scout_reads_a_publisher_document_off_its_url():
    cnav = guidance_document(
        "FR", "https://legislation.lassuranceretraite.fr/Pdf/circulaire_cnav_2025_13_03042025.pdf"
    )
    assert (cnav.publisher, cnav.kind, cnav.title, cnav.valid_from) == (
        "Cnav", "circulaire", "Circulaire Cnav 2025/13 du 03/04/2025", date(2025, 4, 3)
    )
    assert guidance_document(
        "FR", "https://legislation.lassuranceretraite.fr/Documents/Circulaires/Pdf/circulaire_cnav_2026_11_03042026.pdf"
    ).title == "Circulaire Cnav 2026/11 du 03/04/2026"
    unedic = guidance_document(
        "FR",
        "https://www.unedic.org/storage/uploads/2025/04/08/"
        "PRE-CIRC-Circulaire_n_2025-03_du_1er_avril_2025_uid_67f53cc00a07f.pdf",
    )
    assert (unedic.kind, unedic.valid_from) == ("circulaire", date(2025, 4, 1))
    bofip = guidance_document(
        "FR", "https://bofip.impots.gouv.fr/bofip/2491-PGP.html/identifiant=BOI-IR-LIQ-20-20-10-20250414"
    )
    assert (bofip.kind, bofip.title, bofip.valid_from) == (
        "doctrine", "BOI-IR-LIQ-20-20-10 du 14/04/2025", date(2025, 4, 14)
    )
    # A listing, a news page, another country: not a document, nothing guessed.
    assert guidance_document("FR", "https://www.unedic.org/la-reglementation/circulaires") is None
    assert guidance_document(
        "FR", "https://www.unedic.org/actualites/allocations-d-assurance-chomage-revalorisation-de-0-5"
    ) is None
    assert guidance_document(
        "NL", "https://legislation.lassuranceretraite.fr/Pdf/circulaire_cnav_2025_13_03042025.pdf"
    ) is None


def test_scout_ingests_a_cnav_circular_as_guidance(monkeypatch):
    """The ASI ceiling case: the analyst names the Cnav circular, the scout fetches it."""
    url = "https://legislation.lassuranceretraite.fr/Pdf/circulaire_cnav_2025_13_03042025.pdf"
    searched: list[tuple[str, list[str]]] = []
    ran: list[list[str]] = []

    def fake_search(api_key, query, domains):
        searched.append((query, domains))
        if "legislation.lassuranceretraite.fr" in domains:
            return [
                {"url": url, "title": "L'allocation supplémentaire d'invalidité - Circulaire Cnav"},
                {"url": "https://www.unedic.org/la-reglementation/circulaires", "title": "Circulaires"},
            ]
        return []

    monkeypatch.setattr(web, "_web_search_unavailable", None)
    monkeypatch.setattr(web, "_tavily_search", fake_search)
    monkeypatch.setattr(
        scout_mod.llm,
        "run_agent",
        lambda *a, **k: scout_mod.ScoutSuggestion(
            search_queries=["plafond ASI couple 2025"],
            guidance_queries=["circulaire Cnav 2025 plafonds ASI revalorisation"],
        ),
    )
    monkeypatch.setattr(scout_ingest, "known_instruments", lambda cfg, ids, known_key=None: set())
    monkeypatch.setattr(scout_ingest, "run_ingest_cli", lambda cfg, args, what: ran.append(args))
    monkeypatch.setattr(scout_ingest, "build_embeddings", lambda cfg: None)

    cfg = WorkflowConfig(database_url="postgresql://u@h/db", scout="tavily", tavily_api_key="k")
    record = _record("scalar", "currency/year", 17000.0)
    result = scout_mod.run(cfg, record, date(2025, 7, 1), needs=["Circulaire Cnav 2025-13 du 03/04/2025"])

    assert searched[-1] == (
        "circulaire Cnav 2025 plafonds ASI revalorisation",
        ["legislation.lassuranceretraite.fr", "unedic.org", "bofip.impots.gouv.fr"],
    )
    assert result.ingested == [url]
    assert ran == [[
        "document", url, "--database-url", "postgresql://u@h/db", "--jurisdiction", "FR",
        "--lang", "fr", "--title", "Circulaire Cnav 2025/13 du 03/04/2025", "--kind", "circulaire",
        "--valid-from", "2025-04-03", "--trigger", "cache_miss",
    ]]


def test_tavily_432_latches_by_status_code(monkeypatch):
    """One latch for scout and chat, keyed on the HTTP status (code audit 4)."""
    calls = []

    def quota_spent(api_key, query, domains):
        calls.append(query)
        request = httpx.Request("POST", "https://api.tavily.com/search")
        raise httpx.HTTPStatusError("432", request=request, response=httpx.Response(432, request=request))

    monkeypatch.setattr(web, "_web_search_unavailable", None)
    monkeypatch.setattr(web, "_tavily_search", quota_spent)
    for _ in range(2):
        with pytest.raises(web.WebSearchUnavailable):
            web.web_search("k", "q", [])
    assert calls == ["q"]  # latched: no second request
