"""Compare our normalized CSV outputs against H2N4 baseline CSV exports."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any


KEY_FIELDS = ("section", "metric", "position")
EXACT_NUMERIC_FIELDS = ("numerator", "denominator", "hands", "cases", "opportunities")
TOLERANT_NUMERIC_FIELDS = ("value", "percent", "total_profit_bb", "bb_per_100")
NUMERIC_FIELDS = EXACT_NUMERIC_FIELDS + TOLERANT_NUMERIC_FIELDS
REQUIRED_FIELDS = KEY_FIELDS + NUMERIC_FIELDS

POSITION_KEY_FIELDS = ("position",)
POSITION_EXACT_FIELDS = ("hands",)
POSITION_TOLERANT_FIELDS = ("amount_won", "amount_won_bb", "bb_per_100")

SPOT_FILTER_KEY_FIELDS = (
    "filter_id",
    "street",
    "action_line",
    "hero_ip_oop",
    "player_count_context",
    "facing_bet_size_bucket",
)
SPOT_FILTER_EXACT_FIELDS = ("cases", "opportunities")
SPOT_FILTER_TOLERANT_FIELDS = ("amount_won", "amount_won_bb")

ACTION_PROFIT_KEY_FIELDS = ("filter_id", "street", "hero_action", "hand_category")
ACTION_PROFIT_EXACT_FIELDS = (
    "cases",
    "opportunities",
    "next_villain_fold_count",
    "next_villain_call_count",
    "next_villain_raise_count",
)
ACTION_PROFIT_TOLERANT_FIELDS = (
    "total_action_profit_bb",
    "avg_action_profit_bb",
    "amount_won",
    "amount_won_bb",
)


@dataclass(frozen=True)
class FieldMismatch:
    key: tuple[str, ...]
    field: str
    ours: str | None
    baseline: str | None
    difference: float | None


def compare_report_csv(
    ours_path: str | Path,
    baseline_path: str | Path,
    *,
    tolerance: float = 0.01,
) -> dict[str, Any]:
    """Compare normalized report CSV files and return a structured parity result."""

    return _compare_csv(
        ours_path=ours_path,
        baseline_path=baseline_path,
        key_fields=KEY_FIELDS,
        exact_fields=EXACT_NUMERIC_FIELDS,
        tolerant_fields=TOLERANT_NUMERIC_FIELDS,
        required_fields=REQUIRED_FIELDS,
        tolerance=tolerance,
        comparison_type="basic_reports",
        exact_value_metrics={"hands"},
    )


def compare_position_results_csv(
    ours_path: str | Path,
    baseline_path: str | Path,
    *,
    tolerance: float = 0.01,
) -> dict[str, Any]:
    """Compare normalized position-results CSV files."""

    return _compare_csv(
        ours_path=ours_path,
        baseline_path=baseline_path,
        key_fields=POSITION_KEY_FIELDS,
        exact_fields=POSITION_EXACT_FIELDS,
        tolerant_fields=POSITION_TOLERANT_FIELDS,
        required_fields=POSITION_KEY_FIELDS + POSITION_EXACT_FIELDS + POSITION_TOLERANT_FIELDS,
        tolerance=tolerance,
        comparison_type="position_results",
    )


def compare_spot_filter_csv(
    ours_path: str | Path,
    baseline_path: str | Path,
    *,
    tolerance: float = 0.01,
) -> dict[str, Any]:
    """Compare normalized spot-filter CSV files."""

    return _compare_csv(
        ours_path=ours_path,
        baseline_path=baseline_path,
        key_fields=SPOT_FILTER_KEY_FIELDS,
        exact_fields=SPOT_FILTER_EXACT_FIELDS,
        tolerant_fields=SPOT_FILTER_TOLERANT_FIELDS,
        required_fields=SPOT_FILTER_KEY_FIELDS + SPOT_FILTER_EXACT_FIELDS + SPOT_FILTER_TOLERANT_FIELDS,
        tolerance=tolerance,
        comparison_type="spot_filter",
    )


def compare_action_profit_csv(
    ours_path: str | Path,
    baseline_path: str | Path,
    *,
    tolerance: float = 0.01,
) -> dict[str, Any]:
    """Compare normalized Action Profit CSV files."""

    return _compare_csv(
        ours_path=ours_path,
        baseline_path=baseline_path,
        key_fields=ACTION_PROFIT_KEY_FIELDS,
        exact_fields=ACTION_PROFIT_EXACT_FIELDS,
        tolerant_fields=ACTION_PROFIT_TOLERANT_FIELDS,
        required_fields=ACTION_PROFIT_KEY_FIELDS + ACTION_PROFIT_EXACT_FIELDS + ACTION_PROFIT_TOLERANT_FIELDS,
        tolerance=tolerance,
        comparison_type="action_profit",
    )


def _compare_csv(
    *,
    ours_path: str | Path,
    baseline_path: str | Path,
    key_fields: tuple[str, ...],
    exact_fields: tuple[str, ...],
    tolerant_fields: tuple[str, ...],
    required_fields: tuple[str, ...],
    tolerance: float,
    comparison_type: str,
    exact_value_metrics: set[str] | None = None,
) -> dict[str, Any]:
    ours = _load_rows(ours_path, key_fields=key_fields, required_fields=required_fields)
    baseline = _load_rows(baseline_path, key_fields=key_fields, required_fields=required_fields)
    keys = sorted(set(ours) | set(baseline))
    missing_in_ours = [key for key in keys if key not in ours]
    missing_in_baseline = [key for key in keys if key not in baseline]
    mismatches: list[FieldMismatch] = []
    numeric_fields = exact_fields + tolerant_fields

    for key in keys:
        if key not in ours or key not in baseline:
            continue
        for field in numeric_fields:
            ours_value = _empty_to_none(ours[key].get(field))
            baseline_value = _empty_to_none(baseline[key].get(field))
            if ours_value is None and baseline_value is None:
                continue
            if _numeric_equal(
                ours_value,
                baseline_value,
                tolerance=0
                if _requires_exact_match(
                    key,
                    field,
                    exact_fields=exact_fields,
                    exact_value_metrics=exact_value_metrics or set(),
                )
                else tolerance,
            ):
                continue
            mismatches.append(
                FieldMismatch(
                    key=key,
                    field=field,
                    ours=ours_value,
                    baseline=baseline_value,
                    difference=_difference(ours_value, baseline_value),
                )
            )

    return {
        "status": "pass" if not missing_in_ours and not missing_in_baseline and not mismatches else "fail",
        "comparison_type": comparison_type,
        "compared_rows": len([key for key in keys if key in ours and key in baseline]),
        "missing_in_ours": [_key_dict(key, key_fields) for key in missing_in_ours],
        "missing_in_baseline": [_key_dict(key, key_fields) for key in missing_in_baseline],
        "mismatches": [_mismatch_dict(mismatch, key_fields) for mismatch in mismatches],
    }


def _load_rows(
    path: str | Path,
    *,
    key_fields: tuple[str, ...],
    required_fields: tuple[str, ...],
) -> dict[tuple[str, ...], dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing_fields = [field for field in required_fields if field not in (reader.fieldnames or [])]
        if missing_fields:
            raise ValueError(f"{path} is missing required columns: {', '.join(missing_fields)}")
        rows = list(reader)

    keyed: dict[tuple[str, ...], dict[str, str]] = {}
    duplicates = []
    for row in rows:
        key = _key(row, key_fields)
        if key in keyed:
            duplicates.append(key)
        keyed[key] = row
    if duplicates:
        duplicate_text = ", ".join("/".join(key) for key in duplicates)
        raise ValueError(f"{path} has duplicate comparison keys: {duplicate_text}")
    return keyed


def _key(row: dict[str, str], key_fields: tuple[str, ...]) -> tuple[str, ...]:
    return tuple((row.get(field) or "").strip() for field in key_fields)


def _key_dict(key: tuple[str, ...], key_fields: tuple[str, ...]) -> dict[str, str]:
    return dict(zip(key_fields, key))


def _mismatch_dict(mismatch: FieldMismatch, key_fields: tuple[str, ...]) -> dict[str, Any]:
    return {
        **_key_dict(mismatch.key, key_fields),
        "field": mismatch.field,
        "ours": mismatch.ours,
        "baseline": mismatch.baseline,
        "difference": mismatch.difference,
    }


def _empty_to_none(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped if stripped else None


def _numeric_equal(ours: str | None, baseline: str | None, *, tolerance: float) -> bool:
    if ours is None or baseline is None:
        return ours == baseline
    try:
        return abs(float(ours) - float(baseline)) <= tolerance
    except ValueError:
        return ours == baseline


def _difference(ours: str | None, baseline: str | None) -> float | None:
    if ours is None or baseline is None:
        return None
    try:
        return round(float(ours) - float(baseline), 6)
    except ValueError:
        return None


def _requires_exact_match(
    key: tuple[str, ...],
    field: str,
    *,
    exact_fields: tuple[str, ...],
    exact_value_metrics: set[str],
) -> bool:
    metric = key[1] if len(key) > 1 else ""
    return field in exact_fields or (field == "value" and metric in exact_value_metrics)
