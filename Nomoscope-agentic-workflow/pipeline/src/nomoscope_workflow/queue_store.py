"""File-based review queue + decision log.

Layout under WORKFLOW_DATA_DIR (default Nomoscope-agentic-workflow/data):
  parameters/   input parameter records (Activity 1 JSON, git-versioned)
  queue/        one JSON per ReviewItem — what the validation UI reads/writes
  decisions.jsonl  append-only audit log of every reviewer decision
  export/       accepted records in the Activity 1 format (write-back is export-first)

The Tauri UI operates on the same files (see ui/src-tauri/src/store.rs); this
module is the Python side used by the pipeline and the CLI.
"""

from __future__ import annotations

import json
import re
from datetime import date, datetime, timezone
from pathlib import Path

from .schema import ItemStatus, ParameterRecord, ReviewItem


def slugify(text: str) -> str:
    """Filesystem-safe slug of a model_target path."""
    return re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_").lower()


def item_id(country: str, model_target: str, system_year: int) -> str:
    """Stable id so re-runs of the same (parameter, system year) overwrite, not duplicate.

    Keyed on the system year, not the anchor date: one run verifies one EUROMOD
    system year, and re-running it on another day (or with a shifted anchor, as
    income_year parameters do) is the same review, not a second one.
    """
    return f"{country.lower()}_{slugify(model_target)}_{system_year}"


def queue_dir(data_dir: Path) -> Path:
    return data_dir / "queue"


def load_record(path: Path) -> ParameterRecord:
    """Load an Activity 1 parameter record; tolerates //-comment lines (.jsonc)."""
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"^\s*//.*$", "", text, flags=re.MULTILINE)
    return ParameterRecord.model_validate_json(text)


def write_item(item: ReviewItem, data_dir: Path, force: bool = False) -> bool:
    """Write a queue item; never clobber an already-reviewed item unless forced."""
    path = queue_dir(data_dir) / f"{item.id}.json"
    if path.exists() and not force:
        existing = json.loads(path.read_text(encoding="utf-8"))
        if existing.get("status") != ItemStatus.PENDING:
            return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(item.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return True


def load_items(data_dir: Path) -> list[ReviewItem]:
    """All queue items, newest first."""
    folder = queue_dir(data_dir)
    if not folder.is_dir():
        return []
    items = [
        ReviewItem.model_validate_json(p.read_text(encoding="utf-8"))
        for p in sorted(folder.glob("*.json"))
    ]
    return sorted(items, key=lambda i: i.created_at, reverse=True)


def migrate_item_ids(data_dir: Path, apply: bool = False) -> list[dict]:
    """Re-key queue files from the old `<country>_<target>_<as_of>` id to the
    system-year id, collapsing the duplicates that produced.

    Items written before `--year` existed carry `system_year: null`; their anchor
    date was the run date, so the year is taken from `as_of`. When several runs
    land on the same system year, the decided one wins over a pending one and the
    newest wins among equals; the losers are moved to `queue_superseded/` rather
    than deleted, because they are the audit trail of what was proposed when.

    Returns one plan entry per file; nothing is written unless `apply` is set.
    """
    folder = queue_dir(data_dir)
    if not folder.is_dir():
        return []

    candidates: dict[str, list[tuple[Path, dict, str]]] = {}
    plan: list[dict] = []
    for path in sorted(folder.glob("*.json")):
        item = json.loads(path.read_text(encoding="utf-8"))
        year = item.get("system_year") or int(str(item.get("as_of", ""))[:4] or 0)
        if not (year and item.get("country") and item.get("model_target")):
            plan.append({"path": path, "action": "skip", "reason": "no country/target/year"})
            continue
        new_id = item_id(item["country"], item["model_target"], year)
        candidates.setdefault(new_id, []).append((path, item, str(year)))

    for new_id, runs in sorted(candidates.items()):
        # decided beats pending, then newest created_at; ties broken by filename
        runs.sort(
            key=lambda r: (
                r[1].get("status", "pending") != "pending",
                str(r[1].get("created_at", "")),
                r[0].name,
            ),
            reverse=True,
        )
        (winner_path, winner, year), losers = runs[0], runs[1:]
        target = folder / f"{new_id}.json"
        if target.exists() and target not in {p for p, _, _ in runs}:
            # a file already owns the canonical name but holds another parameter
            plan.append({"path": winner_path, "action": "skip", "reason": f"{target.name} taken"})
            continue
        plan.append(
            {
                "path": winner_path,
                "action": "keep" if winner_path == target else "rename",
                "new_id": new_id,
                "old_id": winner.get("id"),
                "status": winner.get("status"),
                "superseded": len(losers),
            }
        )
        if apply:
            winner["id"] = new_id
            winner["system_year"] = int(year)
            if winner_path != target:
                winner_path.unlink()
            target.write_text(
                json.dumps(winner, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
        for loser_path, loser, _ in losers:
            plan.append(
                {
                    "path": loser_path,
                    "action": "supersede",
                    "new_id": new_id,
                    "old_id": loser.get("id"),
                    "status": loser.get("status"),
                }
            )
            if apply:
                archive = data_dir / "queue_superseded"
                archive.mkdir(parents=True, exist_ok=True)
                loser_path.replace(archive / loser_path.name)
    return plan


def append_decision(data_dir: Path, entry: dict) -> None:
    """Append one reviewer decision to the audit log (this log is training data)."""
    entry.setdefault("logged_at", datetime.now(timezone.utc).isoformat())
    path = data_dir / "decisions.jsonl"
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def export_accepted(data_dir: Path, out_dir: Path | None = None) -> list[Path]:
    """Write accepted/edited items' full records for the modelling team."""
    out = out_dir or data_dir / "export"
    out.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for item in load_items(data_dir):
        if item.status in (ItemStatus.ACCEPTED, ItemStatus.EDITED) and item.proposed_record:
            path = out / f"{item.id}.json"
            path.write_text(
                json.dumps(item.proposed_record.model_dump(mode="json"), ensure_ascii=False, indent=2)
                + "\n",
                encoding="utf-8",
            )
            written.append(path)
    return written
