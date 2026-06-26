"""Extract coarse H2N4-style spot features from canonical hands."""

from __future__ import annotations

from collections import Counter
from typing import Any


DECISION_ACTIONS = {"fold", "check", "call", "bet", "raise"}
VOLUNTARY_PREFLOP = {"call", "bet", "raise"}
RANK_ORDER = "23456789TJQKA"
POSITION_ORDER = ["SB", "BB", "UTG", "UTG+1", "LJ", "HJ", "CO", "BTN", "BTN/SB"]


def extract_spot_features(hand: dict[str, Any], hero_name: str | None = None) -> list[dict[str, Any]]:
    """Return one feature row per Hero decision."""

    hero_name = _hero_name(hand, hero_name)
    hero = hand.get("hero") or {}
    hero_position = hero.get("position") or "UNKNOWN"
    players = {player.get("player"): player for player in hand.get("players", [])}
    hand_net_bb = _hero_net_bb(hand, hero_name)
    preflop_line = _preflop_line(hand, hero_name)
    hero_hand_group = _hero_hand_group(hand.get("hero_hole_cards") or [])
    actions = sorted(hand.get("actions", []), key=lambda action: action.get("order", 0))
    rows: list[dict[str, Any]] = []

    for action in actions:
        if action.get("player") != hero_name or action.get("action_type") not in DECISION_ACTIONS:
            continue
        street = action.get("street")
        rows.append(
            {
                "hand_id": hand.get("hand_id"),
                "node_id": f"{hand.get('hand_id')}:{len(rows) + 1}",
                "street": street,
                "hero_position": hero_position,
                "pot_type": _pot_type_before_action(actions, action),
                "player_count_context": _player_count_context(hand, actions, action),
                "position_combo": _position_combo(actions, action, hero_position, players, hero_name),
                "hero_ip_oop": _hero_ip_oop(actions, action, hero_position, players, hero_name),
                "preflop_line": preflop_line,
                "hero_hand_group": hero_hand_group,
                "made_hand_class": _made_hand_class(hand, street),
                "draw_class": _draw_class(hand, street),
                "board_family": _board_family(hand, street),
                "action_line_before": _action_line_before(actions, action),
                "facing_bet_size_bucket": _facing_bet_size_bucket(action),
                "hero_decision": action.get("action_type"),
                "river_runout_class": _river_runout_class(hand, street),
                "hand_net_bb": hand_net_bb,
                "source": "canonical_hand",
                "attribution_warning": "hand_net_bb is full-hand observed result, not decision EV",
            }
        )
    return rows


def _preflop_line(hand: dict[str, Any], hero_name: str) -> str:
    actions = [action for action in _preflop_actions(hand) if action.get("action_type") in DECISION_ACTIONS]
    hero_actions = [action for action in actions if action.get("player") == hero_name]
    if not hero_actions:
        return "no_hero_decision"
    first_hero = hero_actions[0]
    prior = actions[: actions.index(first_hero)]
    prior_raises = [action for action in prior if action.get("action_type") == "raise"]
    hero_raises = [action for action in hero_actions if action.get("action_type") == "raise"]
    if first_hero.get("action_type") == "raise" and not prior_raises:
        if _faced_3bet_after_open(actions, hero_name):
            return "hero_open_faced_3bet"
        return "hero_open"
    if first_hero.get("action_type") == "call" and len(prior_raises) == 1:
        return "hero_flat_vs_open"
    if first_hero.get("action_type") == "raise" and len(prior_raises) == 1:
        return "hero_3bet"
    if any(action.get("action_type") in VOLUNTARY_PREFLOP for action in hero_actions):
        return "hero_vpip_other"
    return "no_hero_vpip"


