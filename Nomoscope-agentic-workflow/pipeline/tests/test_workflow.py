"""DB-free unit tests: mock extraction, diff logic, queue round-trip."""

from __future__ import annotations

import ast
from datetime import date
from pathlib import Path

import pytest

from nomoscope_workflow import mock, queue_store
from nomoscope_workflow.query_encoder import embedding_process
from nomoscope_workflow.scout import (
    ScoutResult,
    _embedding_model_args,
    _evidence_block,
    merge_results,
)
from nomoscope_workflow.pipeline import (
    GUIDANCE_ONLY_ISSUE,
    cited_classes,
    guidance_only,
    _current_value,
    _income_year_date_issues,
    _needs_gap_fill,
    _retrieval_as_of,
    _unchanged_window,
    _values_equal,
)
from nomoscope_workflow.retrieval import validity_start
from nomoscope_workflow.schema import (
    Bracket,
    CritiqueReport,
    ItemStatus,
    ParameterInformation,
    ParameterRecord,
    ParameterValue,
    ProposalDraft,
    Reference,
    RetrievalHit,
    ReviewItem,
    Routing,
    SourceTrustClass,
    TemporalBasis,
    income_year_for,
)

FR_TEXT = (
    "1. L'impôt est calculé en appliquant à la fraction de chaque part de revenu qui excède "
    "11 497 € le taux de : 11 % pour la fraction supérieure à 11 497 € et inférieure ou égale à "
    "29 315 € ; 30 % pour la fraction supérieure à 29 315 € et inférieure ou égale à 83 823 € ; "
    "45 % pour la fraction supérieure à 180 294 €. 2. La réduction d'impôt est de 45,25 % de son montant."
)


def _hit(**kwargs) -> RetrievalHit:
    defaults = dict(
        chunk_id="c1",
        citation="CGI, art. 197",
        method="citation",
        score=1.0,
        validity="[2025-01-01,)",
        version_status="in_force",
        lang="fr",
        content=FR_TEXT,
    )
    return RetrievalHit(**{**defaults, **kwargs})


def _record(value_type: str, unit: str, value, **info) -> ParameterRecord:
    return ParameterRecord(
        information=ParameterInformation(
            country="FR", model_target="euromod://FR/test", value_type=value_type, unit=unit, **info
        ),
        values=[ParameterValue(value=value, valid_from=date(2024, 1, 1))],
    )


def test_mock_extracts_brackets_with_leading_zero_band():
    record = _record("bracket_schedule", "/1", [Bracket(threshold=0, rate=0.0)])
    draft = mock.propose_with_mock(record, date(2025, 6, 1), [_hit()])
    assert draft.found
    assert [b.threshold for b in draft.value_brackets] == [0, 11497, 29315, 180294]
    assert draft.value_brackets[1].rate == 0.11
    assert draft.valid_from == date(2025, 1, 1)
    assert draft.supporting_extract in FR_TEXT  # verbatim contract


def test_mock_scalar_uses_band_rates_not_incidental_percentages():
    record = _record("scalar", "/1", 0.45)
    draft = mock.propose_with_mock(record, date(2025, 6, 1), [_hit()])
    assert draft.found
    assert draft.value_scalar == 0.45  # not the 45,25 % réduction clause


def test_mock_ignores_hybrid_only_hits():
    record = _record("scalar", "/1", 0.2)
    draft = mock.propose_with_mock(record, date(2025, 6, 1), [_hit(method="hybrid")])
    assert not draft.found


def test_values_equal_and_current_value():
    a = [Bracket(threshold=0, rate=0.0), Bracket(threshold=11294, rate=0.11)]
    b = [Bracket(threshold=0, rate=0.0), Bracket(threshold=11497, rate=0.11)]
    assert _values_equal(a, a.copy())
    assert not _values_equal(a, b)
    record = _record("scalar", "/1", 0.45)
    assert _current_value(record, date(2025, 6, 1)).value == 0.45
    assert _current_value(record, date(2023, 6, 1)) is None


def test_unchanged_routing_keeps_the_current_validity_window():
    # same value as the one in force -> no new period starts, whatever date the
    # model read off the (re-confirming) legal text
    current = ParameterValue(value=0.45, valid_from=date(2024, 1, 1))
    proposed = ParameterValue(
        value=0.45, valid_from=date(2025, 1, 1), valid_to=date(2025, 12, 31)
    )
    kept = _unchanged_window(proposed, current)
    assert kept.valid_from == date(2024, 1, 1)
    assert kept.valid_to is None
    assert kept.value == 0.45


