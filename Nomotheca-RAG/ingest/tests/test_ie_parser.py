"""Parser and adapter tests for the Irish payloads (inline fixtures).

XML excerpts are trimmed verbatim from the live eISB responses for Finance Act
2024 (2024/act/43), Social Welfare Act 2024 (2024/act/36) and the Taxes
Consolidation Act 1997 (1997/act/39); the JSON is trimmed from
api.oireachtas.ie/v1/legislation?act_year=2024.
"""

import json
from datetime import date
from uuid import uuid4

import pytest

from nomotheca_ingest.countries.ie.adapter import IeAdapter
from nomotheca_ingest.countries.ie.parser import _effective_date, parse_ie
from nomotheca_ingest.countries.ie.resolver import IeResolver
from nomotheca_ingest.core.ir import CitationRef, Snapshot, SourceRef


FINANCE_ACT_XML = b"""<?xml version="1.0"?>
<act><metadata><title>FINANCE ACT 2024</title><number>43</number><year>2024</year>
<dateofenactment>20241112</dateofenactment></metadata>
<frontmatter><acttoc><p>3. Rate of charge and personal tax credits</p></acttoc></frontmatter>
<body>
<part>
<title><p><b>PART 1</b></p><p>Universal Social Charge, Income Tax</p></title>
<chapter>
<title><p>Chapter 2</p><p><i>Universal Social Charge</i></p></title>
<sect>
<number>2.</number>
<title><p><b>Amendment of section 531AN of Principal Act (rate of charge)</b></p></title>
<p><b>2.</b> (1) Section 531AN of the Principal Act is amended<emdash/></p>
<p>(a) in subsection (3), by the substitution of <odq/><euro/>27,382<cdq/> for <odq/><euro/>25,760<cdq/>, and</p>
<table width="100%"><colgroup><col width="50%"/></colgroup>
<tr><td><p>Part of aggregate income</p><p>(1)</p></td><td><p>Rate of universal social charge</p><p>(2)</p></td></tr>
<tr><td><p>The first <euro/>12,012</p></td><td><p>0.5 per cent</p></td></tr>
<tr><td><p>The remainder</p></td><td><p>8 per cent</p></td></tr>
</table>
<p>(2) <i>Subsection (1)</i> applies for the year of assessment 2025 and each subsequent year of assessment.</p>
</sect>
</chapter>
<chapter>
<title><p>Chapter 3</p><p><i>Income Tax</i></p></title>
<sect>
<number>3.</number>
<title><p><b>Rate of charge and personal tax credits</b></p></title>
<p><b>3.</b> As respects the year of assessment 2025 and subsequent years of assessment, the Principal Act is amended<emdash/></p>
<p>(a) in section 15<emdash/>(ii) by the substitution of the following Table for the Table to that section:</p>
<table><tr><td><p>The first <euro/>44,000</p></td><td><p>20 per cent</p></td><td><p>the standard rate</p></td></tr></table>
<p>(b) in section 461<emdash/>(iii) in paragraph (c), by the substitution of <odq/><euro/>2,000<cdq/> for <odq/><euro/>1,875<cdq/>.</p>
</sect>
</chapter>
</part>
</body>
<backmatter>
<schedule>
<title><p><b>SCHEDULE 1</b></p><p><b>Miscellaneous Technical Amendments</b></p></title>
<p>Section 99</p>
</schedule>
</backmatter>
</act>
"""

SOCIAL_WELFARE_ACT_XML = b"""<?xml version="1.0"?>
<act><metadata><title>SOCIAL WELFARE ACT 2024</title><number>36</number><year>2024</year>
<dateofenactment>20241028</dateofenactment></metadata>
<frontmatter><p>long title</p></frontmatter>
<body>
<sect>
<number>4.</number>
<title><p><b>Maternity benefit <emdash/> new rate</b></p></title>
<p><b>4.</b> (1) Section 49(1) of the Principal Act is amended by the substitution of <odq/><euro/>289<cdq/>.</p>
<p>(2) This section comes into operation on 6 January 2025.</p>
</sect>
<sect>
<number>16.</number>
<title><p><b>Social insurance benefits <endash/> new rates</b></p></title>
<p><b>16.</b> (1) Schedule 2 to the Principal Act is amended by the substitution of the Parts set out in Schedule 1.</p>
<p>(2) This section comes into operation<emdash/></p>
<p>(a) in so far as it relates to jobseeker<csq/>s benefit, on 26 December 2024,</p>
<p>(b) in so far as it relates to illness benefit, on 2 January 2025, and</p>
<p>(c) in so far as it relates to State pension (contributory), on 3 January 2025.</p>
</sect>
</body>
<backmatter>
<schedule id="SCHED1">
<title><p><b>SCHEDULE 1</b></p><p><b>Social Insurance Benefits (New Rates)</b></p></title>
<p>Section 16</p>
<table>
<tr><td><p>Description of benefit</p><p>(1)</p></td><td><p>Weekly rate</p><p>(2)</p></td></tr>
<tr><td><p>State Pension (Contributory)</p></td><td><p>289.30</p></td></tr>
</table>
</schedule>
</backmatter>
</act>
"""

