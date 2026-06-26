"""Mine repeated losing spots from structured spot features."""

from __future__ import annotations

from collections import defaultdict
from typing import Any


DEFAULT_SPOT_DIMENSIONS: dict[str, list[str]] = {
    "top_loss_positions": ["hero_position"],
    "top_loss_pot_types": ["pot_type"],
    "top_loss_preflop_lines": ["preflop_line"],
    "top_loss_action_lines": ["action_line_before"],
    "top_loss_board_families": ["board_family"],
    "top_loss_combined_spots": ["hero_position", "pot_type", "preflop_line", "board_family", "hero_decision"],
}


def mine_loss_spots(rows: list[dict[str, Any]], limit: int = 10) -> dict[str, list[dict[str, Any]]]:
    """Mine top losing groups from spot feature rows."""

    return {
        source: _mine_dimension(rows, fields, source=source, limit=limit)
        for source, fields in DEFAULT_SPOT_DIMENSIONS.items()
    }


def _mine_dimension(
    rows: list[dict[str, Any]],
    fields: list[str],
    *,
    source: str,
    limit: int,
) -> list[dict[str, Any]]:
    grouped: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        key = tuple(row.get(field) for field in fields)
        grouped[key].append(row)

    mined = []
    for key, group_rows in grouped.items():
        total = round(sum(float(row.get("hand_net_bb") or 0) for row in group_rows), 4)
        if total >= 0:
            continue
        sample_count = len(group_rows)
        avg = round(total / sample_count, 4)
        max_5_share = _max_5_loss_share(group_rows, total)
        reliability = _reliability(sample_count, max_5_share)
        mined.append(
            {
                "source": source,
                "spot_key": _spot_key(fields, key),
                "sample_count": sample_count,
                "total_hand_net_bb": _clean_number(total),
                "avg_hand_net_bb": _clean_number(avg),
                "max_5_loss_share": max_5_share,
                "reliability_level": reliability,
                "representative_hands": _representative_hands(group_rows),
                "warning": _warning(sample_count, max_5_share, reliability),
            }
        )

    return sorted(mined, key=lambda row: (row["total_hand_net_bb"], row["sample_count"]))[:limit]


def _spot_key(fields: list[str], values: tuple[Any, ...]) -> dict[str, Any]:
    return dict(zip(fields, values))


def _max_5_loss_share(rows: list[dict[str, Any]], total: float) -> float | None:
    losses = sorted([float(row.get("hand_net_bb") or 0) for row in rows if float(row.get("hand_net_bb") or 0) < 0])
    if not losses or total >= 0:
        return None
    top_5_loss = sum(losses[:5])
    total_loss = sum(losses)
    return round(abs(top_5_loss) / abs(total_loss), 4)


def _reliability(sample_count: int, max_5_loss_share: float | None) -> str:
    concentration = max_5_loss_share or 0
    if sample_count < 10 or concentration > 0.8:
        return "low"
    if sample_count < 50 or concentration > 0.5:
        return "medium"
    return "high"


def _warning(sample_count: int, max_5_loss_share: float | None, reliability: str) -> str | None:
    warnings = []
    if sample_count < 10:
        warnings.append("sample_too_small")
    elif sample_count < 50:
        warnings.append("sample_moderate")
    if max_5_loss_share is not None and max_5_loss_share > 0.8:
        warnings.append("loss_concentrated_in_top_5")
    elif max_5_loss_share is not None and max_5_loss_share > 0.5:
        warnings.append("loss_somewhat_concentrated")
    if reliability == "high":
        return None
    return "; ".join(warnings)


def _representative_hands(rows: list[dict[str, Any]]) -> list[str]:
    sorted_rows = sorted(rows, key=lambda row: float(row.get("hand_net_bb") or 0))
    seen = []
    for row in sorted_rows:
        hand_id = row.get("hand_id")
        if hand_id and hand_id not in seen:
            seen.append(hand_id)
        if len(seen) == 5:
            break
    return seen


def _clean_number(value: float) -> int | float:
    return int(value) if value == int(value) else value