def test_queue_roundtrip_preserves_reviewed_items(tmp_path: Path):
    record = _record("scalar", "/1", 0.45)
    item = ReviewItem(
        id="fr_test_2025-06-01",
        run_id="run-1",
        created_at="2026-07-09T00:00:00Z",
        country="FR",
        model_target="euromod://FR/test",
        as_of=date(2025, 6, 1),
        value_type="scalar",
        unit="/1",
        routing=Routing.UNCHANGED,
        proposed_record=record,
    )
    assert queue_store.write_item(item, tmp_path)
    loaded = queue_store.load_items(tmp_path)
    assert loaded[0].id == item.id

    # a decided item is not overwritten without force
    decided = item.model_copy(update={"status": ItemStatus.ACCEPTED})
    assert queue_store.write_item(decided, tmp_path, force=True)
    assert not queue_store.write_item(item, tmp_path)
    assert queue_store.write_item(item, tmp_path, force=True)


def test_migrate_item_ids_collapses_same_year_runs(tmp_path: Path):
    """Old date-keyed ids re-key to the system year; same-year runs collapse."""

    def item(as_of: date, created: str, status: ItemStatus = ItemStatus.PENDING) -> ReviewItem:
        return ReviewItem(
            id=f"fr_euromod_fr_test_{as_of.isoformat()}",
            run_id=f"run-{created}",
            created_at=created,
            country="FR",
            model_target="euromod://FR/test",
            as_of=as_of,
            system_year=None,  # written before --year existed
            value_type="scalar",
            unit="/1",
            routing=Routing.UNCHANGED,
            status=status,
        )

    old = item(date(2025, 6, 1), "2026-07-09T00:00:00Z", ItemStatus.ACCEPTED)
    newer = item(date(2025, 7, 1), "2026-08-05T00:00:00Z")
    other_year = item(date(2024, 7, 1), "2026-08-05T00:00:00Z")
    for entry in (old, newer, other_year):
        assert queue_store.write_item(entry, tmp_path, force=True)

    queue_store.migrate_item_ids(tmp_path, apply=True)
    loaded = {i.id: i for i in queue_store.load_items(tmp_path)}
    assert set(loaded) == {"fr_euromod_fr_test_2025", "fr_euromod_fr_test_2024"}
    # the decided run wins over the newer pending one, and keeps its decision
    kept = loaded["fr_euromod_fr_test_2025"]
    assert kept.status == ItemStatus.ACCEPTED
    assert kept.system_year == 2025
    # the loser is archived, not deleted
    assert [p.name for p in (tmp_path / "queue_superseded").iterdir()] == [
        "fr_euromod_fr_test_2025-07-01.json"
    ]
    # idempotent: a second pass has nothing left to move
    assert {e["action"] for e in queue_store.migrate_item_ids(tmp_path)} == {"keep"}


def test_derived_refs_detects_formula_parameters():
    from nomoscope_workflow.pipeline import _derived_refs
    from nomoscope_workflow.schema import Lineage

    record = ParameterRecord(
        information=ParameterInformation(
            country="FR",
            model_target="euromod://FR/tinty_fr/def_const/$csg_red_thres",
            value_type="scalar",
            unit="currency",
        ),
        values=[
            ParameterValue(
                value=185568.0,
                valid_from=date(2024, 1, 1),
                lineage=Lineage(model_answer="$PSS * 4"),
            )
        ],
    )
    current = _current_value(record, date(2025, 6, 1))
    assert _derived_refs(record, current) == ["$PSS"]

    # a plain numeric answer is not derived, and a self-reference does not count
    plain = record.model_copy(deep=True)
    plain.values[0].lineage.model_answer = "11496#y"
    assert _derived_refs(plain, _current_value(plain, date(2025, 6, 1))) == []
    self_ref = record.model_copy(deep=True)
    self_ref.values[0].lineage.model_answer = "$csg_red_thres"
    assert _derived_refs(self_ref, _current_value(self_ref, date(2025, 6, 1))) == []
    assert _derived_refs(record, None) == []


def test_income_year_maps_system_year_to_the_previous_income_year():
    # «impôt 2025 sur les revenus 2024»: system year 2025 assesses income 2024.
    assert income_year_for(2025) == 2024


