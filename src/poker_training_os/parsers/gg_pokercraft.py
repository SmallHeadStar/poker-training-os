"""Minimal GG PokerCraft hand-history parser."""

from __future__ import annotations

import re
from collections import defaultdict
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "0.1"
CARD_RE = r"[2-9TJQKA][cdhs]"
HEADER_RE = re.compile(
    r"^Poker Hand #(?P<hand_id>[A-Z]+\d+): (?P<description>.+?) - "
    r"(?P<played_at>\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})$"
)
TABLE_RE = re.compile(r"^Table '(?P<table>.+)' (?P<max_seats>\d+)-max Seat #(?P<button>\d+) is the button$")
SEAT_RE = re.compile(r"^Seat (?P<seat>\d+): (?P<player>.+?) \((?P<stack>.+?) in chips\)$")
POST_RE = re.compile(
    r"^(?P<player>.+?): posts (?:the )?(?P<kind>ante|small blind|big blind) (?P<amount>[$€£¥]?[\d,.]+)$"
)
DEALT_RE = re.compile(r"^Dealt to (?P<player>.+?)(?: \[(?P<cards>[^\]]+)\])?$")
FLOP_RE = re.compile(rf"^\*\*\* FLOP \*\*\* \[(?P<cards>(?:{CARD_RE} ?){{3}})\]$")
TURN_RE = re.compile(rf"^\*\*\* TURN \*\*\* \[(?P<flop>(?:{CARD_RE} ?){{3}})\] \[(?P<turn>{CARD_RE})\]$")
RIVER_RE = re.compile(
    rf"^\*\*\* RIVER \*\*\* \[(?P<turn_board>(?:{CARD_RE} ?){{4}})\] \[(?P<river>{CARD_RE})\]$"
)
CALL_RE = re.compile(r"^(?P<player>.+?): calls (?P<amount>[$€£¥]?[\d,.]+)(?P<allin> and is all-in)?$")
BET_RE = re.compile(r"^(?P<player>.+?): bets (?P<amount>[$€£¥]?[\d,.]+)(?P<allin> and is all-in)?$")
RAISE_RE = re.compile(
    r"^(?P<player>.+?): raises (?P<raise_amount>[$€£¥]?[\d,.]+) to "
    r"(?P<to_amount>[$€£¥]?[\d,.]+)(?P<allin> and is all-in)?$"
)
SIMPLE_ACTION_RE = re.compile(r"^(?P<player>.+?): (?P<verb>folds|checks)(?P<allin> and is all-in)?$")
SHOW_RE = re.compile(rf"^(?P<player>.+?): shows \[(?P<cards>(?:{CARD_RE} ?)+)\](?: \((?P<made_hand>.+)\))?$")
COLLECT_RE = re.compile(r"^(?P<player>.+?) collected (?P<amount>[$€£¥]?[\d,.]+) from pot$")
RETURN_RE = re.compile(r"^Uncalled bet \((?P<amount>[$€£¥]?[\d,.]+)\) returned to (?P<player>.+)$")
TOTAL_POT_RE = re.compile(r"^Total pot (?P<pot>[$€£¥]?[\d,.]+)(?P<rest>.*)$")
BOARD_RE = re.compile(rf"^Board \[(?P<cards>(?:{CARD_RE} ?)+)\]$")
SUMMARY_SEAT_RE = re.compile(r"^Seat (?P<seat>\d+): (?P<player>.+)$")


class PokerCraftParseError(ValueError):
    """Raised when a hand cannot be parsed as a PokerCraft export."""


def parse_hands_from_file(path: str | Path, hero_name: str | None = None) -> list[dict[str, Any]]:
    file_path = Path(path)
    return parse_hands(file_path.read_text(encoding="utf-8"), source_name=str(file_path), hero_name=hero_name)


def parse_hands(text: str, source_name: str | None = None, hero_name: str | None = None) -> list[dict[str, Any]]:
    chunks = [
        chunk.strip()
        for chunk in re.split(r"(?=^Poker Hand #[A-Z]+\d+:)", text, flags=re.MULTILINE)
        if chunk.strip()
    ]
    if not chunks:
        raise PokerCraftParseError("No PokerCraft hand headers found.")
    return [parse_hand(chunk, source_name=source_name, hero_name=hero_name) for chunk in chunks]


