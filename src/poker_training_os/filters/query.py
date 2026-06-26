"""Lightweight structured filter layer for spot feature rows."""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Iterable


def filter_rows(rows: Iterable[dict[str, Any]], **filters: Any) -> list[dict[str, Any]]:
    """Filter rows by exact value or by a collection of allowed values."""

    return [row for row in rows if _matches(row, filters)]


def group_rows(rows: Iterable[dict[str, Any]], group_by: list[str]) -> list[dict[str, Any]]:
    """Group spot rows and aggregate sample count plus observed hand result."""

    grouped: dict[tuple[Any, ...], dict[str, Any]] = defaultdict(
        lambda: {"sample_count": 0, "total_hand_net_bb": 0.0}
    )
    for row in rows:
        key = tuple(row.get(field) for field in group_by)
        bucket = grouped[key]
        for field, value in zip(group_by, key):
            bucket[field] = value
        bucket["sample_count"] += 1
        bucket["total_hand_net_bb"] += float(row.get("hand_net_bb") or 0)

    output = []
    for bucket in grouped.values():
        total = round(bucket["total_hand_net_bb"], 4)
        count = bucket["sample_count"]
        output.append(
            {
                **{field: bucket[field] for field in group_by},
                "sample_count": count,
                "total_hand_net_bb": _clean_number(total),
                "avg_hand_net_bb": _clean_number(round(total / count, 4)) if count else None,
            }
        )
    return sorted(output, key=lambda row: tuple(str(row.get(field)) for field in group_by))


def _matches(row: dict[str, Any], filters: dict[str, Any]) -> bool:
    for field, expected in filters.items():
        actual = row.get(field)
        if isinstance(expected, (set, tuple, list)):
            if actual not in expected:
                return False
        elif actual != expected:
            return False
    return True


def _clean_number(value: float) -> int | float:
    return int(value) if value == int(value) else value