def test_income_year_shifts_retrieval_date():
    # System year 2025 = income year 2024, whose barème is enacted by LF 2025
    # (Feb 2025) — so version selection targets mid-2025, not as_of.
    bareme = _record("bracket_schedule", "/1", None, temporal_basis=TemporalBasis.INCOME_YEAR)
    assert _retrieval_as_of(bareme, date(2025, 6, 1)) == date(2025, 7, 1)
    in_force = _record("scalar", "/1", 0.45)  # default basis: unchanged
    assert _retrieval_as_of(in_force, date(2025, 6, 1)) == date(2025, 6, 1)


def test_income_year_mock_backdates_valid_from_to_income_year_start():
    record = _record(
        "bracket_schedule", "/1", [Bracket(threshold=0, rate=0.0)],
        temporal_basis=TemporalBasis.INCOME_YEAR,
    )
    # version consolidated 2025-02-14 (LF 2025) -> proposal back-dated to the
    # income year it governs, 2024-01-01 — not to the system year.
    draft = mock.propose_with_mock(record, date(2025, 6, 1), [_hit(validity="[2025-02-14,)")])
    assert draft.found
    assert draft.valid_from == date(2024, 1, 1)


def test_income_year_date_issues():
    # act for income year 2025 consolidated Feb 2026, proposal back-dated: consistent
    assert _income_year_date_issues(date(2025, 1, 1), date(2026, 2, 21), 2025) == ([], False)
    # LF 2025 slipped to February 2025 (censure): still inside the 2024 window
    assert _income_year_date_issues(date(2024, 1, 1), date(2025, 2, 15), 2024) == ([], False)
    # valid_from not back-dated to the income-year start — a proposal defect, not provisional
    for wrong in (date(2026, 2, 21), date(2025, 2, 16)):
        issues, provisional = _income_year_date_issues(wrong, date(2026, 2, 21), 2025)
        assert any("2025-01-01" in i for i in issues) and not provisional
    # stale corpus: version from LF 2025 (2024-income barème) cited for income year 2025
    issues, provisional = _income_year_date_issues(date(2025, 1, 1), date(2025, 2, 15), 2025)
    assert any("provisional" in i for i in issues) and provisional
    # CDHR exemption: enacted Feb 2025 FOR 2025 income — the cited text names the
    # income year, which proves the vintage despite predating the December window
    cdhr = "Le I s'applique à compter de l'imposition des revenus de l'année 2025."
    assert _income_year_date_issues(date(2025, 1, 1), date(2025, 2, 15), 2025, cdhr) == ([], False)
    # ...but a text naming some OTHER year does not exempt
    issues, provisional = _income_year_date_issues(
        date(2025, 1, 1), date(2025, 2, 15), 2025, "revenus de l'année 2024"
    )
    assert provisional
    # no cited version validity -> only the back-dating check applies
    assert _income_year_date_issues(date(2025, 1, 1), None, 2025) == ([], False)


def test_cross_article_year_proof():
    from nomoscope_workflow.pipeline import _cross_article_year_proof

    # LF 2025 art. 10 ties CGI art. 224 to income year 2025 by cross-reference
    lf_text = (
        "III. - A. - 1. La contribution mentionnée au I de l'article 224 du code général "
        "des impôts due au titre de l'imposition des revenus de l'année 2025 donne lieu "
        "au versement d'un acompte entre le 1er décembre et le 15 décembre 2025."
    )
    assert _cross_article_year_proof("CGI, art. 224", lf_text, 2025)
    assert not _cross_article_year_proof("CGI, art. 224", lf_text, 2026)
    # a mention of a DIFFERENT article near the year is not proof
    assert not _cross_article_year_proof("CGI, art. 197", lf_text, 2025)
    assert not _cross_article_year_proof(None, lf_text, 2025)
    assert not _cross_article_year_proof("no article here", lf_text, 2025)


