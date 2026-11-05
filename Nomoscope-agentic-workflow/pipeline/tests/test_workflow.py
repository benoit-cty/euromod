"""DB-free unit tests: mock extraction, diff logic, queue round-trip."""

from __future__ import annotations

import ast
from datetime import date
from pathlib import Path

import pytest

from nomoscope_workflow import mock
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


def test_scout_fr_keeps_collective_agreements_but_not_whole_conventions():
    # ADR 0006: the AGIRC-ARRCO ANI is evidence; its /conv_coll/ ids used to be dropped.
    from nomoscope_workflow.scout import COUNTRY_SOURCES

    pattern = COUNTRY_SOURCES["FR"]["id_pattern"]
    assert pattern.findall(
        "https://www.legifrance.gouv.fr/conv_coll/id/KALIARTI000036731900"
    ) == ["KALIARTI000036731900"]
    assert pattern.findall(
        "https://www.legifrance.gouv.fr/conv_coll/id/KALITEXT000036731682?idConteneur=KALICONT000046709421"
    ) == ["KALITEXT000036731682"]


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
    monkeypatch.delenv("NOMOS_PYTHON", raising=False)
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
    monkeypatch.delenv("NOMOS_PYTHON", raising=False)
    directory = _ingest_package(tmp_path, cuda=True)

    spec = embedding_process(directory, "nomotheca_ingest.cli", "embeddings", "build")

    assert spec.cuda is True
    assert spec.command[:5] == ["uv", "run", "--extra", "embeddings-cuda", "python"]
    assert spec.command[-3:] == ["nomotheca_ingest.cli", "embeddings", "build"]
    assert spec.env["UV_PROJECT_ENVIRONMENT"] == str(directory / ".venv-cuda")
    assert "VIRTUAL_ENV" not in spec.env
    assert spec.cwd == directory


def test_embedding_process_uses_nomos_python_in_the_current_directory(tmp_path: Path, monkeypatch) -> None:
    """Inside the worker the spawn is its interpreter, -m module, here: no uv, no ingest-dir walk."""
    monkeypatch.setenv("NOMOS_PYTHON", "/opt/worker/bin/python")
    monkeypatch.setenv("VIRTUAL_ENV", "/somewhere/.venv")
    monkeypatch.chdir(tmp_path)
    directory = _ingest_package(tmp_path, cuda=True)  # would pick CUDA on the uv path

    spec = embedding_process(None, "nomotheca_ingest.cli", "embeddings", "build")

    assert spec.command == ["/opt/worker/bin/python", "-m", "nomotheca_ingest.cli", "embeddings", "build"]
    assert spec.cwd == Path.cwd()
    assert spec.cuda is False
    assert "VIRTUAL_ENV" not in spec.env
    assert "UV_PROJECT_ENVIRONMENT" not in spec.env
    # the walk-based directory is ignored even when it exists
    assert embedding_process(directory, "nomotheca_ingest.query_embeddings").command[0] == "/opt/worker/bin/python"


def test_scout_ingest_uses_nomos_python(tmp_path: Path, monkeypatch) -> None:
    """The scout's archive-first ingest follows the same switch."""
    from nomoscope_workflow import scout as scout_mod
    from nomoscope_workflow.config import WorkflowConfig

    monkeypatch.setenv("NOMOS_PYTHON", "/opt/worker/bin/python")
    monkeypatch.chdir(tmp_path)
    calls: list[dict] = []

    class _Done:
        returncode = 0
        stdout = stderr = ""

    def fake_run(command, **kwargs):
        calls.append({"command": command, **kwargs})
        return _Done()

    monkeypatch.setattr(scout_mod.subprocess, "run", fake_run)
    cfg = WorkflowConfig(database_url="postgresql://u@h/db")

    assert scout_mod._ingest_instrument(cfg, "FR", "JORFTEXT000051168007") is None
    assert calls[0]["command"] == [
        "/opt/worker/bin/python", "-m", "nomotheca_ingest.cli",
        "instrument", "fr", "JORFTEXT000051168007", "--database-url", "postgresql://u@h/db",
    ]
    assert calls[0]["cwd"] == Path.cwd()
    assert "VIRTUAL_ENV" not in calls[0]["env"]

    assert scout_mod._build_embeddings(cfg) is None
    assert calls[1]["command"] == [
        "/opt/worker/bin/python", "-m", "nomotheca_ingest.cli", "embeddings", "build",
        "--database-url", "postgresql://u@h/db", "--no-progress",
    ]


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