# The TCA dialect: <title> before <number>, id attributes, no trailing dot.
TCA_XML = b"""<?xml version="1.0"?>
<act><metadata><title>TAXES CONSOLIDATION ACT, 1997</title><number>39</number><year>1997</year>
<dateofenactment>19971130</dateofenactment></metadata>
<frontmatter><p>long title</p></frontmatter>
<body>
<part id="PART2">
<title><p>PART 2</p><p><font>Income Tax</font></p></title>
<sect id="SEC15">
<title><p><font>Rate of charge.</font></p><p><font>[FA91 s2; FA97 s2(1) and (2)]</font></p></title>
<number>15</number>
<p><b>15.</b><emdash/>(1) Income tax shall be charged at the standard rate as specified in the Table to this section.</p>
</sect>
</part>
</body>
<backmatter>
<schedule id="SCHED2">
<title><pc>SCHEDULE 2</pc><p><font>Machinery for Assessment, Charge and Payment of Tax</font></p></title>
<p>Section 1104</p>
</schedule>
</backmatter>
</act>
"""

ACT_INDEX_JSON = json.dumps(
    {
        "head": {"counts": {"billCount": 4}},
        "results": [
            {
                "bill": {
                    "act": {
                        "actNo": "43",
                        "actYear": "2024",
                        "dateSigned": "2024-11-12",
                        "shortTitleEn": "Finance Act 2024",
                        "shortTitleGa": "An tAcht Airgeadais, 2024",
                        "statutebookURI": "http://www.irishstatutebook.ie/eli/2024/act/43",
                    }
                }
            },
            {
                "bill": {
                    "act": {
                        "actNo": "36",
                        "actYear": "2024",
                        "dateSigned": "2024-10-28",
                        "shortTitleEn": "Social Welfare Act 2024",
                        "shortTitleGa": "An tAcht Leasa Shóisialaigh, 2024",
                        "statutebookURI": "http://www.irishstatutebook.ie/eli/2024/act/36",
                    }
                }
            },
            {
                "bill": {
                    "act": {
                        "actNo": "45",
                        "actYear": "2024",
                        "dateSigned": "2024-11-13",
                        "shortTitleEn": "Appropriation Act 2024",
                        "statutebookURI": "http://www.irishstatutebook.ie/eli/2024/act/45",
                    }
                }
            },
            {
                "bill": {
                    "act": {
                        "actNo": "3",
                        "actYear": "2024",
                        "dateSigned": "2024-02-14",
                        "shortTitleEn": (
                            "Finance (State Guarantees, International Financial Institution Funds "
                            "and Miscellaneous Provisions) Act 2024"
                        ),
                        "statutebookURI": "http://www.irishstatutebook.ie/eli/2024/act/3",
                    }
                }
            },
        ],
    }
).encode()


def _ref(source_id: str, source_type: str, source_code: str = "IE-EISB", **metadata) -> SourceRef:
    return SourceRef(
        jurisdiction="IE",
        source_code=source_code,
        source_id=source_id,
        source_type=source_type,
        metadata=metadata,
    )


def _snapshot(ref: SourceRef) -> Snapshot:
    return Snapshot(
        id=uuid4(),
        source_code=ref.source_code,
        url="https://www.irishstatutebook.ie/eli/2024/act/43/enacted/en/xml",
        http_status=200,
        content_type="application/xml",
        content_hash="0" * 64,
        raw_content=b"",
    )


def _units(payload: bytes, ref: SourceRef):
    doc = parse_ie(payload, ref, _snapshot(ref))
    instrument = doc.instruments[0]
    return doc, instrument, {unit.path: unit for unit in instrument.units}