def test_cross_article_year_proof_reads_a_terminal_applicability_clause():
    """How finance acts are actually drafted: the amendment at the top, the
    clause that dates it at the bottom. In LF 2025 art. 2 those are 5 166
    characters apart, so a proximity window can never connect them — and every
    FR barème case refused because of it."""
    from nomoscope_workflow.pipeline import _cross_article_year_proof

    lf_art2 = (
        "I. - Le code général des impôts est ainsi modifié : B. - Le I de l'article 197 "
        "est ainsi modifié : a) le montant « 11 294 € » est remplacé par « 11 497 € » ; "
        + "b) " + "x" * 5000 + " ; "
        "II. - Les A et B du I s'appliquent à l'impôt sur le revenu dû au titre de "
        "l'année 2024 et des années suivantes."
    )
    assert _cross_article_year_proof("CGI, art. 197", lf_art2, 2024)
    # the clause dates the whole article, but only for articles it actually
    # names: an article the text never mentions is still not proven
    assert not _cross_article_year_proof("CGI, art. 196 B", lf_art2, 2024)
    # and it proves only the year it names
    assert not _cross_article_year_proof("CGI, art. 197", lf_art2, 2023)
    # a bare year with no applicability clause in front of it is not a proof
    bare = "Le I de l'article 197 est ainsi modifié. " + "x" * 5000 + " Rapport 2024."
    assert not _cross_article_year_proof("CGI, art. 197", bare, 2024)


def test_income_year_prompt_states_the_income_year_not_the_system_year():
    """The prompt and the mechanical date check must agree on the year, or the
    model is asked to prove something the act does not say and refuses. They
    disagreed: the prompt demanded valid_from 2025-01-01 for system year 2025
    while _income_year_date_issues demanded 2024-01-01."""
    from nomoscope_workflow.prompts import _parameter_block

    record = ParameterRecord.model_validate(
        {
            "information": {
                "country": "FR",
                "model_target": "euromod://FR/tinkt_fr/def_const/$tin_rate1",
                "value_type": "scalar",
                "unit": "rate",
                "temporal_basis": "income_year",
            },
            "values": [],
        }
    )
    block = _parameter_block(record, date(2025, 6, 1))
    assert "income year 2024" in block
    assert "valid_from must be 2024-01-01" in block
    assert "2025-01-01" not in block


def test_year_anchor_and_cli_mapping():
    from nomoscope_workflow.cli import _anchor_date

    assert _anchor_date(2025, None) == date(2025, 7, 1)
    assert _anchor_date(None, "2025-06-01") == date(2025, 6, 1)  # deprecated alias
    import pytest
    import typer

    with pytest.raises(typer.Exit):
        _anchor_date(None, None)
    with pytest.raises(typer.Exit):
        _anchor_date(2025, "2025-06-01")


def test_validity_start_parses_pg_daterange():
    assert validity_start("[2025-02-15,)") == date(2025, 2, 15)
    assert validity_start("(2025-02-15,2026-01-01)") == date(2025, 2, 15)
    assert validity_start(None) is None
    assert validity_start("empty") is None


def test_fts_query_ors_distinct_terms():
    from nomoscope_workflow.retrieval import _fts_query

    q = _fts_query("Taux de la tranche 1 taux marginal de l'impôt")
    assert " OR " in q
    terms = q.split(" OR ")
    assert len(terms) == len(set(terms))  # deduplicated
    assert "taux" in terms and "marginal" in terms
    assert "or" not in terms  # websearch operator keyword never emitted as a term
    assert _fts_query("") == ""  # degenerate input falls through unchanged


def test_scout_country_rules_are_complete_and_render_the_prompt():
    from nomoscope_workflow.scout import COUNTRY_SOURCES, ID_HINTS, SCOUT_SYSTEM

    for country, rules in COUNTRY_SOURCES.items():
        assert rules["domains"] and rules["id_pattern"]
        # A country without an id hint would be asked for "exact official id",
        # which is how the LLM starts inventing identifiers.
        assert country in ID_HINTS
        SCOUT_SYSTEM.format(
            country=country, id_hint=ID_HINTS[country], act_kinds=rules["act_kinds"]
        )


def test_scout_lt_ids_are_harvested_from_e_seimas_urls():
    from nomoscope_workflow.scout import COUNTRY_SOURCES

    pattern = COUNTRY_SOURCES["LT"]["id_pattern"]
    # Both TAR id generations, as they appear in portal URLs.
    legacy = "https://e-seimas.lrs.lt/portal/legalAct/lt/TAD/TAR.C677663D2202/asr"
    modern = "https://e-seimas.lrs.lt/portal/legalAct/lt/TAD/ce0f95d090d111e4bb408baba2bdddf3?jfwid=-1c37ov9nb"
    assert pattern.findall(legacy) == ["TAR.C677663D2202"]
    assert pattern.findall(modern) == ["ce0f95d090d111e4bb408baba2bdddf3"]
    # The consolidation index is what gets ingested: the as-published text alone
    # carries no value history.
    assert COUNTRY_SOURCES["LT"]["ingest_suffix"] == "/asr"


