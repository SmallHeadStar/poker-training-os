"""Validate the structure of an H2N4 baseline evidence package."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from poker_training_os.validation.h2n4_parity import REQUIRED_FIELDS as BASIC_REPORT_FIELDS


MANIFEST_FILENAME = "h2n4_baseline_manifest.json"

REQUIRED_MANIFEST_FIELDS = (
    "h2n4_version",
    "export_date",
    "fixture_id",
    "source_hand_history_files",
    "hero_aliases",
    "game_type",
    "stake",
    "currency",
    "timezone",
    "bb_conversion_rule",
    "includes_rake",
    "includes_all_in_ev",
    "raw_label_map",
    "notes",
)

BASELINE_SCHEMAS: dict[str, tuple[str, ...]] = {
    "h2n4_basic_reports_baseline.csv": BASIC_REPORT_FIELDS,
    "h2n4_position_results_baseline.csv": (
        "position",
        "hands",
        "amount_won",
        "amount_won_bb",
        "bb_per_100",
        "h2n_raw_label",
    ),
    "h2n4_spot_filter_baseline.csv": (
        "filter_id",
        "filter_definition",
        "street",
        "action_line",
        "hero_ip_oop",
        "player_count_context",
        "facing_bet_size_bucket",
        "cases",
        "opportunities",
        "amount_won",
        "amount_won_bb",
        "h2n_raw_label",
    ),
    "h2n4_action_profit_baseline.csv": (
        "filter_id",
        "filter_definition",
        "street",
        "hero_action",
        "hand_category",
        "cases",
        "opportunities",
        "total_action_profit_bb",
        "avg_action_profit_bb",
        "amount_won",
        "amount_won_bb",
        "next_villain_fold_count",
        "next_villain_call_count",
        "next_villain_raise_count",
        "h2n_raw_label",
    ),
}


def validate_h2n4_baseline_package(package_dir: str | Path) -> dict[str, Any]:
    """Validate required metadata and CSV schemas for an H2N4 baseline package."""

    root = Path(package_dir)
    manifest_result = _validate_manifest(root / MANIFEST_FILENAME)
    artifact_results = {
        filename: _validate_csv_schema(root / filename, fields)
        for filename, fields in BASELINE_SCHEMAS.items()
    }
    failed = manifest_result["status"] != "pass" or any(
        result["status"] != "pass" for result in artifact_results.values()
    )
    return {
        "status": "fail" if failed else "pass",
        "package_dir": str(root),
        "manifest": manifest_result,
        "artifacts": artifact_results,
        "parity_note": "schema_valid_only_not_h2n4_parity",
    }


def _validate_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "status": "fail",
            "path": str(path),
            "missing": True,
            "missing_fields": list(REQUIRED_MANIFEST_FIELDS),
        }
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {
            "status": "fail",
            "path": str(path),
            "missing": False,
            "error": f"invalid_json: {exc.msg}",
            "missing_fields": [],
        }
    missing_fields = [field for field in REQUIRED_MANIFEST_FIELDS if _is_missing(payload.get(field))]
    return {
        "status": "pass" if not missing_fields else "fail",
        "path": str(path),
        "missing": False,
        "missing_fields": missing_fields,
    }


def _validate_csv_schema(path: Path, required_fields: tuple[str, ...]) -> dict[str, Any]:
    if not path.exists():
        return {
            "status": "fail",
            "path": str(path),
            "missing": True,
            "missing_columns": list(required_fields),
        }
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
    missing_columns = [field for field in required_fields if field not in fieldnames]
    return {
        "status": "pass" if not missing_columns else "fail",
        "path": str(path),
        "missing": False,
        "missing_columns": missing_columns,
    }


def _is_missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, dict)):
        return len(value) == 0
    return False

