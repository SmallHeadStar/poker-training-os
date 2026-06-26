"""Basic Hero-centric poker reports from canonical hands."""

from __future__ import annotations

from collections import defaultdict
from typing import Any


PREFLOP_VOLUNTARY_ACTIONS = {"call", "bet", "raise"}
PREFLOP_DECISION_ACTIONS = {"fold", "call", "raise", "check", "bet"}


def build_basic_reports(hands: list[dict[str, Any]], hero_name: str | None = None) -> dict[str, Any]:
    """Build Phase 2 basic reports from canonical hand dictionaries."""

    hero_hands = [hand for hand in hands if _hero_result(hand, _hero_name(hand, hero_name)) is not None]
    total_hands = len(hero_hands)
    total_profit_bb = round(sum(_hero_net_bb(hand, _hero_name(hand, hero_name)) for hand in hero_hands), 4)

    preflop = [_preflop_summary(hand, _hero_name(hand, hero_name)) for hand in hero_hands]
    postflop = [_postflop_summary(hand, _hero_name(hand, hero_name)) for hand in hero_hands]

    return {
        "session_summary": {
            "hands": total_hands,
            "total_profit_bb": _clean_number(total_profit_bb),
            "bb_per_100": _rate(total_profit_bb * 100, total_hands),
        },
        "position_results": _position_results(hero_hands, hero_name),
        "preflop": {
            "vpip": _fraction(sum(item["vpip"] for item in preflop), total_hands),
            "pfr": _fraction(sum(item["pfr"] for item in preflop), total_hands),
            "rfi_by_position": _rfi_by_position(preflop),
            "three_bet": _fraction(
                sum(item["three_bet_taken"] for item in preflop),
                sum(item["three_bet_opportunity"] for item in preflop),
            ),
            "call_3bet": _fraction(
                sum(item["call_3bet"] for item in preflop),
                sum(item["facing_3bet_after_open"] for item in preflop),
            ),
            "fold_to_3bet": _fraction(
                sum(item["fold_to_3bet"] for item in preflop),
                sum(item["facing_3bet_after_open"] for item in preflop),
            ),
            "four_bet": _fraction(
                sum(item["four_bet"] for item in preflop),
                sum(item["facing_3bet_after_open"] for item in preflop),
            ),
        },
        "showdown": {
            "wtsd": _fraction(
                sum(item["went_to_showdown"] for item in postflop),
                sum(item["saw_flop"] for item in postflop),
            ),
            "w_sd": _fraction(
                sum(item["won_at_showdown"] for item in postflop),
                sum(item["went_to_showdown"] for item in postflop),
            ),
            "wwsf": _fraction(
                sum(item["won_when_saw_flop"] for item in postflop),
                sum(item["saw_flop"] for item in postflop),
            ),
        },
        "stat_opportunities": build_stat_opportunity_rows(hero_hands, hero_name=hero_name),
    }