def test_guidance_only_flag_survives_the_queue_roundtrip():
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

    # the queue row stores item.model_dump(mode="json"); this is that round trip
    loaded = ReviewItem.model_validate(item.model_dump(mode="json"))

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
    _values_sane,
    _figures_in,
    _misquote_hint,
    _round_like_held,
    evaluate_derivation,
)
from nomoscope_workflow.retrieval import _article_tokens, _code_refs, closest_passage  # noqa: E402
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


def test_derivation_rounds_where_the_text_says_so():
    # AGIRC-ARRCO art. 36: «Les taux ainsi appelés sont arrondis au centième».
    # 6,20 % × 127 % = 7,874 % -> 7,87 %; the 60 % employer share is 4,722 %.
    called = evaluate_derivation("round(a * b, 4)", {"a": 0.062, "b": 1.27})
    assert called == 0.0787
    assert evaluate_derivation("round(a * b, 4) * c", {"a": 0.062, "b": 1.27, "c": 0.6}) == pytest.approx(0.04722)
    # Half-up, as a legal text means it — Python's round(0.5) is 0.
    assert evaluate_derivation("round(a, 0)", {"a": 0.5}) == 1.0
    assert evaluate_derivation("round(a, 0)", {"a": 2.5}) == 3.0
    # The precision is a literal, never a figure smuggled in by another route.
    for bad in ("round(a, b)", "round(a, 1.5)", "round(a)", "round(a, 9)", "round(a, ndigits=2)", "round(a, -1)"):
        with pytest.raises(ValueError):
            evaluate_derivation(bad, {"a": 1.234, "b": 2.0})


def test_derivation_rejects_an_operand_the_extract_does_not_state():
    hits = [_hit(chunk_id="akw", content=AKW_TEXT)]
    draft = _derived(operands=[
        Operand(name="a", value=347.83, citation_chunk_id="akw",
                supporting_extract="6 jaar of ouder, maar jonger is dan 12 jaar: € 347,83"),
        Operand(name="b", value=286.45, citation_chunk_id="akw",
                supporting_extract="12 jaar en ouder, maar jonger is dan 18 jaar: € 409,21"),
    ])
    issues, _, _ = _check_derivation(draft, hits, _verify_in(hits))
    assert issues[0] == "derivation: operand b's extract does not state 286.45"
    # The retry is shown where the chunk does state it (CSS D. 622-7's «1/ 730e»
    # was a sentence away from the one the model quoted twice).
    assert issues[1] == "derivation: operand b: its chunk states 286.45 in «jonger is dan 6 jaar: € 286,45» — quote that"


def test_derivation_rejects_a_paraphrased_operand_and_an_unretrieved_chunk():
    hits = [_hit(chunk_id="akw", content=AKW_TEXT)]
    draft = _derived(operands=[
        Operand(name="a", value=347.83, citation_chunk_id="akw",
                supporting_extract="between 6 and 12 years: € 347,83"),
        Operand(name="b", value=286.45, citation_chunk_id="elsewhere",
                supporting_extract="jonger dan 6 jaar: € 286,45"),
    ])
    issues, offsets, _ = _check_derivation(draft, hits, _verify_in(hits))
    assert offsets == [None, None]
    assert any("not a verbatim quote" in i for i in issues)
    assert any("not retrieved" in i for i in issues)


