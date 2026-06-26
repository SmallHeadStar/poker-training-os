from pathlib import Path

from poker_training_os.features import extract_spot_features
from poker_training_os.filters import filter_rows, group_rows
from poker_training_os.parsers.gg_pokercraft import parse_hand


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "gg_pokercraft_cash_hand.txt"


def test_extract_spot_features_from_fixture() -> None:
    hand = parse_hand(FIXTURE.read_text(encoding="utf-8"))

    rows = extract_spot_features(hand)

    assert [row["street"] for row in rows] == ["preflop", "flop", "turn", "river"]
    assert [row["hero_decision"] for row in rows] == ["call", "call", "bet", "check"]
    assert all(row["preflop_line"] == "hero_flat_vs_open" for row in rows)
    assert all(row["hand_net_bb"] == 28.5 for row in rows)


def test_extract_spot_features_uses_canonical_hero_name() -> None:
    hand = parse_hand(FIXTURE.read_text(encoding="utf-8").replace("Hero", "student_hero"))

    rows = extract_spot_features(hand)

    assert [row["hero_decision"] for row in rows] == ["call", "call", "bet", "check"]
    assert rows[1]["position_combo"] == "BTN_vs_CO"
    assert rows[1]["hero_ip_oop"] == "ip"
    assert all(row["hand_net_bb"] == 28.5 for row in rows)


def test_preflop_spot_feature_fields() -> None:
    hand = parse_hand(FIXTURE.read_text(encoding="utf-8"))
    preflop = extract_spot_features(hand)[0]

    assert preflop["pot_type"] == "single_raised_pot"
    assert preflop["player_count_context"] == "multiway"
    assert preflop["position_combo"] == "BTN_vs_CO"
    assert preflop["hero_ip_oop"] == "unknown"
    assert preflop["hero_hand_group"] == "suited_ace"
    assert preflop["made_hand_class"] == "preflop"
    assert preflop["draw_class"] == "preflop"
    assert preflop["facing_bet_size_bucket"] == "preflop_2_6_to_4bb"


def test_postflop_spot_feature_fields() -> None:
    hand = parse_hand(FIXTURE.read_text(encoding="utf-8"))
    flop = extract_spot_features(hand)[1]

    assert flop["street"] == "flop"
    assert flop["pot_type"] == "single_raised_pot"
    assert flop["position_combo"] == "BTN_vs_CO"
    assert flop["hero_ip_oop"] == "ip"
    assert flop["made_hand_class"] == "pair_or_better"
    assert flop["draw_class"] == "backdoor_or_none"
    assert flop["board_family"] == "king_high_rainbow_unpaired"
    assert flop["action_line_before"] == "check-bet"
    assert flop["facing_bet_size_bucket"] == "postflop_34_to_66pct_pot"


def test_filter_and_group_spot_rows() -> None:
    hand = parse_hand(FIXTURE.read_text(encoding="utf-8"))
    rows = extract_spot_features(hand)

    postflop = filter_rows(rows, street={"flop", "turn", "river"})
    grouped = group_rows(postflop, ["street", "hero_decision"])

    assert grouped == [
        {"street": "flop", "hero_decision": "call", "sample_count": 1, "total_hand_net_bb": 28.5, "avg_hand_net_bb": 28.5},
        {"street": "river", "hero_decision": "check", "sample_count": 1, "total_hand_net_bb": 28.5, "avg_hand_net_bb": 28.5},
        {"street": "turn", "hero_decision": "bet", "sample_count": 1, "total_hand_net_bb": 28.5, "avg_hand_net_bb": 28.5},
    ]