def build_stat_opportunity_rows(hands: list[dict[str, Any]], hero_name: str | None = None) -> list[dict[str, Any]]:
    """Return one audit row per Hero stat opportunity or non-opportunity.

    These rows are for H2N4 parity investigation. They expose the hand-level
    denominator and numerator decisions behind the aggregate basic reports.
    """

    rows: list[dict[str, Any]] = []
    for hand in hands:
        current_hero_name = _hero_name(hand, hero_name)
        if _hero_result(hand, current_hero_name) is None:
            continue

        preflop = _preflop_summary(hand, current_hero_name)
        postflop = _postflop_summary(hand, current_hero_name)
        rows.extend(
            [
                _stat_opportunity_row(hand, current_hero_name, "preflop", "vpip", True, bool(preflop["vpip"]), "hero_hand"),
                _stat_opportunity_row(hand, current_hero_name, "preflop", "pfr", True, bool(preflop["pfr"]), "hero_hand"),
                _stat_opportunity_row(
                    hand,
                    current_hero_name,
                    "preflop",
                    "rfi",
                    bool(preflop["rfi_opportunity"]),
                    bool(preflop["rfi_taken"]),
                    "no_prior_voluntary_before_hero_first_decision"
                    if preflop["rfi_opportunity"]
                    else "not_first_in_opportunity",
                ),
                _stat_opportunity_row(
                    hand,
                    current_hero_name,
                    "preflop",
                    "three_bet",
                    bool(preflop["three_bet_opportunity"]),
                    bool(preflop["three_bet_taken"]),
                    "facing_exactly_one_prior_raise_at_first_decision"
                    if preflop["three_bet_opportunity"]
                    else "not_three_bet_opportunity",
                ),
                _stat_opportunity_row(
                    hand,
                    current_hero_name,
                    "preflop",
                    "call_3bet",
                    bool(preflop["facing_3bet_after_open"]),
                    bool(preflop["call_3bet"]),
                    "hero_opened_unopened_pot_and_faced_3bet"
                    if preflop["facing_3bet_after_open"]
                    else "not_facing_3bet_after_open",
                ),
                _stat_opportunity_row(
                    hand,
                    current_hero_name,
                    "preflop",
                    "fold_to_3bet",
                    bool(preflop["facing_3bet_after_open"]),
                    bool(preflop["fold_to_3bet"]),
                    "hero_opened_unopened_pot_and_faced_3bet"
                    if preflop["facing_3bet_after_open"]
                    else "not_facing_3bet_after_open",
                ),
                _stat_opportunity_row(
                    hand,
                    current_hero_name,
                    "preflop",
                    "four_bet",
                    bool(preflop["facing_3bet_after_open"]),
                    bool(preflop["four_bet"]),
                    "hero_opened_unopened_pot_and_faced_3bet"
                    if preflop["facing_3bet_after_open"]
                    else "not_facing_3bet_after_open",
                ),
                _stat_opportunity_row(
                    hand,
                    current_hero_name,
                    "showdown",
                    "wtsd",
                    bool(postflop["saw_flop"]),
                    bool(postflop["went_to_showdown"]),
                    "hero_saw_flop" if postflop["saw_flop"] else "hero_did_not_see_flop",
                ),
                _stat_opportunity_row(
                    hand,
                    current_hero_name,
                    "showdown",
                    "w_sd",
                    bool(postflop["went_to_showdown"]),
                    bool(postflop["won_at_showdown"]),
                    "hero_went_to_showdown"
                    if postflop["went_to_showdown"]
                    else "hero_did_not_go_to_showdown",
                ),
                _stat_opportunity_row(
                    hand,
                    current_hero_name,
                    "showdown",
                    "wwsf",
                    bool(postflop["saw_flop"]),
                    bool(postflop["won_when_saw_flop"]),
                    "hero_saw_flop" if postflop["saw_flop"] else "hero_did_not_see_flop",
                ),
            ]
        )
    return rows


def _position_results(hands: list[dict[str, Any]], hero_name: str | None) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, float | int | str | None]] = defaultdict(
        lambda: {"position": None, "hands": 0, "total_profit_bb": 0.0, "bb_per_100": None}
    )
    for hand in hands:
        current_hero_name = _hero_name(hand, hero_name)
        position = (hand.get("hero") or {}).get("position") or "UNKNOWN"
        row = grouped[position]
        row["position"] = position
        row["hands"] = int(row["hands"]) + 1
        row["total_profit_bb"] = float(row["total_profit_bb"]) + _hero_net_bb(hand, current_hero_name)

    position_order = ["UTG", "UTG+1", "LJ", "HJ", "CO", "BTN", "SB", "BB", "BTN/SB", "UNKNOWN"]
    rows = []
    for position, row in grouped.items():
        hands_count = int(row["hands"])
        total = round(float(row["total_profit_bb"]), 4)
        rows.append(
            {
                "position": position,
                "hands": hands_count,
                "total_profit_bb": _clean_number(total),
                "bb_per_100": _rate(total * 100, hands_count),
            }
        )
    return sorted(rows, key=lambda row: position_order.index(row["position"]) if row["position"] in position_order else 99)


def _preflop_summary(hand: dict[str, Any], hero_name: str) -> dict[str, Any]:
    actions = _preflop_actions(hand)
    hero_position = (hand.get("hero") or {}).get("position") or "UNKNOWN"
    hero_actions = [action for action in actions if action.get("player") == hero_name]
    first_hero_decision = next(
        (action for action in hero_actions if action.get("action_type") in PREFLOP_DECISION_ACTIONS),
        None,
    )
    prior_to_first_hero = actions[: actions.index(first_hero_decision)] if first_hero_decision in actions else []
    prior_voluntary = [action for action in prior_to_first_hero if action.get("action_type") in PREFLOP_VOLUNTARY_ACTIONS]
    prior_raises = [action for action in prior_to_first_hero if action.get("action_type") == "raise"]

    vpip = any(action.get("action_type") in PREFLOP_VOLUNTARY_ACTIONS for action in hero_actions)
    pfr = any(action.get("action_type") == "raise" for action in hero_actions)
    rfi_opportunity = first_hero_decision is not None and not prior_voluntary
    rfi_taken = rfi_opportunity and first_hero_decision.get("action_type") == "raise"
    three_bet_opportunity = first_hero_decision is not None and len(prior_raises) == 1
    three_bet_taken = three_bet_opportunity and first_hero_decision.get("action_type") == "raise"
    facing_3bet_after_open, response = _hero_response_to_3bet_after_open(actions, hero_name)

    return {
        "position": hero_position,
        "vpip": int(vpip),
        "pfr": int(pfr),
        "rfi_opportunity": int(rfi_opportunity),
        "rfi_taken": int(rfi_taken),
        "three_bet_opportunity": int(three_bet_opportunity),
        "three_bet_taken": int(three_bet_taken),
        "facing_3bet_after_open": int(facing_3bet_after_open),
        "call_3bet": int(response == "call"),
        "fold_to_3bet": int(response == "fold"),
        "four_bet": int(response == "raise"),
    }