CSG_TEXT = (
    "2° Sont assujetties à la contribution au taux de 8,3 % les pensions de retraite, et les "
    "pensions d'invalidité. III.-Par dérogation aux I, II et III bis, sont assujettis"
)


def test_a_tidied_quote_is_answered_with_the_passage_it_tried_to_quote():
    # 3 Nov full run: the model "corrected" la contribution into la contribution
    # sociale, and the bare retry repeated the same quote.
    tidied = "2° Sont assujetties à la contribution sociale au taux de 8,3 % les pensions de retraite, et les pensions d'invalidité."
    assert closest_passage(CSG_TEXT, tidied) == (
        "2° Sont assujetties à la contribution au taux de 8,3 % les pensions de retraite, et les "
        "pensions d'invalidité."
    )
    assert closest_passage(CSG_TEXT, "Le taux forfaitaire est fixé à 12,8 %") is None
    hint = _misquote_hint([_hit(chunk_id="csg", content=CSG_TEXT)], "csg", tidied)
    assert hint.startswith("the cited chunk reads: «2° Sont assujetties à la contribution au taux")


def test_a_paraphrased_operand_gets_the_same_hint():
    hits = [_hit(chunk_id="akw", content=AKW_TEXT)]
    draft = _derived(operands=[
        Operand(name="a", value=347.83, citation_chunk_id="akw",
                supporting_extract="b. 6 jaar of ouder en jonger dan 12 jaar: € 347,83"),
        Operand(name="b", value=286.45, citation_chunk_id="akw",
                supporting_extract="jonger is dan 6 jaar: € 286,45"),
    ])
    issues, _, _ = _check_derivation(draft, hits, _verify_in(hits))
    assert issues[0] == "derivation: operand a's extract is not a verbatim quote of its chunk"
    assert "«b. 6 jaar of ouder, maar jonger is dan 12 jaar: € 347,83" in issues[1]


def test_derivation_must_evaluate_to_the_proposed_value():
    hits = [_hit(chunk_id="akw", content=AKW_TEXT)]
    issues, _, _ = _check_derivation(_derived(value_scalar=1.3), hits, _verify_in(hits))
    assert issues and "evaluates to 1.21428" in issues[0]


def test_figures_are_read_in_every_european_spelling():
    assert 1801.80 in _figures_in("11,88 € par heure, soit 1 801,80 € par mois")
    assert 1801.80 in _figures_in("1.801,80 euros")
    assert 9139.0 in _figures_in("vermeerderd met € 9.139")  # Dutch thousands
    assert 2.1 in _figures_in("artikel 2.10") and 44000.0 in _figures_in("€44,000")


def test_a_table_row_states_each_of_its_amounts():
    # arrêté du 27 sept. 2019 art. 7, zone I: the PDF row is one run of digits
    row = _figures_in("I 329,71 397,64 449,43 65,21 II")
    assert {329.71, 397.64, 449.43, 65.21} <= row
    assert 801.80 not in _figures_in("1 801,80 €")


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


# ---------------------------------------------------------------------------
# The queue item and run_parameter on an in-memory record (ADR 0004)
# ---------------------------------------------------------------------------


def _item_kwargs(**extra) -> dict:
    return dict(
        id="fr_euromod_fr_test_2025",
        run_id="run-1",
        created_at="2026-07-09T00:00:00Z",
        country="FR",
        model_target="euromod://FR/test",
        as_of=date(2025, 7, 1),
        system_year=2025,
        value_type="scalar",
        unit="/1",
        routing=Routing.UNCHANGED,
        **extra,
    )


def test_review_item_still_loads_the_old_parameter_file_key():
    """Items stored before the queue moved into the DB named the materialized file."""
    stored = {**_item_kwargs(), "as_of": "2025-07-01", "parameter_file": "data/parameters/db/x.json"}
    loaded = ReviewItem.model_validate(stored)
    assert loaded.parameter_ref == "data/parameters/db/x.json"
    assert "parameter_ref" in loaded.model_dump(mode="json")
    assert "parameter_file" not in loaded.model_dump(mode="json")
    fresh = ReviewItem(**_item_kwargs(), parameter_ref="group:FR:tinkt_fr:tin_schedule")
    assert ReviewItem.model_validate(fresh.model_dump(mode="json")).parameter_ref == fresh.parameter_ref


