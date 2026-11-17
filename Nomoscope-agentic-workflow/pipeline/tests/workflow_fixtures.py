"""Records, hits and drafts the workflow tests build on (not a test module)."""

from __future__ import annotations

from datetime import date

from nomoscope_workflow.schema import (
    Operand,
    ParameterInformation,
    ParameterRecord,
    ParameterValue,
    ProposalDraft,
    RetrievalHit,
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