def _hero_response_to_3bet_after_open(actions: list[dict[str, Any]], hero_name: str) -> tuple[bool, str | None]:
    raises_seen = 0
    hero_open_index: int | None = None
    for index, action in enumerate(actions):
        if action.get("action_type") == "raise":
            raises_seen += 1
            prior_voluntary = any(
                prior.get("action_type") in PREFLOP_VOLUNTARY_ACTIONS for prior in actions[:index]
            )
            if action.get("player") == hero_name and raises_seen == 1 and not prior_voluntary:
                hero_open_index = index
                break
    if hero_open_index is None:
        return False, None

    opponent_3bet_index: int | None = None
    for index in range(hero_open_index + 1, len(actions)):
        action = actions[index]
        if action.get("player") == hero_name:
            continue
        if action.get("action_type") == "raise":
            opponent_3bet_index = index
            break
    if opponent_3bet_index is None:
        return False, None

    for action in actions[opponent_3bet_index + 1 :]:
        if action.get("player") == hero_name and action.get("action_type") in {"fold", "call", "raise"}:
            return True, str(action.get("action_type"))
    return False, None


def _postflop_summary(hand: dict[str, Any], hero_name: str) -> dict[str, int]:
    saw_flop = bool((hand.get("board") or {}).get("flop")) and not _hero_folded_on_street(hand, hero_name, "preflop")
    went_to_showdown = saw_flop and any(item.get("player") == hero_name for item in hand.get("showdown", []))
    net_bb = _hero_net_bb(hand, hero_name)
    return {
        "saw_flop": int(saw_flop),
        "went_to_showdown": int(went_to_showdown),
        "won_at_showdown": int(went_to_showdown and net_bb > 0),
        "won_when_saw_flop": int(saw_flop and net_bb > 0),
    }


def _rfi_by_position(preflop: list[dict[str, Any]]) -> list[dict[str, Any]]:
    positions: dict[str, dict[str, int]] = defaultdict(lambda: {"taken": 0, "opportunities": 0})
    for item in preflop:
        position = item["position"]
        positions[position]["taken"] += item["rfi_taken"]
        positions[position]["opportunities"] += item["rfi_opportunity"]
    return [
        {"position": position, **_fraction(values["taken"], values["opportunities"])}
        for position, values in sorted(positions.items())
        if values["opportunities"] > 0
    ]


def _preflop_actions(hand: dict[str, Any]) -> list[dict[str, Any]]:
    return sorted(
        [action for action in hand.get("actions", []) if action.get("street") == "preflop"],
        key=lambda action: action.get("order", 0),
    )


def _hero_folded_on_street(hand: dict[str, Any], hero_name: str, street: str) -> bool:
    return any(
        action.get("player") == hero_name
        and action.get("street") == street
        and action.get("action_type") == "fold"
        for action in hand.get("actions", [])
    )


def _hero_result(hand: dict[str, Any], hero_name: str) -> dict[str, Any] | None:
    return next((result for result in hand.get("results", []) if result.get("player") == hero_name), None)


def _hero_net_bb(hand: dict[str, Any], hero_name: str) -> float:
    result = _hero_result(hand, hero_name)
    if result is None:
        return 0.0
    return float(result.get("net_bb") or 0)


def _stat_opportunity_row(
    hand: dict[str, Any],
    hero_name: str,
    section: str,
    metric: str,
    opportunity: bool,
    hit: bool,
    reason: str,
) -> dict[str, Any]:
    return {
        "hand_id": hand.get("hand_id"),
        "hero_player": hero_name,
        "section": section,
        "metric": metric,
        "position": (hand.get("hero") or {}).get("position"),
        "opportunity": int(opportunity),
        "hit": int(hit) if opportunity else 0,
        "opportunity_reason": reason,
        "h2n4_comparison_status": "implemented_provisional",
    }


def _hero_name(hand: dict[str, Any], hero_name: str | None) -> str:
    if hero_name:
        return hero_name
    return str((hand.get("hero") or {}).get("player") or "Hero")


def _fraction(numerator: int | float, denominator: int | float) -> dict[str, Any]:
    return {
        "numerator": int(numerator),
        "denominator": int(denominator),
        "percent": _rate(float(numerator) * 100, int(denominator)),
    }


def _rate(numerator: float, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return _clean_number(round(numerator / denominator, 2))


def _clean_number(value: float) -> int | float:
    return int(value) if value == int(value) else value