def _offline_cfg():
    """A config that cannot reach any DB: the run must not need one."""
    from nomoscope_workflow.config import WorkflowConfig

    return WorkflowConfig(
        database_url="postgresql://nobody@127.0.0.1:1/nothing",
        model="mock/extractor",
        critique_model="mock/extractor",
        tracing_enabled=False,
        scout="off",
    )


def test_run_parameter_takes_a_record_and_can_skip_the_queue(capsys):
    """run_parameter(cfg, tracer, record, as_of, enqueue=False) returns the item without writing.

    A national-team-sourced value is routed before any retrieval, so this
    exercises the whole record -> item path with no DB at all; record_run_safe
    only prints its warning.
    """
    from nomoscope_workflow.pipeline import run_parameter
    from nomoscope_workflow.schema import SourceType
    from nomoscope_workflow.tracing import setup_tracing

    record = ParameterRecord(
        information=ParameterInformation(
            country="FR", model_target="euromod://FR/nt_fr/def_const/$nt_test",
            value_type="scalar", unit="/1",
        ),
        values=[ParameterValue(value=0.45, valid_from=date(2024, 1, 1), source_type=SourceType.NATIONAL_TEAM)],
    )
    cfg = _offline_cfg()
    item = run_parameter(
        cfg, setup_tracing(cfg), record, date(2025, 7, 1),
        parameter_ref="euromod://FR/nt_fr/def_const/$nt_test", enqueue=False,
    )
    assert item.routing == Routing.NATIONAL_TEAM_SOURCE
    assert item.id == "fr_euromod_fr_nt_fr_def_const_nt_test_2025"
    assert item.system_year == 2025
    assert item.parameter_ref == "euromod://FR/nt_fr/def_const/$nt_test"
    assert item.status == ItemStatus.PENDING
    assert "not recorded" in capsys.readouterr().out  # record_run_safe stayed best-effort

    # parameter_ref defaults to the record's model_target
    assert run_parameter(cfg, setup_tracing(cfg), record, date(2025, 7, 1), enqueue=False).parameter_ref == record.information.model_target


def test_run_parameter_with_enqueue_fails_when_the_queue_is_unreachable():
    """The queue is rows: no DB, no item — never a silent file fallback."""
    from nomoscope_workflow.pipeline import run_parameter
    from nomoscope_workflow.schema import SourceType
    from nomoscope_workflow.tracing import setup_tracing

    record = ParameterRecord(
        information=ParameterInformation(country="FR", model_target="euromod://FR/test", value_type="scalar", unit="/1"),
        values=[ParameterValue(value=0.45, valid_from=date(2024, 1, 1), source_type=SourceType.NATIONAL_TEAM)],
    )
    cfg = _offline_cfg()
    with pytest.raises(Exception):
        run_parameter(cfg, setup_tracing(cfg), record, date(2025, 7, 1))


def test_scout_reads_a_publisher_document_off_its_url():
    from nomoscope_workflow.scout import guidance_document

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
    from nomoscope_workflow import scout as scout_mod
    from nomoscope_workflow.config import WorkflowConfig

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

    monkeypatch.setattr(scout_mod, "_web_search_unavailable", None)
    monkeypatch.setattr(scout_mod, "_tavily_search", fake_search)
    monkeypatch.setattr(
        scout_mod.llm,
        "run_agent",
        lambda *a, **k: scout_mod.ScoutSuggestion(
            search_queries=["plafond ASI couple 2025"],
            guidance_queries=["circulaire Cnav 2025 plafonds ASI revalorisation"],
        ),
    )
    monkeypatch.setattr(scout_mod, "_known_instruments", lambda cfg, ids, rules: set())
    monkeypatch.setattr(scout_mod, "_run_ingest_cli", lambda cfg, args, what: ran.append(args))
    monkeypatch.setattr(scout_mod, "_build_embeddings", lambda cfg: None)

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


