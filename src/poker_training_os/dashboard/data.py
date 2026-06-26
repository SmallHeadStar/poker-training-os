"""Load session artifacts for the Streamlit dashboard."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


REQUIRED_DASHBOARD_FILES = {
    "session_review": "session_review.md",
    "session_summary": "session_summary.json",
    "basic_reports": "basic_reports.csv",
    "loss_map": "loss_map.csv",
    "issue_cards": "issue_cards.json",
    "review_queue": "review_queue.csv",
    "gto_study_cards": "gto_study_cards.md",
    "training_cycle_update": "training_cycle_update.json",
}


def load_session_dashboard(artifact_dir: str | Path) -> dict[str, Any]:
    root = Path(artifact_dir)
    missing = [filename for filename in REQUIRED_DASHBOARD_FILES.values() if not (root / filename).exists()]
    return {
        "missing_files": missing,
        "session_review": _read_text(root / "session_review.md"),
        "session_summary": _read_json(root / "session_summary.json", default={}),
        "basic_reports": _read_csv(root / "basic_reports.csv"),
        "loss_map": _read_csv(root / "loss_map.csv"),
        "issue_cards": _read_json(root / "issue_cards.json", default=[]),
        "review_queue": _read_csv(root / "review_queue.csv"),
        "gto_study_cards": _read_text(root / "gto_study_cards.md"),
        "training_cycle_update": _read_json(root / "training_cycle_update.json", default={}),
    }


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _read_json(path: Path, default: Any) -> Any:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))