def parse_hand(text: str, source_name: str | None = None, hero_name: str | None = None) -> dict[str, Any]:
    lines = [line.strip() for line in text.replace("\ufeff", "").splitlines() if line.strip()]
    if not lines:
        raise PokerCraftParseError("Empty hand history.")

    header_match = HEADER_RE.match(lines[0])
    if not header_match:
        raise PokerCraftParseError(f"Unsupported PokerCraft header: {lines[0]}")

    description = header_match.group("description")
    hand_id = header_match.group("hand_id")
    game = _parse_game(description, hand_id)
    played_at = datetime.strptime(header_match.group("played_at"), "%Y/%m/%d %H:%M:%S").isoformat()

    table_name: str | None = None
    button_seat: int | None = None
    max_seats: int | None = None
    players: list[dict[str, Any]] = []
    explicit_hero_name = hero_name.strip() if hero_name else None
    dealt_private_cards_by_player: dict[str, list[str]] = {}
    dealt_private_cards_candidate: str | None = None
    hero_hole_cards: list[str] = []
    actions: list[dict[str, Any]] = []
    board: dict[str, list[str]] = {"flop": [], "turn": [], "river": [], "full": []}
    showdown: list[dict[str, Any]] = []
    parser_warnings: list[str] = []
    summary_by_player: dict[str, str] = {}
    summary_totals: dict[str, Any] = {}
    current_street = "setup"
    order = 0

    total_contributed: defaultdict[str, Decimal] = defaultdict(Decimal)
    total_returned: defaultdict[str, Decimal] = defaultdict(Decimal)
    total_collected: defaultdict[str, Decimal] = defaultdict(Decimal)
    street_contrib: defaultdict[str, Decimal] = defaultdict(Decimal)
    pot_committed = Decimal("0")

    for line in lines[1:]:
        table_match = TABLE_RE.match(line)
        if table_match:
            table_name = table_match.group("table")
            max_seats = int(table_match.group("max_seats"))
            button_seat = int(table_match.group("button"))
            continue

        seat_match = SEAT_RE.match(line)
        if seat_match:
            stack = _parse_amount(seat_match.group("stack"))
            players.append(
                {
                    "seat": int(seat_match.group("seat")),
                    "player": seat_match.group("player"),
                    "starting_stack": _number(stack),
                    "starting_stack_bb": _bb(stack, game["big_blind_decimal"]),
                    "position": None,
                    "is_hero": False,
                }
            )
            continue

        if line == "*** HOLE CARDS ***":
            current_street = "preflop"
            continue

        post_match = POST_RE.match(line)
        if post_match:
            player = post_match.group("player")
            amount = _parse_amount(post_match.group("amount"))
            kind = post_match.group("kind")
            action_type = "ante" if kind == "ante" else "post_blind"
            facing = _facing_amount(street_contrib, player)
            order += 1
            actions.append(
                _action(
                    order=order,
                    street="preflop",
                    player=player,
                    action_type=action_type,
                    amount=amount,
                    big_blind=game["big_blind_decimal"],
                    facing=facing,
                    pot_before=pot_committed,
                    raw_text=line,
                    extra={"blind_type": kind if kind != "ante" else None},
                )
            )
            total_contributed[player] += amount
            street_contrib[player] += amount
            pot_committed += amount
            continue

        dealt_match = DEALT_RE.match(line)
        if dealt_match:
            dealt_player = dealt_match.group("player")
            cards = _cards(dealt_match.group("cards") or "")
            if cards:
                dealt_private_cards_by_player[dealt_player] = cards
                if explicit_hero_name is None and dealt_private_cards_candidate is None:
                    dealt_private_cards_candidate = dealt_player
            continue

        flop_match = FLOP_RE.match(line)
        if flop_match:
            current_street = "flop"
            street_contrib = defaultdict(Decimal)
            board["flop"] = _cards(flop_match.group("cards"))
            board["full"] = list(board["flop"])
            continue

        turn_match = TURN_RE.match(line)
        if turn_match:
            current_street = "turn"
            street_contrib = defaultdict(Decimal)
            board["flop"] = _cards(turn_match.group("flop"))
            board["turn"] = [turn_match.group("turn")]
            board["full"] = board["flop"] + board["turn"]
            continue

        river_match = RIVER_RE.match(line)
        if river_match:
            current_street = "river"
            street_contrib = defaultdict(Decimal)
            turn_board = _cards(river_match.group("turn_board"))
            board["flop"] = turn_board[:3]
            board["turn"] = turn_board[3:4]
            board["river"] = [river_match.group("river")]
            board["full"] = turn_board + board["river"]
            continue

        if line == "*** SHOWDOWN ***":
            current_street = "showdown"
            continue

        if line == "*** SUMMARY ***":
            current_street = "summary"
            continue

        action_record = _parse_player_action(
            line=line,
            current_street=current_street,
            order=order + 1,
            street_contrib=street_contrib,
            pot_before=pot_committed,
            big_blind=game["big_blind_decimal"],
        )
        if action_record:
            order += 1
            actions.append(action_record["action"])
            amount = action_record["committed"]
            if amount:
                player = action_record["action"]["player"]
                total_contributed[player] += amount
                street_contrib[player] += amount
                pot_committed += amount
            continue

        return_match = RETURN_RE.match(line)
        if return_match:
            player = return_match.group("player")
            amount = _parse_amount(return_match.group("amount"))
            order += 1
            actions.append(
                _action(
                    order=order,
                    street=current_street,
                    player=player,
                    action_type="return_uncalled_bet",
                    amount=amount,
                    big_blind=game["big_blind_decimal"],
                    facing=Decimal("0"),
                    pot_before=pot_committed,
                    raw_text=line,
                )
            )
            total_returned[player] += amount
            pot_committed -= amount
            continue

        show_match = SHOW_RE.match(line)
        if show_match:
            showdown.append(
                {
                    "player": show_match.group("player"),
                    "cards": _cards(show_match.group("cards")),
                    "made_hand": show_match.group("made_hand"),
                    "raw_text": line,
                }
            )
            continue

        collect_match = COLLECT_RE.match(line)
        if collect_match:
            player = collect_match.group("player")
            amount = _parse_amount(collect_match.group("amount"))
            total_collected[player] += amount
            order += 1
            actions.append(
                _action(
                    order=order,
                    street="showdown",
                    player=player,
                    action_type="collect_pot",
                    amount=amount,
                    big_blind=game["big_blind_decimal"],
                    facing=Decimal("0"),
                    pot_before=pot_committed,
                    raw_text=line,
                )
            )
            continue

        total_pot_match = TOTAL_POT_RE.match(line)
        if total_pot_match:
            summary_totals["total_pot"] = _number(_parse_amount(total_pot_match.group("pot")))
            summary_totals.update(_parse_summary_amounts(total_pot_match.group("rest")))
            continue

        board_match = BOARD_RE.match(line)
        if board_match:
            full_board = _cards(board_match.group("cards"))
            board["full"] = full_board
            board["flop"] = full_board[:3]
            board["turn"] = full_board[3:4]
            board["river"] = full_board[4:5]
            continue

        summary_seat_match = SUMMARY_SEAT_RE.match(line)
        if summary_seat_match:
            summary_name = _summary_player_name(
                summary_seat_match.group("player"),
                [player["player"] for player in players],
            )
            summary_by_player[summary_name] = line
            continue

        parser_warnings.append(f"Unparsed line: {line}")

    if table_name is not None:
        game["table_name"] = table_name
    if max_seats is not None:
        game["max_seats"] = max_seats
    if button_seat is not None:
        game["button_seat"] = button_seat
        _assign_positions(players, button_seat)
    game["table_type"] = _table_type(hand_id, table_name, description)
    big_blind = game.pop("big_blind_decimal")

    resolved_hero_name = _resolve_hero_name(players, explicit_hero_name, dealt_private_cards_candidate)
    for player in players:
        player["is_hero"] = player["player"] == resolved_hero_name
    if resolved_hero_name:
        hero_hole_cards = dealt_private_cards_by_player.get(resolved_hero_name, [])

    hero_player = next((player for player in players if player["is_hero"]), None)
    if hero_player is None:
        missing_hero_name = resolved_hero_name or explicit_hero_name or "Hero"
        parser_warnings.append(f"Hero seat was not found for player: {missing_hero_name}.")
        hero = {"player": missing_hero_name, "seat": None, "position": None}
    else:
        hero = {"player": hero_player["player"], "seat": hero_player["seat"], "position": hero_player["position"]}

    if not hero_hole_cards:
        parser_warnings.append("Hero hole cards were not found.")

    return {
        "schema_version": SCHEMA_VERSION,
        "source": {
            "site": "GGPoker",
            "format": "PokerCraft hand history",
            "file": source_name,
            "imported_from": "manual_export",
        },
        "hand_id": hand_id,
        "played_at": played_at,
        "game": game,
        "hero": hero,
        "players": players,
        "hero_hole_cards": hero_hole_cards,
        "actions": actions,
        "board": board,
        "showdown": showdown,
        "results": _build_results(
            players=players,
            contributed=total_contributed,
            returned=total_returned,
            collected=total_collected,
            summary_by_player=summary_by_player,
            big_blind=big_blind,
        ),
        "summary": summary_totals,
        "parser_warnings": parser_warnings,
    }