def _pot_type_before_action(actions: list[dict[str, Any]], current: dict[str, Any]) -> str:
    preflop_before = [
        action
        for action in actions
        if action.get("street") == "preflop"
        and action.get("order", 0) < current.get("order", 0)
        and action.get("action_type") == "raise"
    ]
    if current.get("street") == "preflop" and not preflop_before:
        return "unopened_preflop"
    raises = len(preflop_before)
    if raises == 0:
        return "limped_pot"
    if raises == 1:
        return "single_raised_pot"
    if raises == 2:
        return "three_bet_pot"
    return "four_bet_plus_pot"


def _player_count_context(hand: dict[str, Any], actions: list[dict[str, Any]], current: dict[str, Any]) -> str:
    active = {player.get("player") for player in hand.get("players", []) if player.get("player")}
    for action in actions:
        if action.get("order", 0) >= current.get("order", 0):
            break
        if action.get("action_type") == "fold":
            active.discard(action.get("player"))
    return "heads_up" if len(active) <= 2 else "multiway"


def _position_combo(
    actions: list[dict[str, Any]],
    current: dict[str, Any],
    hero_position: str,
    players: dict[str, dict[str, Any]],
    hero_name: str,
) -> str:
    villain = _recent_non_hero_actor(actions, current, hero_name)
    villain_position = (players.get(villain) or {}).get("position") if villain else None
    return f"{hero_position}_vs_{villain_position or 'UNKNOWN'}"


def _hero_ip_oop(
    actions: list[dict[str, Any]],
    current: dict[str, Any],
    hero_position: str,
    players: dict[str, dict[str, Any]],
    hero_name: str,
) -> str:
    if current.get("street") == "preflop":
        return "unknown"
    villain = _recent_non_hero_actor(actions, current, hero_name)
    villain_position = (players.get(villain) or {}).get("position") if villain else None
    if hero_position not in POSITION_ORDER or villain_position not in POSITION_ORDER:
        return "unknown"
    return "ip" if POSITION_ORDER.index(hero_position) > POSITION_ORDER.index(villain_position) else "oop"


def _recent_non_hero_actor(actions: list[dict[str, Any]], current: dict[str, Any], hero_name: str = "Hero") -> str | None:
    prior = [action for action in actions if action.get("order", 0) < current.get("order", 0)]
    for action in reversed(prior):
        if action.get("player") != hero_name and action.get("action_type") in DECISION_ACTIONS:
            return action.get("player")
    return None


def _hero_hand_group(cards: list[str]) -> str:
    if len(cards) != 2:
        return "unknown"
    ranks = [card[0] for card in cards]
    suited = cards[0][1] == cards[1][1]
    if ranks[0] == ranks[1]:
        return "pocket_pair"
    if "A" in ranks and suited:
        return "suited_ace"
    if "A" in ranks:
        return "offsuit_ace"
    if all(rank in {"T", "J", "Q", "K", "A"} for rank in ranks):
        return "suited_broadway" if suited else "offsuit_broadway"
    return "suited_connector_or_gap" if suited and _rank_gap(ranks) <= 2 else "other"


def _made_hand_class(hand: dict[str, Any], street: str | None) -> str:
    if street == "preflop":
        return "preflop"
    board = _board_cards_for_street(hand, street)
    hero_cards = hand.get("hero_hole_cards") or []
    if not board or len(hero_cards) != 2:
        return "unknown"
    ranks = [card[0] for card in board + hero_cards]
    return "pair_or_better" if max(Counter(ranks).values(), default=0) >= 2 else "no_pair"


def _draw_class(hand: dict[str, Any], street: str | None) -> str:
    if street == "preflop":
        return "preflop"
    board = _board_cards_for_street(hand, street)
    hero_cards = hand.get("hero_hole_cards") or []
    if not board or len(hero_cards) != 2:
        return "unknown"
    suits = Counter(card[1] for card in board + hero_cards)
    return "flush_draw" if max(suits.values(), default=0) == 4 else "backdoor_or_none"