def test_a_mistyped_operand_chunk_id_is_resolved_by_its_extract():
    # 3 Nov full run: 11 derivations rejected as "cites a chunk that was not
    # retrieved" — the ids were a citation string or one hex digit off.
    hits = [_hit(chunk_id="akw", content=AKW_TEXT)]
    draft = _derived(operands=[
        Operand(name="a", value=347.83, citation_chunk_id="JORFTEXT000051393086",
                supporting_extract="6 jaar of ouder, maar jonger is dan 12 jaar: € 347,83"),
        Operand(name="b", value=286.45, citation_chunk_id="akw",
                supporting_extract="jonger is dan 6 jaar: € 286,45"),
    ])
    issues, offsets, _ = _check_derivation(draft, hits, _verify_in(hits))
    assert issues == [] and None not in offsets
    assert draft.operands[0].citation_chunk_id == "akw"
    # Not in any retrieved chunk: still refused, nothing guessed.
    draft.operands[0].citation_chunk_id = "elsewhere"
    draft.operands[0].supporting_extract = "between 6 and 12 years: € 347,83"
    issues, _, _ = _check_derivation(draft, hits, _verify_in(hits))
    assert any("not retrieved" in i for i in issues)


def test_a_schedule_may_derive_one_of_its_figures():
    # 3 Nov full run: five schedules with exactly EUROMOD's bands were rejected
    # as "only a scalar value can be derived" (AGIRC-ARRCO CET share a * b).
    text = "contribution d'équilibre technique, au taux de 0,35 % ... répartie à raison de 60 % à la charge des employeurs et 40 % à la charge des salariés"
    hits = [_hit(chunk_id="ani", content=text)]
    ops = [
        Operand(name="a", value=0.0035, citation_chunk_id="ani", supporting_extract="au taux de 0,35 %"),
        Operand(name="b", value=0.4, citation_chunk_id="ani", supporting_extract="40 % à la charge des salariés"),
    ]
    good = _derived(value_scalar=None, value_brackets=[Bracket(threshold=0.0, rate=0.0014)],
                    derivation="a * b", operands=ops, supporting_extract="au taux de 0,35 %", citation_chunk_id="ani")
    assert _check_derivation(good, hits, _verify_in(hits))[0] == []
    wrong = good.model_copy(update={"value_brackets": [Bracket(threshold=0.0, rate=0.0035)]})
    issues, _, _ = _check_derivation(wrong, hits, _verify_in(hits))
    assert issues == ["derivation: a * b evaluates to 0.0014, not any figure of the proposed schedule"]


def test_a_negative_rate_is_sane_and_an_unnormalised_percentage_is_not():
    # «Majoration par personne à charge -0,06%» ($bho_Tf_rate8, 3 Nov run).
    assert _values_sane("/1", ProposalDraft(found=True, value_scalar=-0.0006))
    assert not _values_sane("/1", ProposalDraft(found=True, value_scalar=11.0))
    assert not _values_sane("/1", ProposalDraft(found=True, value_scalar=-6.0))


