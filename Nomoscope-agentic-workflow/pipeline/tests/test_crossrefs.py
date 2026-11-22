"""Corpus lookups: FTS terms, article tokens, code and same-act references."""

from __future__ import annotations

from datetime import date

from nomoscope_workflow.corpus import _fts_query
from nomoscope_workflow.crossrefs import _code_refs, _same_act_citing, _same_act_refs
from nomoscope_workflow.locate import _article_tokens


def test_fts_query_ors_distinct_terms():
    q = _fts_query("Taux de la tranche 1 taux marginal de l'impôt")
    assert " OR " in q
    terms = q.split(" OR ")
    assert len(terms) == len(set(terms))  # deduplicated
    assert "taux" in terms and "marginal" in terms
    assert "or" not in terms  # websearch operator keyword never emitted as a term
    assert _fts_query("") == ""  # degenerate input falls through unchanged


def test_article_tokens_follow_each_country_idiom():
    assert _article_tokens("article D. 633-3 du code de la sécurité sociale") == ["D633-3"]
    assert _article_tokens("artículo 66.2 de la Ley 35/2006") == ["66.2"]
    assert _article_tokens("de tabel in artikel 2.10, eerste lid, van de Wet IB 2001") == ["2.10"]
    assert _article_tokens("Finance Act 2024, section amending section 531AN of the TCA 1997") == ["531AN"]
    assert _article_tokens("section 461 of the Taxes Consolidation Act 1997") == ["461"]
    assert _article_tokens("VSDĮ 10 straipsnio 1 dalis") == ["10"]
    assert _article_tokens("art. L. 241-3 du CSS et l'article 4 bis") == ["L241-3", "4 bis"]
    assert _article_tokens("l'arrêté fixant le plafond de la sécurité sociale pour 2025") == []


def test_an_article_number_belongs_to_the_code_named_after_it():
    codes = {
        "css": "code de la sécurité sociale",
        "cgi": "code général des impôts",
        "cgi3": "code général des impôts, annexe iii",
    }
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


def test_a_list_of_articles_takes_the_code_named_at_its_end():
    codes = {"css": "code de la sécurité sociale"}
    text = (
        "Textes de référence - Articles L. 381-1, L. 545-1, R. 522-2, R. 522-4, R. 531-1, "
        "R. 543- 5, R. 755 -2, D. 521- 1, D. 521-2 et D. 521-3 du code de la sécurité sociale"
    )
    refs = _code_refs(text, None, codes)
    assert ("css", "R522-2") in refs and ("css", "L381-1") in refs
    # prose between the number and the code: not a list, no reference
    assert (
        _code_refs("l'article R. 522-2 dont il est question plus loin dans le code de la sécurité sociale", None, codes)
        == []
    )


def test_an_article_naming_another_of_its_own_act_is_followed():
    # Décret n° 2025-1212 art. 2 states the amount, art. 1 whom it is for.
    assert _same_act_refs("Le montant de l'aide mentionnée à l'article 1 er est égal à 152,45 euros.") == ["1"]
    assert _same_act_refs("l'article 2 du présent décret") == ["2"]
    assert _same_act_refs("au titre de l'article 3 de la loi n° 2008-1249") == []
    assert _same_act_refs("l'article 197 du code général des impôts") == []
    assert _same_act_refs("l'article L. 262-2 du code de l'action sociale") == []


def test_an_agreement_article_brings_the_nearest_article_that_names_it():
    # ANI AGIRC-ARRCO art. 36 «… appliqué aux taux visés à l'article 35» —
    # art. 35 retrieved, art. 36 not, the schedules not_found (7 Nov batch).

    ani = "Accord national interprofessionnel du 17 novembre 2017, art. "

    class _Conn:
        def cursor(self, row_factory=None):
            return self

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def execute(self, sql, params):
            return self

        def fetchall(self):
            def hit(n, content):
                return {
                    "ord": 1,
                    "chunk_id": f"c{n}",
                    "citation": f"{ani}{n}",
                    "context_header": "",
                    "content": content,
                    "lang": "fr",
                    "validity": "[2019-01-01,)",
                    "version_status": "in_force",
                    "source_trust_class": "evidence",
                    "score": 0.0,
                }

            return [
                hit(13, "les taux fixés à l'article 35 et à l'article 36"),
                hit(49, "selon l'article 35"),
                hit(36, "Un pourcentage d'appel, fixé à 127 %, est appliqué aux taux visés à l'article 35."),
                hit(60, "l'article 35 de la loi n° 2020-1 ne s'applique pas"),
            ]

    rows = [
        {
            "chunk_id": "c35",
            "citation": f"{ani}35",
            "instrument_id": "i",
            "valid_from": date(2019, 1, 1),
            "content": "taux de calcul des points",
        }
    ]
    found = _same_act_citing(_Conn(), "fr", rows, {"c35"})
    assert [h.citation.rsplit(" ", 1)[-1] for h in found] == ["36", "49"]
