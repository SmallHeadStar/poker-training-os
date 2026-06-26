import json
from pathlib import Path

import pytest

from poker_training_os.cli import main
from poker_training_os.contracts import missing_required_fields
from poker_training_os.parsers.gg_pokercraft import PokerCraftParseError, parse_hand, parse_hands


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "gg_pokercraft_cash_hand.txt"


def test_parse_cash_hand_to_canonical_json() -> None:
    hand = parse_hand(FIXTURE.read_text(encoding="utf-8"), source_name=str(FIXTURE))

    assert missing_required_fields(hand) == []
    assert hand["schema_version"] == "0.1"
    assert hand["hand_id"] == "HD1000000001"
    assert hand["played_at"] == "2026-06-01T21:15:00"
    assert hand["game"]["table_type"] == "cash"
    assert hand["game"]["stake"] == "$0.05/$0.1"
    assert hand["game"]["big_blind"] == 0.1
    assert hand["hero"] == {"player": "Hero", "seat": 3, "position": "BTN"}
    assert hand["hero_hole_cards"] == ["Ah", "Kh"]
    assert hand["board"]["full"] == ["Kc", "7d", "2s", "4h", "9c"]
    assert hand["parser_warnings"] == []


def test_parse_infers_hero_from_private_dealt_cards_when_name_is_not_literal_hero() -> None:
    hand = parse_hand(_fixture_with_hero_name("student_hero"))

    assert hand["hero"] == {"player": "student_hero", "seat": 3, "position": "BTN"}
    assert hand["hero_hole_cards"] == ["Ah", "Kh"]
    assert next(player for player in hand["players"] if player["player"] == "student_hero")["is_hero"] is True
    assert next(result for result in hand["results"] if result["player"] == "student_hero")["net_bb"] == 28.5
    assert hand["parser_warnings"] == []


def test_cli_parse_accepts_explicit_hero_name_when_private_cards_are_missing(tmp_path: Path) -> None:
    input_path = tmp_path / "renamed_no_private_cards.txt"
    output_path = tmp_path / "canonical.json"
    text = _fixture_with_hero_name("student_hero").replace("Dealt to student_hero [Ah Kh]", "Dealt to student_hero")
    input_path.write_text(text, encoding="utf-8")

    exit_code = main(["parse", str(input_path), "--hero-name", "student_hero", "-o", str(output_path)])

    assert exit_code == 0
    parsed = json.loads(output_path.read_text(encoding="utf-8"))
    assert parsed["hero"] == {"player": "student_hero", "seat": 3, "position": "BTN"}
    assert "Hero hole cards were not found." in parsed["parser_warnings"]


def test_parse_actions_normalizes_raise_and_bb_amounts() -> None:
    hand = parse_hand(FIXTURE.read_text(encoding="utf-8"))

    raise_action = next(action for action in hand["actions"] if action["action_type"] == "raise")
    assert raise_action["player"] == "b2222222"
    assert raise_action["amount"] == 0.35
    assert raise_action["amount_bb"] == 3.5
    assert raise_action["raise_amount"] == 0.25
    assert raise_action["to_amount"] == 0.35

    big_blind_call = next(
        action
        for action in hand["actions"]
        if action["player"] == "d4444444" and action["street"] == "preflop" and action["action_type"] == "call"
    )
    assert big_blind_call["amount"] == 0.25
    assert big_blind_call["facing_amount_bb"] == 2.5

    hero_turn_bet = next(
        action
        for action in hand["actions"]
        if action["player"] == "Hero" and action["street"] == "turn" and action["action_type"] == "bet"
    )
    assert hero_turn_bet["pot_before_bb"] == 25
    assert hero_turn_bet["amount_bb"] == 16


def test_parse_results_use_observed_accounting_not_ev() -> None:
    hand = parse_hand(FIXTURE.read_text(encoding="utf-8"))
    results = {result["player"]: result for result in hand["results"]}

    assert results["Hero"]["contributed"] == 2.65
    assert results["Hero"]["collected"] == 5.5
    assert results["Hero"]["net"] == pytest.approx(2.85)
    assert results["Hero"]["net_bb"] == 28.5
    assert results["b2222222"]["net_bb"] == -26.5


def test_parse_multiple_hands() -> None:
    text = FIXTURE.read_text(encoding="utf-8")

    hands = parse_hands(text + "\n\n" + text.replace("HD1000000001", "HD1000000002"))

    assert [hand["hand_id"] for hand in hands] == ["HD1000000001", "HD1000000002"]


def test_cli_writes_canonical_json(tmp_path: Path) -> None:
    output = tmp_path / "canonical.json"

    exit_code = main(["parse", str(FIXTURE), "-o", str(output), "--pretty"])

    assert exit_code == 0
    parsed = json.loads(output.read_text(encoding="utf-8"))
    assert parsed["hand_id"] == "HD1000000001"
    assert parsed["source"]["imported_from"] == "manual_export"


def test_parse_rejects_unknown_header() -> None:
    with pytest.raises(PokerCraftParseError):
        parse_hand("Not a PokerCraft hand\nSeat 1: Hero ($1 in chips)")


def _fixture_with_hero_name(hero_name: str) -> str:
    return FIXTURE.read_text(encoding="utf-8").replace("Hero", hero_name)
