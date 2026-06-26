"""Simplified observed action-result analysis."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from poker_training_os.features import extract_spot_features


COMMITTING_ACTIONS = {"ante", "post_blind", "call", "bet", "raise"}


def build_action_result_rows(hand: dict[str, Any], hero_name: str | None = None) -> list[dict[str, Any]]:
    """Build action-result rows from Hero spot features."""

    hero_name = _hero_name(hand, hero_name)
    features = extract_spot_features(hand, hero_name=hero_name)
    actions = sorted(hand.get("actions", []), key=lambda action: action.get("order", 0))
    by_order = {
        f"{hand.get('hand_id')}:{index + 1}": action
        for index, action in enumerate(
            [action for action in actions if action.get("player") == hero_name and action.get("action_type") in {"fold", "check", "call", "bet", "raise"}]
        )
    }
    rows = []
    for feature in features:
        action = by_order.get(feature["node_id"])
        action_profit = _action_profit(feature, actions, hero_name, action)
        row = {
            **feature,
            "action_opportunity_count": 1,
            "action_taken_count": 1,
            "observed_result": _observed_result(feature),
            "action_profit_bb": action_profit,
            "decision_incremental_bb": action_profit,
            "incremental_basis": "h2n_action_profit_formula_provisional",
        }
        if feature["hero_decision"] == "fold":
            row["observed_result"] = 0
            row["action_profit_bb"] = 0
            row["decision_incremental_bb"] = 0
            row["incremental_basis"] = "fold_action_profit_zero"
        rows.append(row)
    return rows


def summarize_action_results(rows: list[dict[str, Any]], group_by: list[str]) -> list[dict[str, Any]]:
    """Aggregate action-result rows by spot fields."""

    grouped: dict[tuple[Any, ...], dict[str, Any]] = defaultdict(
        lambda: {
            "action_opportunity_count": 0,
            "action_taken_count": 0,
            "total_observed_result": 0.0,
            "incremental_count": 0,
            "total_decision_incremental_bb": 0.0,
        }
    )
    for row in rows:
        key = tuple(row.get(field) for field in group_by)
        bucket = grouped[key]
        for field, value in zip(group_by, key):
            bucket[field] = value
        bucket["action_opportunity_count"] += int(row.get("action_opportunity_count") or 0)
        bucket["action_taken_count"] += int(row.get("action_taken_count") or 0)
        bucket["total_observed_result"] += float(row.get("observed_result") or 0)
        if row.get("decision_incremental_bb") is not None:
            bucket["incremental_count"] += 1
            bucket["total_decision_incremental_bb"] += float(row.get("decision_incremental_bb") or 0)

    output = []
    for bucket in grouped.values():
        taken = bucket["action_taken_count"]
        incremental_count = bucket["incremental_count"]
        total_observed = round(bucket["total_observed_result"], 4)
        total_incremental = round(bucket["total_decision_incremental_bb"], 4)
        output.append(
            {
                **{field: bucket[field] for field in group_by},
                "action_opportunity_count": bucket["action_opportunity_count"],
                "action_taken_count": taken,
                "total_observed_result": _clean_number(total_observed),
                "avg_observed_result": _clean_number(round(total_observed / taken, 4)) if taken else None,
                "incremental_count": incremental_count,
                "total_decision_incremental_bb": _clean_number(total_incremental) if incremental_count else None,
                "avg_decision_incremental_bb": _clean_number(round(total_incremental / incremental_count, 4))
                if incremental_count
                else None,
            }
        )
    return sorted(output, key=lambda row: tuple(str(row.get(field)) for field in group_by))


def _observed_result(feature: dict[str, Any]) -> float:
    return float(feature.get("hand_net_bb") or 0)


def _action_profit(
    feature: dict[str, Any],
    actions: list[dict[str, Any]],
    hero_name: str,
    action: dict[str, Any] | None,
) -> int | float | None:
    if action is None:
        return None
    predecision_contrib = _hero_contributed_before(actions, hero_name, action.get("order", 0))
    return _clean_number(round(float(feature.get("hand_net_bb") or 0) + predecision_contrib, 4))


def _hero_contributed_before(actions: list[dict[str, Any]], hero_name: str, order: int) -> float:
    contributed = 0.0
    returned = 0.0
    for action in actions:
        if action.get("order", 0) >= order or action.get("player") != hero_name:
            continue
        action_type = action.get("action_type")
        amount = float(action.get("amount_bb") or 0)
        if action_type in COMMITTING_ACTIONS:
            contributed += amount
        elif action_type == "return_uncalled_bet":
            returned += amount
    return contributed - returned


def _clean_number(value: float) -> int | float:
    return int(value) if value == int(value) else value


def _hero_name(hand: dict[str, Any], hero_name: str | None) -> str:
    if hero_name:
        return hero_name
    return str((hand.get("hero") or {}).get("player") or "Hero")
