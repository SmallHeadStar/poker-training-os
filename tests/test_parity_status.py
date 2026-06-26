from poker_training_os.parity import PARITY_REGISTRY, provisional_items, validated_items


EXPECTED_PARITY_ITEMS = {
    ("parser", "gg_pokercraft_canonical_json"),
    ("basic_reports", "hands"),
    ("basic_reports", "total_profit_bb"),
    ("basic_reports", "bb_per_100"),
    ("basic_reports", "position_results"),
    ("preflop", "vpip"),
    ("preflop", "pfr"),
    ("preflop", "rfi_by_position"),
    ("preflop", "three_bet"),
    ("preflop", "call_3bet"),
    ("preflop", "fold_to_3bet"),
    ("preflop", "four_bet"),
    ("postflop", "wtsd"),
    ("postflop", "w_sd"),
    ("postflop", "wwsf"),
    ("spot_filters", "structured_spot_features"),
    ("action_results", "simplified_action_profit_like"),
    ("loss_miner", "loss_map"),
    ("issue_cards", "issue_cards"),
    ("dashboard", "streamlit_v0_1"),
}


def test_all_current_analytical_items_are_provisional_until_h2n4_baseline_exists() -> None:
    assert PARITY_REGISTRY
    assert validated_items() == []
    assert len(provisional_items()) == len(PARITY_REGISTRY)


def test_parity_registry_names_core_h2n4_targets() -> None:
    item_names = {(item.area, item.item) for item in PARITY_REGISTRY}

    assert item_names == EXPECTED_PARITY_ITEMS