def test_scout_fr_ids_still_exclude_whole_codes():
    from nomoscope_workflow.scout import COUNTRY_SOURCES

    pattern = COUNTRY_SOURCES["FR"]["id_pattern"]
    assert pattern.findall(
        "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051521140"
    ) == ["LEGIARTI000051521140"]
    assert pattern.findall("https://www.legifrance.gouv.fr/codes/texte_lc/LEGITEXT000006069577") == []


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
    from nomoscope_workflow.query_encoder import ingest_dir
    from nomoscope_workflow.scout import COUNTRY_SOURCES

    directory = ingest_dir()
    if directory is None:
        # No ingest checkout, so no adapters to disagree with — and a scout with
        # nothing to ingest into cannot gap-fill at all.
        pytest.skip("no Nomotheca-RAG/ingest checkout next to this package")

    for country, rules in COUNTRY_SOURCES.items():
        adapter = directory / "src" / "nomotheca_ingest" / "countries" / country.lower() / "adapter.py"
        assert adapter.is_file(), f"{country} is in COUNTRY_SOURCES but has no adapter to ingest it"
        domains, id_pattern = _adapter_url_source(adapter)
        assert tuple(rules["domains"]) == domains, f"{country}: scout domains differ from {adapter}"
        assert rules["id_pattern"].pattern == id_pattern, (
            f"{country}: scout id_pattern differs from {adapter}"
        )


def _ingest_package(tmp_path: Path, *, cuda: bool) -> Path:
    """Build a minimal ingest package layout, optionally with the GPU environment."""
    directory = tmp_path / "ingest"
    directory.mkdir()
    (directory / "pyproject.toml").write_text("")
    if cuda:
        (directory / ".venv-cuda").mkdir()
        (directory / ".venv-cuda" / "pyvenv.cfg").write_text("home = /usr/bin\n")
    return directory


def test_embedding_process_stays_on_the_cpu_environment_by_default(tmp_path: Path, monkeypatch) -> None:
    """Without .venv-cuda the spawn is exactly the CPU/OpenVINO invocation."""
    monkeypatch.delenv("UV_PROJECT_ENVIRONMENT", raising=False)
    directory = _ingest_package(tmp_path, cuda=False)

    spec = embedding_process(directory, "nomotheca_ingest.query_embeddings")

    assert spec.cuda is False
    assert spec.command == [
        "uv", "run", "--extra", "embeddings", "python", "-m", "nomotheca_ingest.query_embeddings",
    ]
    assert "UV_PROJECT_ENVIRONMENT" not in spec.env


def test_embedding_process_prefers_the_installed_cuda_environment(tmp_path: Path, monkeypatch) -> None:
    """An installed .venv-cuda routes the subprocess to the GPU wheels."""
    monkeypatch.delenv("UV_PROJECT_ENVIRONMENT", raising=False)
    directory = _ingest_package(tmp_path, cuda=True)

    spec = embedding_process(directory, "nomotheca_ingest.cli", "embeddings", "build")

    assert spec.cuda is True
    assert spec.command[:5] == ["uv", "run", "--extra", "embeddings-cuda", "python"]
    assert spec.command[-3:] == ["nomotheca_ingest.cli", "embeddings", "build"]
    assert spec.env["UV_PROJECT_ENVIRONMENT"] == str(directory / ".venv-cuda")
    assert "VIRTUAL_ENV" not in spec.env


def test_embedding_model_args_never_send_the_openvino_export_to_the_gpu(tmp_path: Path) -> None:
    """The OpenVINO IR only loads under the OpenVINO backend, never under Torch."""
    directory = _ingest_package(tmp_path, cuda=True)
    (directory / "models").mkdir()
    (directory / "models" / "bge-m3-openvino").mkdir()

    assert _embedding_model_args(directory, cuda=True) == []
    assert _embedding_model_args(directory, cuda=False) == [
        "--backend", "openvino", "--model-path", "models/bge-m3-openvino",
    ]

    torch_model = directory / "models" / "bge-m3"
    torch_model.mkdir()
    (torch_model / "config.json").write_text("{}")
    assert _embedding_model_args(directory, cuda=True) == ["--model-path", "models/bge-m3"]


