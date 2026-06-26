from poker_training_os.analysis import build_action_result_rows, summarize_action_results


def test_fold_result_is_zero_not_hand_loss() -> None:
    hand = _hand(
        actions=[
            _action(1, "preflop", "Hero", "post_blind", amount_bb=1),
            _action(2, "preflop", "CO", "raise", amount_bb=3, facing_amount_bb=0, pot_before_bb=1.5),
            _action(3, "preflop", "Hero", "fold", facing_amount_bb=2, pot_before_bb=4.5),
        ],
        net_bb=-1,
    )

    row = build_action_result_rows(hand)[0]

    assert row["hero_decision"] == "fold"
    assert row["observed_result"] == 0
    assert row["action_profit_bb"] == 0
    assert row["decision_incremental_bb"] == 0
    assert row["incremental_basis"] == "fold_action_profit_zero"


def test_action_profit_uses_h2n_stack_before_action_formula() -> None:
    hand = _hand(
        actions=[
            _action(1, "preflop", "Hero", "raise", amount_bb=3),
            _action(2, "preflop", "BB", "call", amount_bb=2),
            _action(3, "flop", "Hero", "bet", amount_bb=4, pot_before_bb=6),
            _action(4, "flop", "BB", "call", amount_bb=4, pot_before_bb=10),
            _action(5, "turn", "Hero", "check", pot_before_bb=14),
            _action(6, "turn", "BB", "check", pot_before_bb=14),
            _action(7, "river", "BB", "bet", amount_bb=20, pot_before_bb=14),
            _action(8, "river", "Hero", "call", amount_bb=20, facing_amount_bb=20, pot_before_bb=34),
        ],
        net_bb=53,
    )

    rows = build_action_result_rows(hand)
    flop_bet = rows[1]
    river_call = rows[-1]

    assert flop_bet["street"] == "flop"
    assert flop_bet["hero_decision"] == "bet"
    assert flop_bet["action_profit_bb"] == 56
    assert flop_bet["incremental_basis"] == "h2n_action_profit_formula_provisional"
    assert river_call["street"] == "river"
    assert river_call["hero_decision"] == "call"
    assert river_call["hand_net_bb"] == 53
    assert river_call["action_profit_bb"] == 60
    assert river_call["decision_incremental_bb"] == 60
    assert river_call["incremental_basis"] == "h2n_action_profit_formula_provisional"


def test_action_profit_uses_canonical_hero_name() -> None:
    hand = _hand(
        actions=[
            _action(1, "preflop", "student_hero", "raise", amount_bb=3),
            _action(2, "preflop", "BB", "call", amount_bb=2),
            _action(3, "flop", "BB", "check", pot_before_bb=6),
            _action(4, "flop", "student_hero", "bet", amount_bb=4, pot_before_bb=6),
        ],
        net_bb=12,
        hero_name="student_hero",
    )

    rows = build_action_result_rows(hand)

    assert [row["hero_decision"] for row in rows] == ["raise", "bet"]
    assert rows[1]["action_profit_bb"] == 15


def test_summarize_action_results_keeps_incremental_separate() -> None:
    rows = [
        {"street": "river", "hero_decision": "call", "observed_result": 53, "decision_incremental_bb": 60, "action_opportunity_count": 1, "action_taken_count": 1},
        {"street": "river", "hero_decision": "fold", "observed_result": 0, "decision_incremental_bb": 0, "action_opportunity_count": 1, "action_taken_count": 1},
        {"street": "turn", "hero_decision": "bet", "observed_result": -10, "decision_incremental_bb": None, "action_opportunity_count": 1, "action_taken_count": 1},
    ]

    summary = summarize_action_results(rows, ["street", "hero_decision"])

    assert summary == [
        {"street": "river", "hero_decision": "call", "action_opportunity_count": 1, "action_taken_count": 1, "total_observed_result": 53, "avg_observed_result": 53, "incremental_count": 1, "total_decision_incremental_bb": 60, "avg_decision_incremental_bb": 60},
        {"street": "river", "hero_decision": "fold", "action_opportunity_count": 1, "action_taken_count": 1, "total_observed_result": 0, "avg_observed_result": 0, "incremental_count": 1, "total_decision_incremental_bb": 0, "avg_decision_incremental_bb": 0},
        {"street": "turn", "hero_decision": "bet", "action_opportunity_count": 1, "action_taken_count": 1, "total_observed_result": -10, "avg_observed_result": -10, "incremental_count": 0, "total_decision_incremental_bb": None, "avg_decision_incremental_bb": None},
    ]


def _hand(actions: list[dict], net_bb: float, hero_name: str = "Hero") -> dict:
    return {
        "hand_id": "H1",
        "hero": {"player": hero_name, "position": "BTN"},
        "players": [
            {"player": hero_name, "position": "BTN"},
            {"player": "BB", "position": "BB"},
            {"player": "CO", "position": "CO"},
        ],
        "hero_hole_cards": ["Ah", "Kh"],
        "actions": actions,
        "board": {"flop": ["Kc", "7d", "2s"], "turn": ["4h"], "river": ["9c"], "full": ["Kc", "7d", "2s", "4h", "9c"]},
        "showdown": [{"player": hero_name}],
        "results": [{"player": hero_name, "net_bb": net_bb}],
    }


def _action(
    order: int,
    street: str,
    player: str,
    action_type: str,
    *,
    amount_bb: float | None = None,
    facing_amount_bb: float | None = None,
    pot_before_bb: float | None = None,
) -> dict:
    return {
        "order": order,
        "street": street,
        "player": player,
        "action_type": action_type,
        "amount_bb": amount_bb,
        "facing_amount_bb": facing_amount_bb,
        "pot_before_bb": pot_before_bb,
    }
