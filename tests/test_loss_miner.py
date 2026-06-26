from poker_training_os.analysis import mine_loss_spots


def test_mine_loss_spots_outputs_required_fields() -> None:
    rows = [
        _row("H1", "BTN", "single_raised_pot", "hero_flat_vs_open", "check-bet", "king_high_rainbow_unpaired", "call", -20),
        _row("H2", "BTN", "single_raised_pot", "hero_flat_vs_open", "check-bet", "king_high_rainbow_unpaired", "call", -10),
        _row("H3", "BTN", "single_raised_pot", "hero_flat_vs_open", "check-bet", "king_high_rainbow_unpaired", "call", 5),
        _row("H4", "BB", "three_bet_pot", "hero_3bet", "bet", "ace_high_two_tone_unpaired", "bet", 15),
    ]

    mined = mine_loss_spots(rows, limit=3)
    position = mined["top_loss_positions"][0]

    assert position == {
        "source": "top_loss_positions",
        "spot_key": {"hero_position": "BTN"},
        "sample_count": 3,
        "total_hand_net_bb": -25,
        "avg_hand_net_bb": -8.3333,
        "max_5_loss_share": 1,
        "reliability_level": "low",
        "representative_hands": ["H1", "H2", "H3"],
        "warning": "sample_too_small; loss_concentrated_in_top_5",
    }


def test_mine_loss_spots_marks_high_reliability_when_sample_is_large_and_distributed() -> None:
    rows = [
        _row(f"H{i}", "CO", "single_raised_pot", "hero_open", "none", "preflop", "raise", -1)
        for i in range(60)
    ]

    mined = mine_loss_spots(rows)
    spot = mined["top_loss_positions"][0]

    assert spot["sample_count"] == 60
    assert spot["total_hand_net_bb"] == -60
    assert spot["max_5_loss_share"] == 0.0833
    assert spot["reliability_level"] == "high"
    assert spot["warning"] is None


def _row(
    hand_id: str,
    hero_position: str,
    pot_type: str,
    preflop_line: str,
    action_line_before: str,
    board_family: str,
    hero_decision: str,
    hand_net_bb: float,
) -> dict:
    return {
        "hand_id": hand_id,
        "hero_position": hero_position,
        "pot_type": pot_type,
        "preflop_line": preflop_line,
        "action_line_before": action_line_before,
        "board_family": board_family,
        "hero_decision": hero_decision,
        "hand_net_bb": hand_net_bb,
    }
