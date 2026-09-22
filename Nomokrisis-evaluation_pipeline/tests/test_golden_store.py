"""eval.golden_cases / golden_selections / embedding_cases round trips (dev DB),
plus the content hash and the legacy-key guard, which need no database."""

from __future__ import annotations

import json
from datetime import date

import pytest
from typer.testing import CliRunner
from pydantic import ValidationError

from nomoscope_workflow.schema import Routing

from nomokrisis_eval import golden_store
from nomokrisis_eval.cli import app
from nomokrisis_eval.schema import EmbeddingCase, Expected, GoldenCase

from conftest import TEST_PREFIX


def make_case(case_id: str = TEST_PREFIX + "fr_pss", value=47100.0, **kwargs) -> GoldenCase:
    return GoldenCase(
        id=case_id,
        country="FR",
        language="fr",
        parameter_target="euromod://FR/ConstDef_fr/def_const/$PSS",
        as_of=date(2025, 6, 1),
        expected=Expected(routing=Routing.UNCHANGED, value=value, citations=["JORFTEXT000050854392"]),
        drafted_by="human",
        **kwargs,
    )


# --------------------------------------------------------------------------- #
# No database
# --------------------------------------------------------------------------- #


def test_golden_set_hash_is_content_only():
    a, b = make_case("a"), make_case("b")
    digest = golden_store.golden_set_hash([a, b])
    assert len(digest) == 12
    assert digest == golden_store.golden_set_hash([b, a])
    # A verdict is not content: flipping it must not change the set's identity.
    reviewed = make_case("a", verified=True, reviewed_by="ben", review_note="ok")
    assert digest == golden_store.golden_set_hash([reviewed, b])
    # The ground truth is.
    assert digest != golden_store.golden_set_hash([make_case("a", value=47101.0), b])
    assert digest != golden_store.golden_set_hash([a])


def test_legacy_parameter_file_is_refused_outside_the_importer():
    payload = make_case().model_dump(mode="json")
    payload["parameter_file"] = payload.pop("parameter_target")
    with pytest.raises(ValidationError, match="import-golden"):
        GoldenCase.model_validate(payload)
    # The importer says who it is and maps the key itself before validating.
    payload["parameter_target"] = payload.pop("parameter_file")
    assert GoldenCase.model_validate(payload, context={"legacy_parameter_file": True}).parameter_target


def test_selection_document_is_the_old_file_shape():
    header = {"country": "ZZ", "language": "zz", "corpus": "curated", "conventions": {"x": 1}}
    entries = [{"model_target": "euromod://ZZ/x_zz/def_const/$x"}]
    doc = golden_store.selection_document({**header, "entries": ["stale"]}, entries)
    # header keys first, in their stored order, `entries` last and the real ones
    assert list(doc) == ["country", "language", "corpus", "conventions", "entries"]
    assert doc["entries"] == entries
    # and it reads back as the header/entries pair it came from
    assert golden_store.selection_identity(doc) == ("ZZ", "curated")


def test_selection_identity_reads_the_header_then_the_filename():
    assert golden_store.selection_identity({"country": "fr", "corpus": "openfisca"}) == ("FR", "openfisca")
    # no header: the filename decides, the way import-golden read golden_sources/
    assert golden_store.selection_identity({}, "golden_sources/openfisca_fr.json") == ("FR", "openfisca")
    assert golden_store.selection_identity({}, "/tmp/lt.json") == ("LT", "curated")
    # the header's country wins over the filename; an unknown `corpus` falls back to the name
    assert golden_store.selection_identity({"country": "ES", "corpus": "hand"}, "openfisca_fr.json") == ("ES", "openfisca")
    with pytest.raises(ValueError, match="country"):
        golden_store.selection_identity({"corpus": "curated"})


# --------------------------------------------------------------------------- #
# Dev database
# --------------------------------------------------------------------------- #


def test_case_round_trip_and_verdict_columns(db):
    case = make_case()
    golden_store.save_case(db, case)
    loaded = golden_store.load_case(db, case.id)
    assert loaded is not None
    assert loaded.parameter_target == case.parameter_target
    assert loaded.expected == case.expected
    assert loaded.verified is False and loaded.reviewed_by is None

    # The human gate stamps the DB login, not a caller-supplied name.
    verified = golden_store.set_verified(db, case.id, True, "checked against the arrêté")
    assert verified is not None and verified.verified
    assert verified.reviewed_by == db.execute("SELECT current_user").fetchone()[0]
    assert verified.reviewed_at is not None
    assert verified.review_note == "checked against the arrêté"

    # save_case never touches the verdict, whatever the object says.
    case.notes = "provenance refreshed"
    case.verified = False
    golden_store.save_case(db, case)
    again = golden_store.load_case(db, case.id)
    assert again.notes == "provenance refreshed" and again.verified is True

    # Filters.
    assert case.id in {c.id for c in golden_store.load_cases(db, countries=["fr"], verified_only=True)}
    assert case.id not in {c.id for c in golden_store.load_cases(db, languages=["de"])}
    assert golden_store.set_verified(db, TEST_PREFIX + "nope", True) is None
    assert golden_store.delete_case(db, case.id) and golden_store.load_case(db, case.id) is None


def test_carry_over_keeps_the_verdict_only_while_the_ground_truth_stands(db):
    golden_store.save_case(db, make_case())
    golden_store.set_verified(db, TEST_PREFIX + "fr_pss", True, "ok")

    # Same ground truth, refreshed provenance: the verdict survives.
    redraft = make_case(notes="rebuilt")
    assert golden_store.save_drafted_case(db, redraft) is False
    kept = golden_store.load_case(db, redraft.id)
    assert kept.verified and kept.reviewed_by and kept.notes == "rebuilt"
    assert redraft.verified  # the caller's object reflects the row

    # The expected value moved: the approval was for a different value.
    moved = make_case(value=47200.0)
    assert golden_store.save_drafted_case(db, moved) is True
    reset = golden_store.load_case(db, moved.id)
    assert reset.verified is False and reset.reviewed_by is None and reset.review_note is None
    assert reset.expected.value == 47200.0