def test_a_derived_amount_is_rounded_like_the_amount_held():
    # PAJE ceiling 29 169 × 1,8 = 52 504,2, published 52 504; RSA
    # 646,52 × 1,8 = 1 163,736, paid 1 163,74 (4 Nov round-2 run).
    def held(value):
        return ParameterValue(value=value, valid_from=date(2024, 1, 1))

    ceiling = ProposalDraft(found=True, value_scalar=52504.2)
    assert "52504" in _round_like_held("currency", ceiling, held(51229.0))
    assert ceiling.value_scalar == 52504
    half = ProposalDraft(found=True, value_scalar=8750.5)
    _round_like_held("currency", half, held(8546.0))
    assert half.value_scalar == 8751
    rsa = ProposalDraft(found=True, value_scalar=1163.736)
    _round_like_held("currency", rsa, held(1143.28))
    assert rsa.value_scalar == 1163.74
    # Unknown precision: cents. Already at the precision: untouched.
    loose = ProposalDraft(found=True, value_scalar=258.608)
    _round_like_held("currency", loose, None)
    assert loose.value_scalar == 258.61
    assert _round_like_held("currency", ProposalDraft(found=True, value_scalar=52504.0), held(1.0)) is None
    rate = ProposalDraft(found=True, value_scalar=0.0787)
    assert _round_like_held("/1", rate, held(0.08)) is None and rate.value_scalar == 0.0787
    # A rate held with four or more decimals: as many. A coarser one: untouched.
    pi = ProposalDraft(found=True, value_scalar=0.12954)
    assert _round_like_held("/1", pi, held(0.1295)) and pi.value_scalar == 0.1295
    fine = ProposalDraft(found=True, value_scalar=0.047244)
    _round_like_held("/1", fine, held(0.0472))
    assert fine.value_scalar == 0.0472
    coarse = ProposalDraft(found=True, value_scalar=0.0675)
    assert _round_like_held("/1", coarse, held(0.068)) is None and coarse.value_scalar == 0.0675


def test_an_article_number_belongs_to_the_code_named_after_it():
    codes = {"css": "code de la sécurité sociale", "cgi": "code général des impôts",
             "cgi3": "code général des impôts, annexe iii"}
    text = (
        "Le plafond prévu au dernier alinéa de l'article L. 531-2 du code de la sécurité sociale "
        "et au premier alinéa de l'article L. 531-3 du même code. Voir l'article 46 quater-0 YE "
        "et l'article R. 522-2. Article 1417 du code général des impôts, annexe III : D. 41-1."
    )
    # An order (no code of its own): a bare R. 522-2 has no code and is skipped.
    assert _code_refs(text, None, codes) == [("css", "L531-2"), ("css", "L531-3")]
    # A CSS article: its bare references are to itself.
    assert ("css", "R522-2") in _code_refs(text, "css", codes)
    assert _code_refs("l'article D. 41-1 du code général des impôts, annexe III", None, codes) == [("cgi3", "D41-1")]


def test_a_version_entered_since_reads_the_range_start():
    from nomoscope_workflow.retrieval import _entered_since

    assert _entered_since("[2025-04-01,)", date(2024, 7, 1))
    assert not _entered_since("[2006-01-01,)", date(2024, 7, 1))
    assert not _entered_since(None, date(2024, 7, 1))


def test_a_word_split_by_pdf_extraction_still_matches_but_digits_do_not():
    import re as _re

    from nomoscope_workflow.retrieval import _split_word_pattern

    chunk = "en pourcentage duquel sont fixées les prestati ons \nfamiliales, est donc porté de 466,44 €"
    assert _re.search(_split_word_pattern("sont fixées les prestations familiales, est donc"), chunk)
    assert not _re.search(_split_word_pattern("sont fixées les prestataires familiales"), chunk)
    assert not _re.search(_split_word_pattern("25 %"), "taux 2 5 %")
    assert not _re.search(_split_word_pattern("466,44 €"), "46 6,44 €")


def test_a_quote_ending_on_other_punctuation_than_the_text_still_verifies():
    from unittest.mock import MagicMock

    from nomoscope_workflow.retrieval import verify_extract

    conn = MagicMock()
    content = "2° A 16 % du montant forfaitaire calculé pour deux personnes lorsque le foyer se compose de deux personnes ; 3° A 16,5 %"
    conn.execute.return_value.fetchone.return_value = {"content": content, "char_start": 0}
    assert verify_extract(conn, "c", "2° A 16 % du montant forfaitaire calculé pour deux personnes lorsque le foyer se compose de deux personnes.")
    assert verify_extract(conn, "c", "« 2° A 16 % du montant forfaitaire »")
    assert verify_extract(conn, "c", "2° A 17 % du montant forfaitaire.") is None


