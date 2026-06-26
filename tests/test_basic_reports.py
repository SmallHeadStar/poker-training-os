from pathlib import Path

from poker_training_os.parsers.gg_pokercraft import parse_hand
from poker_training_os.reports import build_basic_reports


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "gg_pokercraft_cash_hand.txt"


def test_basic_reports_use_h2n4_style_opportunities_and_hits() -> None:
    hands = [
        parse_hand(FIXTURE.read_text(encoding="utf-8")),
        _hand(
            position="BTN",
            net_bb=-2.5,
            actions=[
                _action(1, "preflop", "Hero", "raise"),
                _action(2, "preflop", "BB", "raise"),
                _action(3, "preflop", "Hero", "fold"),
            ],
        ),
        _hand(
            position="CO",
            net_bb=-12,
            actions=[
                _action(1, "preflop", "Hero", "raise"),
                _action(2, "preflop", "BB", "raise"),
                _action(3, "preflop", "Hero", "call"),
                _action(4, "flop", "BB", "bet"),
                _action(5, "flop", "Hero", "fold"),
            ],
            board={"flop": ["As", "7h", "2d"], "turn": [], "river": [], "full": ["As", "7h", "2d"]},
        ),
        _hand(
            position="SB",
            net_bb=9,
            actions=[
                _action(1, "preflop", "Hero", "raise"),
                _action(2, "preflop", "BB", "raise"),
                _action(3, "preflop", "Hero", "raise"),
                _action(4, "preflop", "BB", "fold"),
            ],
        ),
        _hand(
            position="BB",
            net_bb=4,
            actions=[
                _action(1, "preflop", "CO", "raise"),
                _action(2, "preflop", "Hero", "raise"),
                _action(3, "preflop", "CO", "fold"),
            ],
        ),
    ]

    reports = build_basic_reports(hands)

    assert reports["session_summary"] == {
        "hands": 5,
        "total_profit_bb": 27,
        "bb_per_100": 540,
    }
    assert reports["preflop"]["vpip"] == {"numerator": 5, "denominator": 5, "percent": 100}
    assert reports["preflop"]["pfr"] == {"numerator": 4, "denominator": 5, "percent": 80}
    assert reports["preflop"]["three_bet"] == {"numerator": 1, "denominator": 2, "percent": 50}
    assert reports["preflop"]["call_3bet"] == {"numerator": 1, "denominator": 3, "percent": 33.33}
    assert reports["preflop"]["fold_to_3bet"] == {"numerator": 1, "denominator": 3, "percent": 33.33}
    assert reports["preflop"]["four_bet"] == {"numerator": 1, "denominator": 3, "percent": 33.33}
    assert reports["showdown"]["wtsd"] == {"numerator": 1, "denominator": 2, "percent": 50}
    assert reports["showdown"]["w_sd"] == {"numerator": 1, "denominator": 1, "percent": 100}
    assert reports["showdown"]["wwsf"] == {"numerator": 1, "denominator": 2, "percent": 50}


def test_basic_reports_use_canonical_hero_player_when_name_is_not_literal_hero() -> None:
    hand = parse_hand(FIXTURE.read_text(encoding="utf-8").replace("Hero", "student_hero"))

    reports = build_basic_reports([hand])

    assert reports["session_summary"] == {
        "hands": 1,
        "total_profit_bb": 28.5,
        "bb_per_100": 2850,
    }
    assert reports["preflop"]["vpip"] == {"numerator": 1, "denominator": 1, "percent": 100}
    assert reports["preflop"]["pfr"] == {"numerator": 0, "denominator": 1, "percent": 0}
    assert reports["showdown"]["w_sd"] == {"numerator": 1, "denominator": 1, "percent": 100}


def test_rfi_is_grouped_by_position_with_denominators() -> None:
    reports = build_basic_reports(
        [
            _hand("BTN", 3, [_action(1, "preflop", "Hero", "raise"), _action(2, "preflop", "BB", "fold")]),
            _hand("BTN", -1, [_action(1, "preflop", "Hero", "fold")]),
            _hand("CO", 2, [_action(1, "preflop", "UTG", "raise"), _action(2, "preflop", "Hero", "fold")]),
        ]
    )

    assert reports["preflop"]["rfi_by_position"] == [
        {"position": "BTN", "numerator": 1, "denominator": 2, "percent": 50}
    ]


def test_iso_raise_then_faces_3bet_is_not_open_vs_3bet_until_h2n4_confirms() -> None:
    reports = build_basic_reports(
        [
            _hand(
                "CO",
                -6,
                [
                    _action(1, "preflop", "UTG", "call"),
                    _action(2, "preflop", "Hero", "raise"),
                    _action(3, "preflop", "BTN", "raise"),
                    _action(4, "preflop", "Hero", "fold"),
                ],
            )
        ]
    )

    assert reports["preflop"]["pfr"] == {"numerator": 1, "denominator": 1, "percent": 100}
    assert reports["preflop"]["fold_to_3bet"] == {"numerator": 0, "denominator": 0, "percent": None}


def _hand(
    position: str,
    net_bb: float,
    actions: list[dict],
    board: dict | None = None,
    showdown: list[dict] | None = None,
) -> dict:
    return {
        "hero": {"player": "Hero", "seat": 1, "position": position},
        "actions": actions,
        "board": board or {"flop": [], "turn": [], "river": [], "full": []},
        "showdown": showdown or [],
        "results": [{"player": "Hero", "net_bb": net_bb}],
    }


def _action(order: int, street: str, player: str, action_type: str) -> dict:
    return {
        "order": order,
        "street": street,
        "player": player,
        "action_type": action_type,
    }