def _resolve_hero_name(
    players: list[dict[str, Any]],
    explicit_hero_name: str | None,
    dealt_private_cards_candidate: str | None,
) -> str | None:
    player_names = {player["player"] for player in players}
    if explicit_hero_name:
        return explicit_hero_name
    if dealt_private_cards_candidate and dealt_private_cards_candidate in player_names:
        return dealt_private_cards_candidate
    if "Hero" in player_names:
        return "Hero"
    return None


def _summary_player_name(raw_summary_player: str, player_names: list[str]) -> str:
    for name in sorted(player_names, key=len, reverse=True):
        if raw_summary_player == name or raw_summary_player.startswith(f"{name} "):
            return name
    return raw_summary_player.split(" ", 1)[0]


def _parse_game(description: str, hand_id: str) -> dict[str, Any]:
    small_blind, big_blind, currency = _parse_blinds(description)
    return {
        "family": "holdem" if "Hold'em" in description else "unknown",
        "limit": "no_limit" if "No Limit" in description else "unknown",
        "description": description,
        "stake": _stake_text(small_blind, big_blind, currency),
        "currency": currency,
        "small_blind": _number(small_blind),
        "big_blind": _number(big_blind),
        "big_blind_decimal": big_blind,
        "hand_prefix": re.match(r"^[A-Z]+", hand_id).group(0) if re.match(r"^[A-Z]+", hand_id) else None,
    }