def test_months_either_side_of_a_mid_year_revaluation_may_appear_unquoted():
    assert evaluate_derivation("(a * 3 + b * 9) / 12", {"a": 622.63, "b": 633.21}) == pytest.approx(630.565)


def test_a_figure_spelt_out_in_words_is_stated():
    from nomoscope_workflow.pipeline import _extract_states

    assert _extract_states("dans la limite de trois fois ce plafond", 3.0)
    assert _extract_states("égal à la moitié du montant du plafond annuel", 0.5)
    assert not _extract_states("dans la limite de trois fois ce plafond", 4.0)


def test_a_proposal_confirming_the_held_value_is_recognised():
    from nomoscope_workflow.pipeline import _confirms_held
    from nomoscope_workflow.schema import ParameterValue

    held = ParameterValue(value=0.07, valid_from=date(2024, 1, 1))
    assert _confirms_held(ProposalDraft(found=True, value_scalar=0.07), held)
    assert not _confirms_held(ProposalDraft(found=True, value_scalar=0.06), held)
    assert not _confirms_held(ProposalDraft(found=True, value_scalar=0.07), None)


def test_a_list_of_articles_takes_the_code_named_at_its_end():
    codes = {"css": "code de la sécurité sociale"}
    text = (
        "Textes de référence - Articles L. 381-1, L. 545-1, R. 522-2, R. 522-4, R. 531-1, "
        "R. 543- 5, R. 755 -2, D. 521- 1, D. 521-2 et D. 521-3 du code de la sécurité sociale"
    )
    refs = _code_refs(text, None, codes)
    assert ("css", "R522-2") in refs and ("css", "L381-1") in refs
    # prose between the number and the code: not a list, no reference
    assert _code_refs("l'article R. 522-2 dont il est question plus loin dans le code de la sécurité sociale", None, codes) == []


def test_a_multiplier_is_stated_by_the_increase_it_applies():
    from nomoscope_workflow.pipeline import _extract_states

    assert _extract_states("est majoré de 50 % lorsque le foyer comporte deux personnes", 1.5)
    assert not _extract_states("est fixé à 50 % du plafond", 1.5)  # no increase: 50 % is 0.5
    assert not _extract_states("est majoré de 50 %", 1.3)


def test_an_average_labelled_amount_is_proposed_as_the_amount_in_force():
    from types import SimpleNamespace

    from nomoscope_workflow.prompts import _average_note

    fya = SimpleNamespace(label={"en": "Base amount - FYA"}, short_label=None, description={})
    plain = SimpleNamespace(label={"en": "Base amount"}, short_label=None, description={})
    held = SimpleNamespace(lineage=SimpleNamespace(model_answer="938.64"))
    formula = SimpleNamespace(lineage=SimpleNamespace(model_answer="(498.39*9+514.64*3)/12#m"))
    assert "IN FORCE" in _average_note(fya, held)
    assert "IN FORCE" in _average_note(plain, formula)
    assert _average_note(plain, held) == ""


def test_a_quote_citing_the_wrong_retrieved_chunk_is_repointed_to_the_one_holding_it():
    from nomoscope_workflow.pipeline import _repoint_misquoted

    hits = [
        RetrievalHit(chunk_id="r5222", citation="CSS R522-2", content="Le plafond est majoré de 25 %"),
        RetrievalHit(chunk_id="dss", citation="DSS/2B/2025/38", content="PREPARE\nTaux plein 96,62 % 458,34"),
        RetrievalHit(chunk_id="dss2", citation="DSS/2B/2025/38", content="CMG maximal 540,97"),
    ]
    assert _repoint_misquoted(hits, "r5222", "Taux plein 96,62 % 458,34") == "dss"
    assert _repoint_misquoted(hits, "dss", "Taux plein 96,62 % 458,34") is None  # already right
    assert _repoint_misquoted(hits, "r5222", "Taux plein 99 %") is None  # nowhere: the failure stands
