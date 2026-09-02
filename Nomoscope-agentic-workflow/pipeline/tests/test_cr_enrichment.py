"""Tests for Country Report query enrichment (frame-step helpers)."""

from __future__ import annotations

from nomoscope_workflow.retrieval import cr_enrichment_terms, euromod_ident_tokens
from nomoscope_workflow.schema import RetrievalHit


def _hit(citation: str) -> RetrievalHit:
    return RetrievalHit(chunk_id="00000000-0000-0000-0000-000000000000", citation=citation, method="country_report")


def test_ident_tokens_split_policy_and_constant() -> None:
    """Policy stem and constant parts come out; scheme/country/def_const noise does not."""
    tokens = euromod_ident_tokens("euromod://FR/tin_fr/def_const/$tinrt_cdhr")
    assert tokens == ["tin", "tinrt", "cdhr"]


def test_ident_tokens_drop_numeric_and_short() -> None:
    tokens = euromod_ident_tokens("euromod://FR/bch00_fr/def_const/$bch_amt2024")
    assert "bch00" in tokens and "bch" in tokens
    assert "2024" not in tokens and "fr" not in tokens


def test_enrichment_requires_ident_match_in_heading() -> None:
    """Generic high-rank sections must not contribute terms."""
    hits = [
        _hit("CR FR Y16, §Income test"),
        _hit('CR FR Y16, §5.4 General Social contribution — **tscxc_s** ("Contribution Sociale Généralisée", CSG)'),
        _hit('CR FR Y16, §Differential contribution on high income — tinto01_s ("Contribution différentielle sur les hauts revenus", CDHR) [pp. 110-111]'),
    ]
    terms = cr_enrichment_terms(hits, ["tin", "tinrt", "cdhr"], "CDHR rate")
    assert "différentielle" in terms and "revenus" in terms
    # nothing harvested from the CSG or 'Income test' headings
    assert "Généralisée" not in terms and "Sociale" not in terms
    # code-like and page-ref tokens never leak into the query
    assert all("_" not in t and not any(c.isdigit() for c in t) for t in terms)


def test_enrichment_skips_words_already_in_query() -> None:
    hits = [_hit("CR FR Y16, §Personal income tax — tin_s — (Impôt sur le Revenu, IRPP)")]
    terms = cr_enrichment_terms(hits, ["tin"], "top marginal income tax rate")
    assert "income" not in [t.lower() for t in terms]
    assert "Impôt" in terms and "IRPP" in terms


def test_enrichment_caps_terms() -> None:
    long_heading = "CR FR Y16, §" + " ".join(f"word{chr(97 + i)}" for i in range(30)) + " tin_s"
    terms = cr_enrichment_terms([_hit(long_heading)], ["tin"], "")
    assert len(terms) <= 12


def test_no_ident_tokens_means_no_enrichment() -> None:
    hits = [_hit("CR FR Y16, §Personal income tax — tin_s")]
    assert cr_enrichment_terms(hits, [], "query") == []