# ---------------------------------------------------------------------------
# Gap-fill: when the agent should go and ingest more, and what drives it
# ---------------------------------------------------------------------------


def _report(**kwargs) -> CritiqueReport:
    return CritiqueReport(**kwargs)


def test_gap_fill_triggers_when_no_value_was_found():
    assert _needs_gap_fill({}) is True
    assert _needs_gap_fill({"draft": ProposalDraft(found=False)}) is True


def test_gap_fill_stops_once_a_proposal_survives_the_critique():
    state = {
        "draft": ProposalDraft(found=True, value_scalar=0.11),
        "critique": _report(verdict="pass"),
    }
    assert _needs_gap_fill(state) is False


def test_gap_fill_ignores_a_critique_that_rejected_the_answer_itself():
    """Fetching more law cannot fix a unit error — only a missing source."""
    state = {
        "draft": ProposalDraft(found=True, value_scalar=4.1),
        "critique": _report(
            verdict="fail",
            issues=["values_sane: the parameter declares unit currency for a percentage rate"],
        ),
    }
    assert _needs_gap_fill(state) is False


def test_gap_fill_triggers_on_a_source_availability_failure():
    """The proposal exists, but nothing in the corpus ties it to the income
    year — the applicability clause is in an act we do not hold."""
    state = {
        "draft": ProposalDraft(found=True, value_scalar=0.11),
        "critique": _report(
            verdict="fail",
            issues=["the cited article never names income year 2025, but art. 10 does"],
        ),
    }
    assert _needs_gap_fill(state) is True

    provisional = {
        "draft": ProposalDraft(found=True, value_scalar=0.11),
        "critique": _report(verdict="fail", provisional=True),
    }
    assert _needs_gap_fill(provisional) is True


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


def test_retrieval_hits_and_mock_proposals_default_to_evidence():
    """Nothing that predates the class column silently becomes guidance."""
    record = _record("bracket_schedule", "/1", [Bracket(threshold=0, rate=0.0)])
    hit = _hit()

    assert hit.source_trust_class == SourceTrustClass.EVIDENCE
    draft = mock.propose_with_mock(record, date(2025, 6, 1), [hit])
    assert draft.found
    assert not guidance_only([hit.source_trust_class])


def test_guidance_only_needs_every_citation_to_be_guidance():
    """The informational finding fires on guidance alone, never on a mix."""
    guidance = SourceTrustClass.GUIDANCE
    evidence = SourceTrustClass.EVIDENCE

    assert guidance_only([guidance])
    assert guidance_only([guidance, guidance])
    assert not guidance_only([guidance, evidence])
    assert not guidance_only([evidence])
    # No citation at all is not "guidance-only": there is nothing to label.
    assert not guidance_only([])


def test_guidance_only_finding_leaves_the_verdict_alone():
    """The finding is appended to issues; the four verdict booleans are untouched."""
    report = CritiqueReport(
        schema_valid=True,
        citation_verified=True,
        dates_consistent=True,
        values_sane=True,
        verdict="pass",
    )

    report.issues.append(GUIDANCE_ONLY_ISSUE)

    assert report.verdict == "pass"
    assert GUIDANCE_ONLY_ISSUE in report.issues


def test_guidance_only_flag_survives_the_queue_roundtrip(tmp_path: Path):
    """A reviewer reopening the queue still sees what the value rested on."""
    item = ReviewItem(
        id="fr_guidance_2025",
        run_id="run-g",
        created_at="2026-07-09T00:00:00Z",
        country="FR",
        model_target="euromod://FR/test",
        as_of=date(2025, 6, 1),
        system_year=2025,
        value_type="scalar",
        unit="/1",
        routing=Routing.CHANGED,
        guidance_only=True,
        proposed_value=ParameterValue(
            value=0.45,
            valid_from=date(2025, 1, 1),
            references=[
                Reference(
                    title="Circulaire Unedic n. 2025-01",
                    source_trust_class=SourceTrustClass.GUIDANCE,
                )
            ],
        ),
    )

    assert queue_store.write_item(item, tmp_path)
    loaded = queue_store.load_items(tmp_path)[0]

    assert loaded.guidance_only
    assert loaded.proposed_value.references[0].source_trust_class == SourceTrustClass.GUIDANCE