def _board_family(hand: dict[str, Any], street: str | None) -> str:
    board = _board_cards_for_street(hand, street)
    if not board:
        return "preflop"
    ranks = [card[0] for card in board]
    suits = [card[1] for card in board]
    high_rank = max(ranks, key=lambda rank: RANK_ORDER.index(rank))
    paired = "paired" if len(set(ranks)) < len(ranks) else "unpaired"
    suit_counts = Counter(suits)
    if max(suit_counts.values(), default=0) >= 3:
        texture = "monotone" if len(board) == 3 and len(suit_counts) == 1 else "flush_possible"
    elif max(suit_counts.values(), default=0) == 2:
        texture = "two_tone"
    else:
        texture = "rainbow"
    return f"{_rank_name(high_rank)}_high_{texture}_{paired}"


def _action_line_before(actions: list[dict[str, Any]], current: dict[str, Any]) -> str:
    same_street = [
        action.get("action_type")
        for action in actions
        if action.get("street") == current.get("street")
        and action.get("order", 0) < current.get("order", 0)
        and action.get("action_type") in DECISION_ACTIONS
    ]
    return "-".join(str(action) for action in same_street) if same_street else "none"


def _facing_bet_size_bucket(action: dict[str, Any]) -> str:
    facing = action.get("facing_amount_bb")
    pot = action.get("pot_before_bb")
    if facing in (None, 0):
        return "no_bet_faced"
    if action.get("street") == "preflop":
        if facing <= 2.5:
            return "preflop_lte_2_5bb"
        if facing <= 4:
            return "preflop_2_6_to_4bb"
        return "preflop_gt_4bb"
    if not pot:
        return "postflop_unknown_pot"
    ratio = facing / pot
    if ratio <= 0.33:
        return "postflop_lte_33pct_pot"
    if ratio <= 0.66:
        return "postflop_34_to_66pct_pot"
    if ratio <= 1.1:
        return "postflop_67_to_110pct_pot"
    return "postflop_overbet"


def _river_runout_class(hand: dict[str, Any], street: str | None) -> str:
    if street != "river":
        return "not_river"
    board = (hand.get("board") or {}).get("full") or []
    if len(board) < 5:
        return "river_blank_or_unknown"
    river = board[-1]
    previous = board[:-1]
    if river[0] in [card[0] for card in previous]:
        return "river_pairs_board"
    if sum(1 for card in board if card[1] == river[1]) >= 3:
        return "river_flush_completes"
    return "river_blank_or_unknown"


def _board_cards_for_street(hand: dict[str, Any], street: str | None) -> list[str]:
    board = hand.get("board") or {}
    if street == "flop":
        return list(board.get("flop") or [])
    if street == "turn":
        return list((board.get("flop") or []) + (board.get("turn") or []))
    if street == "river":
        return list(board.get("full") or [])
    return []


def _preflop_actions(hand: dict[str, Any]) -> list[dict[str, Any]]:
    return sorted(
        [action for action in hand.get("actions", []) if action.get("street") == "preflop"],
        key=lambda action: action.get("order", 0),
    )


def _faced_3bet_after_open(actions: list[dict[str, Any]], hero_name: str) -> bool:
    raises_seen = 0
    hero_opened = False
    for action in actions:
        if action.get("action_type") != "raise":
            continue
        raises_seen += 1
        if action.get("player") == hero_name and raises_seen == 1:
            hero_opened = True
            continue
        if hero_opened and action.get("player") != hero_name:
            return True
    return False


def _rank_gap(ranks: list[str]) -> int:
    values = sorted(RANK_ORDER.index(rank) for rank in ranks)
    return values[-1] - values[0]


def _rank_name(rank: str) -> str:
    names = {
        "T": "ten",
        "J": "jack",
        "Q": "queen",
        "K": "king",
        "A": "ace",
    }
    return names.get(rank, rank)


def _hero_net_bb(hand: dict[str, Any], hero_name: str) -> float:
    for result in hand.get("results", []):
        if result.get("player") == hero_name:
            return float(result.get("net_bb") or 0)
    return 0.0


def _hero_name(hand: dict[str, Any], hero_name: str | None) -> str:
    if hero_name:
        return hero_name
    return str((hand.get("hero") or {}).get("player") or "Hero")