def test_selection_round_trip(db):
    header = {"country": "ZZ", "language": "zz", "corpus": "curated", "description": "test"}
    entries = [{"model_target": "euromod://ZZ/x_zz/def_const/$x", "expected_value": 1.0}]
    with pytest.raises(KeyError, match="import-golden|ZZ"):
        golden_store.load_selection(db, "ZZ", "curated")
    golden_store.save_selection(db, "zz", "curated", {**header, "entries": ["ignored"]}, entries)
    got_header, got_entries = golden_store.load_selection(db, "ZZ", "curated")
    assert got_header == header and got_entries == entries
    golden_store.save_selection(db, "ZZ", "curated", header, [])
    assert golden_store.load_selection(db, "ZZ", "curated")[1] == []
    with pytest.raises(ValueError):
        golden_store.save_selection(db, "ZZ", "handwritten", header, [])


def test_selection_kinds_lists_what_the_country_has(db):
    header = {"country": "ZZ", "language": "zz"}
    assert golden_store.selection_kinds(db, "ZZ") == []
    golden_store.save_selection(db, "ZZ", "openfisca", header, [])
    assert golden_store.selection_kinds(db, "zz") == ["openfisca"]
    golden_store.save_selection(db, "ZZ", "curated", header, [{"model_target": "t"}])
    assert golden_store.selection_kinds(db, "ZZ") == ["openfisca", "curated"]
    assert [(r["country"], r["kind"], r["entries"]) for r in golden_store.list_selections(db) if r["country"] == "ZZ"] == [
        ("ZZ", "curated", 1), ("ZZ", "openfisca", 0)
    ]


def test_selection_export_import_round_trip_through_the_cli(db, tmp_path):
    runner = CliRunner()
    header = {"country": "ZZ", "language": "zz", "corpus": "curated", "description": "cli round trip"}
    entries = [{"model_target": "euromod://ZZ/x_zz/def_const/$x", "expected_value": "1#m", "note": "EASY"}]
    golden_store.save_selection(db, "ZZ", "curated", header, entries)

    # export: the single kind needs no --kind; the file is the old golden_sources shape
    out = tmp_path / "zz.json"
    result = runner.invoke(app, ["selection-export", "ZZ", "--out", str(out)])
    assert result.exit_code == 0, result.output
    doc = json.loads(out.read_text(encoding="utf-8"))
    assert doc == {**header, "entries": entries}
    assert list(doc)[-1] == "entries"
    # to stdout too
    result = runner.invoke(app, ["selection-export", "zz"])
    assert result.exit_code == 0 and json.loads(result.output) == doc

    # two kinds and no --kind is an error, not a guess
    golden_store.save_selection(db, "ZZ", "openfisca", {"country": "ZZ"}, [])
    result = runner.invoke(app, ["selection-export", "ZZ"])
    assert result.exit_code == 1 and "--kind" in result.output
    result = runner.invoke(app, ["selection-export", "ZZ", "--kind", "openfisca"])
    assert result.exit_code == 0 and json.loads(result.output)["entries"] == []
    result = runner.invoke(app, ["selection-export", "ZZ", "--kind", "handwritten"])
    assert result.exit_code == 2

    # edit the file, import it back: the row follows the file, the reminder names the builder
    doc["entries"].append({"model_target": "euromod://ZZ/x_zz/def_const/$y", "expected_value": None})
    doc["description"] = "edited"
    out.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    result = runner.invoke(app, ["selection-import", str(out)])
    assert result.exit_code == 0, result.output
    assert "2 entries" in result.output and "build-curated-dataset --country ZZ" in result.output
    got_header, got_entries = golden_store.load_selection(db, "ZZ", "curated")
    assert got_header["description"] == "edited" and "entries" not in got_header
    assert got_entries == doc["entries"]
    # the openfisca row was not touched
    assert golden_store.load_selection(db, "ZZ", "openfisca")[1] == []

    # --country / --kind override what the file says; a bad kind is refused before writing
    result = runner.invoke(app, ["selection-import", str(out), "--kind", "openfisca"])
    assert result.exit_code == 0 and "build-openfisca-dataset" in result.output
    assert len(golden_store.load_selection(db, "ZZ", "openfisca")[1]) == 2
    result = runner.invoke(app, ["selection-import", str(out), "--kind", "handwritten"])
    assert result.exit_code == 2
    result = runner.invoke(app, ["selection-import", str(tmp_path / "missing.json")])
    assert result.exit_code == 1

    # listing shows both rows with their entry counts and the DB login
    result = runner.invoke(app, ["selections"])
    assert result.exit_code == 0
    me = db.execute("SELECT current_user").fetchone()[0]
    assert f"ZZ  curated   entries=2" in result.output and me in result.output


def test_embedding_case_round_trip(db):
    case = EmbeddingCase(
        id=TEST_PREFIX + "fr_pss_2025",
        country="FR",
        language="en",
        corpus_lang="fr",
        as_of=date(2025, 6, 1),
        query="social security ceiling 2025",
        expected_citations=["JORFTEXT000050854392, art. 1"],
        verified=True,
    )
    golden_store.save_embedding_case(db, case)
    loaded = [c for c in golden_store.load_embedding_cases(db, countries=["FR"], verified_only=True) if c.id == case.id]
    assert loaded == [case]
    assert not [c for c in golden_store.load_embedding_cases(db, languages=["de"]) if c.id == case.id]