def test_finance_act_nests_sections_under_part_and_chapter():
    ref = _ref("2024/act/43", "act", short_title="Finance Act 2024")
    doc, instrument, units = _units(FINANCE_ACT_XML, ref)

    assert instrument.national_id == "2024/act/43"
    assert instrument.title == {"en": "Finance Act 2024"}
    assert instrument.eli == "https://www.irishstatutebook.ie/eli/2024/act/43"
    assert instrument.adoption_date == date(2024, 11, 12)
    assert instrument.metadata["as_enacted_baseline"] is False
    assert doc.metadata["sections"] == 3

    assert set(units) == {
        "part_1",
        "part_1.chapter_2",
        "part_1.chapter_2.sect_2",
        "part_1.chapter_3",
        "part_1.chapter_3.sect_3",
        "sched_1",
    }
    assert units["part_1"].is_container is True
    assert units["part_1"].citation == "Finance Act 2024, Part 1"
    assert units["part_1.chapter_3"].parent_path == "part_1"
    assert units["part_1.chapter_3.sect_3"].is_container is False


def test_finance_act_section_carries_identity_validity_and_verbatim_amounts():
    ref = _ref("2024/act/43", "act", short_title="Finance Act 2024")
    snapshot = _snapshot(ref)
    doc = parse_ie(FINANCE_ACT_XML, ref, snapshot)
    section = next(u for u in doc.instruments[0].units if u.path.endswith("sect_3"))

    assert section.unit_type == "section"
    assert section.citation == "Finance Act 2024, s. 3"
    assert section.national_id == "2024/act/43/section/3"
    assert section.eli == "https://www.irishstatutebook.ie/eli/2024/act/43/section/3/enacted/en/html"

    version = section.versions[0]
    # "As respects the year of assessment 2025" is the only in-force statement
    # the source makes; it is what makes the act answerable at a point in time.
    assert version.valid_from == date(2025, 1, 1)
    assert version.valid_to is None
    assert version.status.value == "in_force"
    assert version.amendment_note == {"effective_date_basis": "year_of_assessment"}
    assert version.source_version_id == "2024/act/43/3/enacted"
    assert version.fetch_snapshot_id == snapshot.id

    content = version.texts[0].content
    assert version.texts[0].lang == "en"
    assert content.startswith("Section 3. Rate of charge and personal tax credits")
    # Canary values must survive verbatim: Nomoscope matches supporting extracts
    # character-for-character, so <euro/> and the curly quotes both matter.
    assert "The first €44,000 | 20 per cent | the standard rate" in content
    assert "the substitution of “€2,000” for “€1,875”" in content


def test_year_of_assessment_beats_a_bare_year_mention():
    ref = _ref("2024/act/43", "act", short_title="Finance Act 2024")
    _, _, units = _units(FINANCE_ACT_XML, ref)
    usc = units["part_1.chapter_2.sect_2"]
    assert usc.versions[0].valid_from == date(2025, 1, 1)
    assert "The first €12,012 | 0.5 per cent" in usc.versions[0].texts[0].content
    assert "“€27,382” for “€25,760”" in usc.versions[0].texts[0].content


def test_social_welfare_act_reads_per_section_commencement():
    ref = _ref("2024/act/36", "act", short_title="Social Welfare Act 2024")
    _, _, units = _units(SOCIAL_WELFARE_ACT_XML, ref)

    assert units["sect_4"].versions[0].valid_from == date(2025, 1, 6)
    assert units["sect_4"].versions[0].amendment_note["effective_date_basis"] == "comes_into_operation"

    # s. 16 commences on three different days depending on the benefit; the
    # section starts at the earliest, and every stated date is kept.
    staggered = units["sect_16"].versions[0]
    assert staggered.valid_from == date(2024, 12, 26)
    assert staggered.amendment_note == {
        "effective_date_basis": "comes_into_operation_staggered",
        "commencement_dates": ["2024-12-26", "2025-01-02", "2025-01-03"],
    }


def test_schedules_are_ingested_from_backmatter_with_flattened_tables():
    ref = _ref("2024/act/36", "act", short_title="Social Welfare Act 2024")
    _, _, units = _units(SOCIAL_WELFARE_ACT_XML, ref)

    schedule = units["sched_1"]
    assert schedule.unit_type == "schedule"
    assert schedule.citation == "Social Welfare Act 2024, Sch. 1"
    assert schedule.national_id == "2024/act/36/schedule/1"
    content = schedule.versions[0].texts[0].content
    # The repeated "SCHEDULE 1" line is dropped from the heading, and the rate
    # grid is flattened to one quotable row per benefit.
    assert content.startswith("Schedule 1. Social Insurance Benefits (New Rates)")
    assert "State Pension (Contributory) | 289.30" in content