def _draft_citing(chunk_id: str) -> ProposalDraft:
    return ProposalDraft(found=True, value_scalar=0.45, citation_chunk_id=chunk_id)


def test_the_finding_reads_the_class_of_the_chunk_the_draft_cites():
    """The wiring itself: only the CITED hit decides, not whatever was retrieved.

    A guidance document answering the question sits next to evidence chunks in
    every real run — reading the whole hit list instead of the cited chunk
    would label almost nothing.
    """
    guidance = _hit(chunk_id="c-guidance", source_trust_class=SourceTrustClass.GUIDANCE)
    evidence = _hit(chunk_id="c-evidence", source_trust_class=SourceTrustClass.EVIDENCE)
    hits = [evidence, guidance]

    assert guidance_only(cited_classes(_draft_citing("c-guidance"), hits))
    assert not guidance_only(cited_classes(_draft_citing("c-evidence"), hits))
    # A citation that is not among the retrieved chunks labels nothing: the
    # critique has already failed it on the citation leg.
    assert cited_classes(_draft_citing("c-unknown"), hits) == []
    assert not guidance_only(cited_classes(_draft_citing("c-unknown"), hits))
    # No proposal at all, and no citation on one, are both "nothing to label".
    assert cited_classes(None, hits) == []
    assert cited_classes(ProposalDraft(found=False), hits) == []


# ---------------------------------------------------------------------------
# Derived values: arithmetic over quoted operands, checked like an extract
# ---------------------------------------------------------------------------

from nomoscope_workflow.paramdb import record_value  # noqa: E402
from nomoscope_workflow.pipeline import (  # noqa: E402
    DERIVATION_CONSTANTS,
    _check_derivation,
    _figures_in,
    evaluate_derivation,
)
from nomoscope_workflow.retrieval import _article_tokens  # noqa: E402
from nomoscope_workflow.schema import Operand  # noqa: E402

AKW_TEXT = (
    "3. Het aan een verzekerde over een kalenderkwartaal te betalen bedrag aan kinderbijslag "
    "bedraagt voor een kind, dat op de eerste dag van dat kwartaal:\na. jonger is dan 6 jaar: "
    "€ 286,45\nb. 6 jaar of ouder, maar jonger is dan 12 jaar: € 347,83 en\nc. 12 jaar en ouder, "
    "maar jonger is dan 18 jaar: € 409,21"
)


def _verify_in(hits):
    content = {h.chunk_id: h.content for h in hits}

    def verify(chunk_id, extract):
        idx = content.get(chunk_id, "").find(extract)
        return (idx, idx + len(extract)) if idx >= 0 else None

    return verify


def _derived(**overrides) -> ProposalDraft:
    draft = dict(
        found=True,
        value_scalar=1.2143,
        citation_chunk_id="akw",
        supporting_extract="6 jaar of ouder, maar jonger is dan 12 jaar: € 347,83",
        derivation="a / b",
        operands=[
            Operand(name="a", value=347.83, citation_chunk_id="akw",
                    supporting_extract="6 jaar of ouder, maar jonger is dan 12 jaar: € 347,83"),
            Operand(name="b", value=286.45, citation_chunk_id="akw",
                    supporting_extract="jonger is dan 6 jaar: € 286,45"),
        ],
    )
    draft.update(overrides)
    return ProposalDraft(**draft)


def test_derivation_over_quoted_operands_is_verified():
    hits = [_hit(chunk_id="akw", citation="AKW, artikel 12", lang="nl", content=AKW_TEXT)]
    issues, offsets, note = _check_derivation(_derived(), hits, _verify_in(hits))
    assert issues == []
    assert all(span is not None for span in offsets) and len(offsets) == 2
    assert "a = 347.83 (AKW, artikel 12)" in note and "= 1.2142" in note


def test_derivation_rejects_a_figure_that_is_not_quoted():
    """Statutory monthly hours remembered rather than quoted are not evidence."""
    hits = [_hit(chunk_id="akw", content=AKW_TEXT)]
    draft = _derived(derivation="a * 151.67", value_scalar=52755.0)
    issues, _, _ = _check_derivation(draft, hits, _verify_in(hits))
    assert issues and "151.67" in issues[0] and "not a quoted operand" in issues[0]