def _parse_blinds(description: str) -> tuple[Decimal, Decimal, str | None]:
    match = re.search(
        r"(?P<currency>[$€£¥]?)(?P<sb>\d[\d,.]*)\s*/\s*(?P=currency)?(?P<bb>\d[\d,.]*)",
        description,
    )
    if not match:
        return Decimal("0"), Decimal("1"), None
    return (_parse_amount(match.group("sb")), _parse_amount(match.group("bb")), match.group("currency") or None)


def _stake_text(small_blind: Decimal, big_blind: Decimal, currency: str | None) -> str:
    prefix = currency or ""
    return f"{prefix}{_decimal_text(small_blind)}/{prefix}{_decimal_text(big_blind)}"


def _table_type(hand_id: str, table_name: str | None, description: str) -> str:
    table = table_name or ""
    if hand_id.startswith("RC") or "RushAndCash" in table:
        return "rush_and_cash"
    if hand_id.startswith("TM") or "Tournament" in description:
        return "tournament"
    if hand_id.startswith("HD"):
        return "cash"
    return "unknown"


def _parse_player_action(
    *,
    line: str,
    current_street: str,
    order: int,
    street_contrib: defaultdict[str, Decimal],
    pot_before: Decimal,
    big_blind: Decimal,
) -> dict[str, Any] | None:
    simple_match = SIMPLE_ACTION_RE.match(line)
    if simple_match:
        player = simple_match.group("player")
        verb = simple_match.group("verb")
        return {
            "committed": Decimal("0"),
            "action": _action(
                order=order,
                street=current_street,
                player=player,
                action_type="fold" if verb == "folds" else "check",
                amount=None,
                big_blind=big_blind,
                facing=_facing_amount(street_contrib, player),
                pot_before=pot_before,
                raw_text=line,
                extra={"is_all_in": bool(simple_match.group("allin"))},
            ),
        }

    call_match = CALL_RE.match(line)
    if call_match:
        amount = _parse_amount(call_match.group("amount"))
        player = call_match.group("player")
        return {
            "committed": amount,
            "action": _action(
                order=order,
                street=current_street,
                player=player,
                action_type="call",
                amount=amount,
                big_blind=big_blind,
                facing=_facing_amount(street_contrib, player),
                pot_before=pot_before,
                raw_text=line,
                extra={"is_all_in": bool(call_match.group("allin"))},
            ),
        }

    bet_match = BET_RE.match(line)
    if bet_match:
        amount = _parse_amount(bet_match.group("amount"))
        player = bet_match.group("player")
        return {
            "committed": amount,
            "action": _action(
                order=order,
                street=current_street,
                player=player,
                action_type="bet",
                amount=amount,
                big_blind=big_blind,
                facing=_facing_amount(street_contrib, player),
                pot_before=pot_before,
                raw_text=line,
                extra={"is_all_in": bool(bet_match.group("allin"))},
            ),
        }

    raise_match = RAISE_RE.match(line)
    if raise_match:
        player = raise_match.group("player")
        raise_amount = _parse_amount(raise_match.group("raise_amount"))
        to_amount = _parse_amount(raise_match.group("to_amount"))
        committed = max(to_amount - street_contrib[player], Decimal("0"))
        return {
            "committed": committed,
            "action": _action(
                order=order,
                street=current_street,
                player=player,
                action_type="raise",
                amount=committed,
                big_blind=big_blind,
                facing=_facing_amount(street_contrib, player),
                pot_before=pot_before,
                raw_text=line,
                extra={
                    "raise_amount": _number(raise_amount),
                    "raise_amount_bb": _bb(raise_amount, big_blind),
                    "to_amount": _number(to_amount),
                    "to_amount_bb": _bb(to_amount, big_blind),
                    "is_all_in": bool(raise_match.group("allin")),
                },
            ),
        }

    return None


