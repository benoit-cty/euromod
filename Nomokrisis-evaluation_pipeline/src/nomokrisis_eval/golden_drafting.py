"""What every golden-case drafter shares, whatever its source of ground truth.

Three drafters write rows into eval.golden_cases — `openfisca_golden` (ground
truth read from the OpenFisca corpus), `curated_golden` (ground truth written
by hand into a `curated` selection) and `build_dataset` (an LLM reading a
trusted document). They differ in where the expected value comes from; the
rest is here, once:

- the case id, which a rebuild must reproduce exactly — a drifted id leaves the
  previous draft behind as a stale row (`golden_case_id`, `entry_case_id`);
"""

from __future__ import annotations

from datetime import date

from nomoscope_workflow import paramdb
from nomoscope_workflow.queue_store import slugify

#: `parameter_target` prefix of a bracket schedule assembled from
#: params.parameter_groups (`group:<group_id>`).
GROUP_PREFIX = "group:"


def case_slug(model_target: str, country: str) -> str:
    """euromod://FR/tinkt_fr/def_const/$tin_upthres1 -> 'tinkt_tin_upthres1'.

    The country prefixes the case id already and `def_const` is the only
    function in the export, so both are noise in a case id.
    """
    parts = paramdb.parse_model_target(model_target)
    policy = (parts["policy"] or "").removesuffix(f"_{country.lower()}")
    name = (parts["name"] or model_target).lstrip("$")
    return slugify(f"{policy}_{name}") if policy else slugify(name)


def golden_case_id(country: str, as_of: date, target: str, slug: str | None = None) -> str:
    """The id of the golden case for one parameter on one date — the one rule.

    `target` is what the case tests: a `euromod://…` model target, or a bracket
    schedule's group id (bare or as `group:<group_id>`). `slug`, when the
    selection entry states one (`id`), wins. A group is slugged from its group
    id, never from the `euromod://<cc>/<policy>/group/<name>` target its
    assembled record carries: the id must be computable from the selection
    entry alone, before (or without) loading the record, or a draft that stops
    building could never be found again to be retired.
    """
    if not slug:
        bare = target.removeprefix(GROUP_PREFIX)
        slug = case_slug(bare, country) if bare.startswith("euromod://") else slugify(bare)
    return f"{country.lower()}_{slug}_{as_of.isoformat()}"


def entry_case_id(entry: dict, as_of: date, country: str) -> str | None:
    """The id a selection entry's case carries (or would carry), from the entry alone.

    None for an entry that names no parameter at all.
    """
    target = entry.get("group_id") or entry.get("model_target")
    if not target:
        return None
    if entry.get("group_id"):
        target = f"{GROUP_PREFIX}{target}"
    return golden_case_id(country, as_of, target, entry.get("id"))
