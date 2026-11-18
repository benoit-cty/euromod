"""The Law Reform Commission's Revised Acts (markup trimmed from the live page of
the Social Welfare Consolidation Act 2005, updated to 1 October 2026)."""

from datetime import date
from uuid import uuid4

from nomotheca_ingest.core.ir import CitationRef, Snapshot, SourceRef
from nomotheca_ingest.countries.ie.adapter import IeAdapter
from nomotheca_ingest.countries.ie.fetcher import url_for_ref
from nomotheca_ingest.countries.ie.parser import parse_ie

PAGE = """<html><head><title>  Social Welfare Consolidation Act 2005  | Law Reform</title></head><body>
<p>Updated to 1 October 2026</p>
<section class="part" id="PART3"><div class="title"><p>PART 3</p><p>Social Assistance</p></div>
<div class="sect-tab"><img src="/images/bkmrk_sm.svg"><span>Section 142</span></div>
<section class="sect" id="SEC142" data-number="142">
<div class="title"><p>Rates of assistance.</p></div><div class="number">142</div>
<p><b>142.</b>&mdash;(1) The rate of <span class="commentary-reference">F833</span><span class="markup">[</span><span class="change">jobseeker&rsquo;s
   allowance</span><span class="markup">]</span> shall not exceed <span class="page" data-number="130"></span>&euro;20.</p>
<div class="annotations"><div class="f-notes"><div class="f-note"><p class="shouldernote1">F833</p>
<p>Substituted (29.09.2006) by <i>Social Welfare Law Reform and Pensions Act 2006</i> (5/2006), s. 4.</p></div>
<div class="f-note"><p class="shouldernote1">F834</p><p>Inserted by Social Welfare Act 2008, s. 5, not commenced as of date of revision.</p></div>
</div></div></section>
<section class="sect" id="SEC143" data-number="143"><div class="title"><p>Never amended.</p></div>
<div class="number">143</div><p><b>143.</b>&mdash;The age is 66 years.</p></section>
</section>
<section class="schedule" id="SCHED4"><div class="title"><p>SCHEDULE 4</p><p>Rates of Assistance</p></div>
<section class="part" id="SCHED4-PARTI"><div class="title"><p><span class="commentary-reference">F1954</span>PART 1</p><p>RATES</p></div>
<table><tr><td><p>Description of benefit</p></td><td><p>Weekly rate</p></td></tr>
<tr><td><p>3. Disability Allowance:</p></td><td><p>254.00</p></td></tr></table>
<div class="annotations"><div class="f-note"><p class="shouldernote1">F1954</p>
<p>Substituted (31.12.2025 to 7.01.2026) by Social Welfare Act 2025 (19/2025), s. 13(1).</p></div></div>
</section></section>
</body></html>""".encode()


def _parse():
    ref = IeAdapter().resolve(CitationRef(jurisdiction="IE", citation="2005/act/26/revised"), date(2025, 7, 1))[0]
    snapshot = Snapshot(id=uuid4(), source_code=ref.source_code, url=url_for_ref(ref), content_hash="x", raw_content=PAGE)
    return ref, parse_ie(PAGE, ref, snapshot).instruments[0]


def test_a_revised_id_goes_to_the_law_reform_commission():
    ref, instrument = _parse()
    assert ref.source_code == "IE-LRC" == IeAdapter().source_code_for("2005/act/26/revised")
    assert url_for_ref(ref) == "https://revisedacts.lawreform.ie/eli/2005/act/26/revised/en/html"
    assert IeAdapter().source_code_for("2024/act/36") == "IE-EISB"
    # The title differs from the as-enacted act's, so a lookup by name finds one act.
    assert instrument.title == {"en": "Social Welfare Consolidation Act 2005 (Revised)"}


def test_the_text_is_the_law_without_the_editorial_marks():
    units = {u.citation: u for u in _parse()[1].units if u.versions}
    text = units["Social Welfare Consolidation Act 2005 (Revised), s. 142"].versions[0].texts[0].content
    assert "The rate of jobseeker’s allowance shall not exceed €20." in text
    assert "F833" not in text and "[" not in text and "Substituted" not in text
    table = units["Social Welfare Consolidation Act 2005 (Revised), Sch. 4, Part 1"].versions[0].texts[0].content
    assert "3. Disability Allowance: | 254.00" in table


def test_a_section_starts_at_its_latest_commenced_amendment():
    units = {u.citation.rsplit(", ", 1)[-1]: u.versions[0] for u in _parse()[1].units if u.versions}
    assert units["s. 142"].valid_from == date(2006, 9, 29)  # the uncommenced note dates nothing
    assert units["s. 142"].amendment_note["uncommenced_amendments"] == 1
    assert units["s. 143"].valid_from == date(2005, 12, 31)  # never amended: the act's year
    # A staggered commencement ends on its last date: the 2026 rates are not the 2025 ones.
    assert units["Part 1"].valid_from == date(2026, 1, 7)