def test_derivation_allows_calendar_constants_only():
    assert evaluate_derivation("a * 12 + b", {"a": 2.0, "b": 1.0}) == 25.0
    assert 12.0 in DERIVATION_CONSTANTS
    for bad in ("a ** 2", "__import__('os').system('x')", "max(a, b)", "a.real", "0.5 * a"):
        with pytest.raises(ValueError):
            evaluate_derivation(bad, {"a": 1.0, "b": 2.0})


def test_derivation_rejects_an_operand_the_extract_does_not_state():
    hits = [_hit(chunk_id="akw", content=AKW_TEXT)]
    draft = _derived(operands=[
        Operand(name="a", value=347.83, citation_chunk_id="akw",
                supporting_extract="6 jaar of ouder, maar jonger is dan 12 jaar: € 347,83"),
        Operand(name="b", value=286.45, citation_chunk_id="akw",
                supporting_extract="12 jaar en ouder, maar jonger is dan 18 jaar: € 409,21"),
    ])
    issues, _, _ = _check_derivation(draft, hits, _verify_in(hits))
    assert issues == ["derivation: operand b's extract does not state 286.45"]


def test_derivation_rejects_a_paraphrased_operand_and_an_unretrieved_chunk():
    hits = [_hit(chunk_id="akw", content=AKW_TEXT)]
    draft = _derived(operands=[
        Operand(name="a", value=347.83, citation_chunk_id="akw",
                supporting_extract="between 6 and 12 years: € 347,83"),
        Operand(name="b", value=286.45, citation_chunk_id="elsewhere",
                supporting_extract="jonger is dan 6 jaar: € 286,45"),
    ])
    issues, offsets, _ = _check_derivation(draft, hits, _verify_in(hits))
    assert offsets == [None, None]
    assert any("not a verbatim quote" in i for i in issues)
    assert any("not retrieved" in i for i in issues)


def test_derivation_must_evaluate_to_the_proposed_value():
    hits = [_hit(chunk_id="akw", content=AKW_TEXT)]
    issues, _, _ = _check_derivation(_derived(value_scalar=1.3), hits, _verify_in(hits))
    assert issues and "evaluates to 1.21428" in issues[0]


def test_figures_are_read_in_every_european_spelling():
    assert 1801.80 in _figures_in("11,88 € par heure, soit 1 801,80 € par mois")
    assert 1801.80 in _figures_in("1.801,80 euros")
    assert 9139.0 in _figures_in("vermeerderd met € 9.139")  # Dutch thousands
    assert 2.1 in _figures_in("artikel 2.10") and 44000.0 in _figures_in("€44,000")


def test_record_value_prefers_the_ingested_scalar_for_percent_literals():
    """`8.17%` is null in the export's normalized value; the ingester read it."""
    assert record_value(None, 0.0817, "numeric") == 0.0817
    assert record_value(0.2, 0.2, "numeric") == 0.2
    assert record_value("$PSS * 4", None, "expression") == "$PSS * 4"
    assert record_value(None, None, "n_a") is None


def test_article_tokens_follow_each_country_idiom():
    assert _article_tokens("article D. 633-3 du code de la sécurité sociale") == ["D633-3"]
    assert _article_tokens("artículo 66.2 de la Ley 35/2006") == ["66.2"]
    assert _article_tokens("de tabel in artikel 2.10, eerste lid, van de Wet IB 2001") == ["2.10"]
    assert _article_tokens("Finance Act 2024, section amending section 531AN of the TCA 1997") == ["531AN"]
    assert _article_tokens("section 461 of the Taxes Consolidation Act 1997") == ["461"]
    assert _article_tokens("VSDĮ 10 straipsnio 1 dalis") == ["10"]
    assert _article_tokens("art. L. 241-3 du CSS et l'article 4 bis") == ["L241-3", "4 bis"]
    assert _article_tokens("l'arrêté fixant le plafond de la sécurité sociale pour 2025") == []


def test_scout_rounds_merge_located_citations():
    merged = merge_results([
        ScoutResult(mode="tavily", round=1, located=["LIRPF Artículo 66"]),
        ScoutResult(mode="tavily", round=2, located=["LIRPF Artículo 66", "LIRPF Artículo 76"]),
    ])
    assert merged.located == ["LIRPF Artículo 66", "LIRPF Artículo 76"]
    assert "located" in merged.summary()