def test_baseline_act_is_loaded_as_structure_not_as_in_force_text():
    ref = _ref("1997/act/39", "act")
    _, instrument, units = _units(TCA_XML, ref)

    # The XML dialect differs: <title> precedes <number>, ids carry the number.
    assert instrument.title == {"en": "Taxes Consolidation Act 1997"}
    assert instrument.metadata["as_enacted_baseline"] is True
    section = units["part_2.sect_15"]
    assert section.citation == "Taxes Consolidation Act 1997, s. 15"
    assert section.metadata["heading"] == "Rate of charge. — [FA91 s2; FA97 s2(1) and (2)]"

    version = section.versions[0]
    # Ireland publishes no consolidation of the TCA, so the as-enacted text must
    # never satisfy `validity @> as_of` inside the EUROMOD window.
    assert version.valid_from == date(1997, 11, 30)
    assert version.valid_to == date(2022, 1, 1)
    assert version.status.value == "unknown"
    assert version.amendment_note == {"effective_date_basis": "as_enacted_baseline"}

    # The TCA writes schedule headings in <pc>, not <p>; treating that as inline
    # would run "SCHEDULE 2" into the title instead of it being dropped.
    schedule = units["sched_2"]
    assert schedule.citation == "Taxes Consolidation Act 1997, Sch. 2"
    assert schedule.versions[0].texts[0].content.startswith(
        "Schedule 2. Machinery for Assessment, Charge and Payment of Tax"
    )


def test_act_index_keeps_fiscal_acts_and_drops_the_decoys():
    ref = _ref("index/2024", "act_index", source_code="IE-OIREACHTAS")
    doc = parse_ie(ACT_INDEX_JSON, ref, _snapshot(ref))

    assert doc.instruments == []
    assert [child["source_id"] for child in doc.metadata["child_refs"]] == ["2024/act/43", "2024/act/36"]
    # Appropriation Act and "Finance (State Guarantees ...) Act" carry no
    # EUROMOD parameter and must not enter the corpus.
    assert doc.metadata["skipped_non_fiscal"] == 2


def test_adapter_expands_index_children_across_hosts():
    ref = _ref("index/2024", "act_index", source_code="IE-OIREACHTAS")
    doc = parse_ie(ACT_INDEX_JSON, ref, _snapshot(ref))
    work = IeAdapter().expand(doc)

    assert len(work) == 2
    first = work[0].ref
    assert first.source_id == "2024/act/43"
    assert first.source_type == "act"
    # Children are fetched from eISB, not from the index's own host.
    assert first.source_code == "IE-EISB"
    assert first.metadata["short_title"] == "Finance Act 2024"
    assert first.metadata["date_signed"] == "2024-11-12"


def test_resolver_covers_the_budget_year_and_the_one_before_it():
    # Ireland's Budget 2025 parameters are enacted by the Finance Act 2024.
    refs = IeResolver().resolve(CitationRef(jurisdiction="IE", citation="2025"), date(2025, 6, 1))
    assert [ref.source_id for ref in refs] == ["index/2024", "index/2025"]
    assert {ref.source_code for ref in refs} == {"IE-OIREACHTAS"}

    from_as_of = IeResolver().resolve(
        CitationRef(jurisdiction="IE", citation="income tax bands"), date(2025, 6, 1)
    )
    assert [ref.source_id for ref in from_as_of] == ["index/2024", "index/2025"]


@pytest.mark.parametrize(
    ("citation", "expected"),
    [
        ("TCA 1997", "1997/act/39"),
        ("Taxes Consolidation Act, 1997", "1997/act/39"),
        ("SWCA 2005", "2005/act/26"),
        ("2024/act/43", "2024/act/43"),
    ],
)
def test_resolver_short_circuits_known_acts_and_explicit_ids(citation, expected):
    refs = IeResolver().resolve(CitationRef(jurisdiction="IE", citation=citation), date(2025, 6, 1))
    assert [ref.source_id for ref in refs] == [expected]
    assert refs[0].source_code == "IE-EISB"


def test_effective_date_falls_back_to_enactment_without_a_stated_date():
    enacted = date(2024, 10, 28)
    effective, basis, stated = _effective_date(
        "This Act may be cited as the Social Welfare Act 2024.", enacted
    )
    assert (effective, basis, stated) == (enacted, "enactment", [])

    effective, basis, _ = _effective_date(
        "This section comes into operation on such day as the Minister may appoint.", enacted
    )
    assert (effective, basis) == (enacted, "enactment")


def test_canary_facts_cover_each_supported_system_year():
    facts = IeAdapter().canary_facts()
    assert [fact.assert_latest_start_gte for fact in facts] == [
        date(2023, 1, 1),
        date(2024, 1, 1),
        date(2025, 1, 1),
    ]
    assert "€44,000" in facts[-1].reason
