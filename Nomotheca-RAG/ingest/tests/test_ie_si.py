"""Irish statutory instruments (eISB print HTML, as made): no network."""

import uuid
from datetime import date

from nomotheca_ingest.core.ir import CitationRef, Snapshot, SourceRef
from nomotheca_ingest.countries.ie.adapter import IE_URL_SOURCE
from nomotheca_ingest.countries.ie.fetcher import url_for_ref
from nomotheca_ingest.countries.ie.resolver import IeResolver
from nomotheca_ingest.countries.ie.si import parse_si

P = '<tr><td></td><td></td><td valign="top"><p style="display:block;{style}">{text}</p>'
PAGE = (
    "<html><head><title>S.I. No. 9/2025 - Social Welfare (Income Limit) Regulations 2025</title></head><body>"
    '<div class="act-content" id="act"><table>'
    + P.format(style="text-align:center;", text="ARRANGEMENT OF ARTICLES")
    + P.format(style="", text="1. Citation.")
    + P.format(style="", text="2. Commencement.")
    + P.format(
        style="",
        text="I, A MINISTER, in exercise of the powers conferred on me, hereby make the following Regulations:",
    )
    + P.format(
        style="", text="1. These Regulations may be cited as the Social Welfare (Income Limit) Regulations 2025."
    )
    + P.format(style="", text="2. These Regulations come into operation on the 1st day of January 2025.")
    + P.format(style="", text="Income limit")
    + P.format(style="", text="3. (1) The weekly income limit is &euro;400.")
    + P.format(style="", text="1. a numbered item that opens nothing")
    + P.format(style="text-align:center;", text="SCHEDULE 1")
    + '<tr><td></td><td></td><td><table class="t1"><tr><td><p>Income</p></td><td><p>Increase</p></td></tr>'
    "<tr><td><p>Up to &euro;100.00</p></td><td><p>123.30</p></td></tr></table>"
    + P.format(style="", text="GIVEN under my Official Seal,")
    + P.format(style="", text="18 December, 2024.")
    + P.format(style="text-align:center;", text="EXPLANATORY NOTE")
    + P.format(style="", text="These Regulations raise the limit to &euro;999.")
    + "<!--End Content--></table></div></body></html>"
).encode()


def _parse():
    ref = SourceRef(jurisdiction="IE", source_code="IE-EISB", source_id="2025/si/9", source_type="statutory_instrument")
    snapshot = Snapshot(
        id=uuid.uuid4(),
        source_code="IE-EISB",
        url="https://www.irishstatutebook.ie/x",
        content_hash="x",
        raw_content=PAGE,
    )
    return parse_si(PAGE, ref, snapshot).instruments[0]


def test_provisions_start_after_the_enacting_words_and_follow_their_numbers():
    instrument = _parse()
    assert instrument.instrument_type == "statutory_instrument"
    assert instrument.title["en"] == "Social Welfare (Income Limit) Regulations 2025 (S.I. No. 9 of 2025)"
    assert [u.citation.rsplit(", ", 1)[1] for u in instrument.units] == ["reg. 1", "reg. 2", "reg. 3", "Sch. 1"]
    three = instrument.units[2].versions[0].texts[0].content
    assert three.startswith("Income limit\n3. (1) The weekly income limit is €400.")
    assert "a numbered item that opens nothing" in three
    assert "Income limit" not in instrument.units[1].versions[0].texts[0].content


def test_a_table_keeps_its_rows_and_the_note_and_signature_are_left_out():
    instrument = _parse()
    schedule = instrument.units[-1].versions[0].texts[0].content
    assert "Up to €100.00 | 123.30" in schedule
    everything = "\n".join(u.versions[0].texts[0].content for u in instrument.units)
    assert "999" not in everything and "Official Seal" not in everything


def test_every_provision_starts_on_the_stated_commencement_date():
    instrument = _parse()
    assert instrument.adoption_date == date(2024, 12, 18)
    assert {u.versions[0].valid_from for u in instrument.units} == {date(2025, 1, 1)}
    assert instrument.units[0].versions[0].amendment_note["as_made"] is True


def test_the_id_resolves_and_fetches_the_print_page():
    (ref,) = IeResolver().resolve(CitationRef(jurisdiction="IE", citation="2017/si/56"), date(2025, 7, 1))
    assert ref.source_type == "statutory_instrument"
    assert url_for_ref(ref) == "https://www.irishstatutebook.ie/eli/2017/si/56/made/en/print"
    assert IE_URL_SOURCE.id_pattern.findall("https://www.irishstatutebook.ie/eli/2017/si/56/made/en/html") == [
        "2017/si/56"
    ]
