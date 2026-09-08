"""Region key and jurisdiction scope (ADR 0003)."""

import pytest

from nomoscope_workflow import retrieval
from nomoscope_workflow.regions import region_key


@pytest.mark.parametrize(
    ("target", "expected"),
    [
        ("euromod://ES/bsarg_es/def_const/$bsarg_rg24_basic_amt", "ES24"),
        ("euromod://ES/bchrg_es/def_const/$bchrg_reg24_lim1", "ES24"),
        ("euromod://ES/tin_cons_es/def_const/$tin_depallrg30_amt1", "ES30"),
        ("euromod://ES/tin_cons_es/def_const/$tin_rg11_upthres1", "ES11"),
        ("euromod://ES/poanc_es/def_const/$poanc_rg70_amt2", "ES70"),
        ("euromod://ES/bsarg_es/def_const/$bsarg_rg63_basic_amt", "ES63"),
        # national parameters: no token, or digits that are not a region
        ("euromod://ES/tin_cons_es/def_const/$tin_perall_amt1", None),
        ("euromod://ES/ConstDef_es/def_const/$SMI2", None),
        ("euromod://ES/tin_cons_es/def_const/$tin_rg99_rate1", None),
        ("euromod://ES/x_es/def_const/$marg10_rate", None),
        # countries without a regional layer never get one, whatever the name
        ("euromod://FR/tin_fr/def_const/$tinrg24_amt", None),
    ],
)
def test_region_key_reads_the_nuts2_code_off_the_constant_name(target, expected):
    country = target.split("/")[2]
    assert region_key(country, target) == expected


def test_scope_codes_accepts_a_country_or_a_scope_list():
    assert retrieval.scope_codes("FR") == ["FR"]
    assert retrieval.scope_codes(["ES", "ES-AR"]) == ["ES", "ES-AR"]
    with pytest.raises(ValueError):
        retrieval.scope_codes([])


def test_the_live_version_cte_filters_on_the_scope_not_on_one_country():
    assert "j.code = ANY(%(jurisdictions)s::text[])" in retrieval._LIVE_VERSION_CTE
    assert "%(country)s" not in retrieval._LIVE_VERSION_CTE
    # the Country Report search stays country-wide: the CR is filed under the
    # country and describes regional parameters too
    assert "j.code = %(country)s" in retrieval._CR_SEARCH_SQL
