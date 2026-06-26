from poker_training_os.analysis import ALLOWED_REVIEW_LABELS, build_issue_cards, build_review_queue


def test_build_issue_cards_from_mined_spots() -> None:
    mined = {
        "top_loss_combined_spots": [
            {
                "source": "top_loss_combined_spots",
                "spot_key": {
                    "hero_position": "BTN",
                    "pot_type": "single_raised_pot",
                    "preflop_line": "hero_flat_vs_open",
                    "board_family": "king_high_rainbow_unpaired",
                    "hero_decision": "call",
                },
                "sample_count": 12,
                "total_hand_net_bb": -45,
                "avg_hand_net_bb": -3.75,
                "max_5_loss_share": 0.62,
                "reliability_level": "medium",
                "representative_hands": ["H1", "H2"],
                "warning": "loss_somewhat_concentrated",
            }
        ],
        "top_loss_positions": [],
    }

    cards = build_issue_cards(mined)

    assert len(cards) == 1
    card = cards[0]
    assert card["issue_name"] == "Issue 1: hero_flat_vs_open / call"
    assert "shows -45 bb over 12 observed decisions" in card["observation"]
    assert card["evidence"]["sample_count"] == 12
    assert card["representative_hands"] == ["H1", "H2"]
    assert card["source"] == "top_loss_combined_spots"
    assert card["reliability"] == "medium"
    assert card["next_cycle_metric"]["target"] == "reduce_or_explain_observed_loss"


def test_build_review_queue_defaults_to_unknown_label() -> None:
    cards = [
        {
            "issue_name": "Issue 1: hero_flat_vs_open / call",
            "source": "top_loss_combined_spots",
            "reliability": "medium",
            "representative_hands": ["H1", "H2"],
        }
    ]

    queue = build_review_queue(cards)

    assert "unknown" in ALLOWED_REVIEW_LABELS
    assert queue == [
        {
            "hand_id": "H1",
            "issue_name": "Issue 1: hero_flat_vs_open / call",
            "source": "top_loss_combined_spots",
            "reliability": "medium",
            "human_label": "unknown",
            "review_status": "pending",
            "notes": "",
        },
        {
            "hand_id": "H2",
            "issue_name": "Issue 1: hero_flat_vs_open / call",
            "source": "top_loss_combined_spots",
            "reliability": "medium",
            "human_label": "unknown",
            "review_status": "pending",
            "notes": "",
        },
    ]