def _action(
    *,
    order: int,
    street: str,
    player: str,
    action_type: str,
    amount: Decimal | None,
    big_blind: Decimal,
    facing: Decimal | None,
    pot_before: Decimal,
    raw_text: str,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "street": street,
        "order": order,
        "player": player,
        "action_type": action_type,
        "amount": _number(amount) if amount is not None else None,
        "amount_bb": _bb(amount, big_blind) if amount is not None else None,
        "facing_amount_bb": _bb(facing, big_blind) if facing is not None else None,
        "pot_before_bb": _bb(pot_before, big_blind),
        "raw_text": raw_text,
    }
    if extra:
        payload.update({key: value for key, value in extra.items() if value is not None})
    return payload


def _facing_amount(street_contrib: defaultdict[str, Decimal], player: str) -> Decimal:
    current_max = max(street_contrib.values(), default=Decimal("0"))
    return max(current_max - street_contrib[player], Decimal("0"))


def _build_results(
    *,
    players: list[dict[str, Any]],
    contributed: defaultdict[str, Decimal],
    returned: defaultdict[str, Decimal],
    collected: defaultdict[str, Decimal],
    summary_by_player: dict[str, str],
    big_blind: Decimal,
) -> list[dict[str, Any]]:
    results = []
    for player in players:
        name = player["player"]
        net = collected[name] + returned[name] - contributed[name]
        results.append(
            {
                "player": name,
                "seat": player["seat"],
                "position": player["position"],
                "contributed": _number(contributed[name]),
                "returned": _number(returned[name]),
                "collected": _number(collected[name]),
                "net": _number(net),
                "net_bb": _bb(net, big_blind),
                "raw_summary": summary_by_player.get(name),
            }
        )
    return results


def _assign_positions(players: list[dict[str, Any]], button_seat: int) -> None:
    if not players:
        return
    players.sort(key=lambda player: player["seat"])
    seats = [player["seat"] for player in players]
    if button_seat not in seats:
        return
    button_index = seats.index(button_seat)
    clockwise = players[button_index:] + players[:button_index]
    if len(clockwise) == 2:
        labels = ["BTN/SB", "BB"]
    else:
        remaining = len(clockwise) - 3
        before_button_by_count = {
            0: [],
            1: ["CO"],
            2: ["HJ", "CO"],
            3: ["UTG", "HJ", "CO"],
            4: ["UTG", "LJ", "HJ", "CO"],
            5: ["UTG", "UTG+1", "LJ", "HJ", "CO"],
            6: ["UTG", "UTG+1", "MP", "LJ", "HJ", "CO"],
        }
        labels = ["BTN", "SB", "BB"] + before_button_by_count.get(
            remaining, [f"EP{i + 1}" for i in range(remaining)]
        )
    for player, label in zip(clockwise, labels):
        player["position"] = label


def _parse_amount(raw: str) -> Decimal:
    cleaned = raw.strip().replace(",", "")
    cleaned = re.sub(r"^[^\d.-]+", "", cleaned)
    try:
        return Decimal(cleaned)
    except InvalidOperation as exc:
        raise PokerCraftParseError(f"Invalid numeric amount: {raw}") from exc


def _parse_summary_amounts(raw: str) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for part in raw.split("|"):
        piece = part.strip()
        if not piece:
            continue
        match = re.match(r"(?P<name>[A-Za-z ]+) (?P<amount>[$€£¥]?[\d,.]+)", piece)
        if match:
            key = match.group("name").strip().lower().replace(" ", "_")
            values[key] = _number(_parse_amount(match.group("amount")))
    return values


def _cards(raw: str) -> list[str]:
    return re.findall(CARD_RE, raw or "")


def _number(value: Decimal | None) -> int | float | None:
    if value is None:
        return None
    if value == value.to_integral_value():
        return int(value)
    return float(value)


def _bb(value: Decimal | None, big_blind: Decimal) -> int | float | None:
    if value is None or big_blind == 0:
        return None
    return _number((value / big_blind).quantize(Decimal("0.0001")).normalize())


def _decimal_text(value: Decimal) -> str:
    return format(value.normalize(), "f")
