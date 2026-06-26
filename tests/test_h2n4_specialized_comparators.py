import csv

from poker_training_os.validation import (
    compare_action_profit_csv,
    compare_position_results_csv,
    compare_spot_filter_csv,
)


def test_compare_position_results_csv_uses_exact_hands_and_tolerant_bb_values(tmp_path) -> None:
    ours = tmp_path / "position_ours.csv"
    baseline = tmp_path / "position_h2n4.csv"
    _write_csv(
        ours,
        ["position", "hands", "amount_won", "amount_won_bb", "bb_per_100"],
        [{"position": "BTN", "hands": "12", "amount_won": "3.50", "amount_won_bb": "35", "bb_per_100": "291.67"}],
    )
    _write_csv(
        baseline,
        ["position", "hands", "amount_won", "amount_won_bb", "bb_per_100"],
        [{"position": "BTN", "hands": "12", "amount_won": "3.504", "amount_won_bb": "35.004", "bb_per_100": "291.674"}],
    )

    result = compare_position_results_csv(ours, baseline)

    assert result["status"] == "pass"
    assert result["comparison_type"] == "position_results"


def test_compare_position_results_csv_fails_exact_hand_count(tmp_path) -> None:
    ours = tmp_path / "position_ours.csv"
    baseline = tmp_path / "position_h2n4.csv"
    fields = ["position", "hands", "amount_won", "amount_won_bb", "bb_per_100"]
    _write_csv(ours, fields, [{"position": "BB", "hands": "10", "amount_won": "-1", "amount_won_bb": "-10", "bb_per_100": "-100"}])
    _write_csv(baseline, fields, [{"position": "BB", "hands": "10.004", "amount_won": "-1", "amount_won_bb": "-10", "bb_per_100": "-100"}])

    result = compare_position_results_csv(ours, baseline)

    assert result["status"] == "fail"
    assert result["mismatches"][0]["field"] == "hands"


def test_compare_spot_filter_csv_detects_missing_group_rows(tmp_path) -> None:
    ours = tmp_path / "spot_ours.csv"
    baseline = tmp_path / "spot_h2n4.csv"
    fields = [
        "filter_id",
        "street",
        "action_line",
        "hero_ip_oop",
        "player_count_context",
        "facing_bet_size_bucket",
        "cases",
        "opportunities",
        "amount_won",
        "amount_won_bb",
    ]
    _write_csv(
        ours,
        fields,
        [_spot_row("F1", "flop", "check-bet", "ip", "heads_up", "postflop_34_to_66pct_pot", cases="3")],
    )
    _write_csv(
        baseline,
        fields,
        [_spot_row("F2", "turn", "bet-call", "oop", "multiway", "postflop_67_to_110pct_pot", cases="2")],
    )

    result = compare_spot_filter_csv(ours, baseline)

    assert result["status"] == "fail"
    assert result["missing_in_ours"][0]["filter_id"] == "F2"
    assert result["missing_in_baseline"][0]["filter_id"] == "F1"


def test_compare_action_profit_csv_requires_exact_cases_and_next_action_counts(tmp_path) -> None:
    ours = tmp_path / "ap_ours.csv"
    baseline = tmp_path / "ap_h2n4.csv"
    fields = [
        "filter_id",
        "street",
        "hero_action",
        "hand_category",
        "cases",
        "opportunities",
        "total_action_profit_bb",
        "avg_action_profit_bb",
        "amount_won",
        "amount_won_bb",
        "next_villain_fold_count",
        "next_villain_call_count",
        "next_villain_raise_count",
    ]
    _write_csv(ours, fields, [_ap_row(next_villain_call_count="4")])
    _write_csv(baseline, fields, [_ap_row(next_villain_call_count="5")])

    result = compare_action_profit_csv(ours, baseline)

    assert result["status"] == "fail"
    assert result["mismatches"] == [
        {
            "filter_id": "AP1",
            "street": "river",
            "hero_action": "call",
            "hand_category": "top_pair",
            "field": "next_villain_call_count",
            "ours": "4",
            "baseline": "5",
            "difference": -1.0,
        }
    ]


def test_compare_action_profit_csv_accepts_rounding_tolerance_for_profit(tmp_path) -> None:
    ours = tmp_path / "ap_ours.csv"
    baseline = tmp_path / "ap_h2n4.csv"
    fields = [
        "filter_id",
        "street",
        "hero_action",
        "hand_category",
        "cases",
        "opportunities",
        "total_action_profit_bb",
        "avg_action_profit_bb",
        "amount_won",
        "amount_won_bb",
        "next_villain_fold_count",
        "next_villain_call_count",
        "next_villain_raise_count",
    ]
    _write_csv(ours, fields, [_ap_row(total_action_profit_bb="12.00", avg_action_profit_bb="4.00")])
    _write_csv(baseline, fields, [_ap_row(total_action_profit_bb="12.004", avg_action_profit_bb="4.004")])

    result = compare_action_profit_csv(ours, baseline)

    assert result["status"] == "pass"


def _spot_row(
    filter_id: str,
    street: str,
    action_line: str,
    hero_ip_oop: str,
    player_count_context: str,
    facing_bet_size_bucket: str,
    *,
    cases: str,
) -> dict[str, str]:
    return {
        "filter_id": filter_id,
        "street": street,
        "action_line": action_line,
        "hero_ip_oop": hero_ip_oop,
        "player_count_context": player_count_context,
        "facing_bet_size_bucket": facing_bet_size_bucket,
        "cases": cases,
        "opportunities": "10",
        "amount_won": "-2.50",
        "amount_won_bb": "-25",
    }


def _ap_row(
    *,
    total_action_profit_bb: str = "12",
    avg_action_profit_bb: str = "4",
    next_villain_call_count: str = "4",
) -> dict[str, str]:
    return {
        "filter_id": "AP1",
        "street": "river",
        "hero_action": "call",
        "hand_category": "top_pair",
        "cases": "3",
        "opportunities": "3",
        "total_action_profit_bb": total_action_profit_bb,
        "avg_action_profit_bb": avg_action_profit_bb,
        "amount_won": "1.20",
        "amount_won_bb": "12",
        "next_villain_fold_count": "0",
        "next_villain_call_count": next_villain_call_count,
        "next_villain_raise_count": "0",
    }


def _write_csv(path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})

