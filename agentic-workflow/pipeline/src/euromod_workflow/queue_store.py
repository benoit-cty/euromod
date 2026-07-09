"""File-based review queue + decision log.

Layout under WORKFLOW_DATA_DIR (default agentic-workflow/data):
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


def item_id(country: str, model_target: str, as_of: date) -> str:
    """Stable id so re-runs of the same (parameter, as_of) overwrite, not duplicate."""
    return f"{country.lower()}_{slugify(model_target)}_{as_of.isoformat()}"


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
