from pathlib import Path

from poker_training_os.contracts import (
    CANONICAL_HAND_REQUIRED_FIELDS,
    PRODUCT_BOUNDARIES,
    REPORTING_ARTIFACTS,
    REQUIRED_PHASE0_DOCS,
    missing_required_fields,
)


ROOT = Path(__file__).resolve().parents[1]


def test_phase0_required_docs_exist() -> None:
    missing = [doc for doc in REQUIRED_PHASE0_DOCS if not (ROOT / doc).exists()]

    assert missing == []


def test_product_boundaries_encode_safety_scope() -> None:
    assert "post_session_only" in PRODUCT_BOUNDARIES
    assert "manual_exported_hand_histories_only" in PRODUCT_BOUNDARIES
    assert "no_realtime_hud" in PRODUCT_BOUNDARIES
    assert "no_live_table_advice" in PRODUCT_BOUNDARIES
    assert "no_shared_opponent_database" in PRODUCT_BOUNDARIES


def test_reporting_contract_contains_all_required_artifacts() -> None:
    filenames = {artifact.filename for artifact in REPORTING_ARTIFACTS}

    assert filenames == {
        "session_review.md",
        "session_summary.json",
        "basic_reports.csv",
        "loss_map.csv",
        "issue_cards.json",
        "review_queue.csv",
        "gto_study_cards.md",
        "training_cycle_update.json",
    }


def test_canonical_hand_contract_has_required_parser_outputs() -> None:
    assert set(CANONICAL_HAND_REQUIRED_FIELDS) >= {
        "hand_id",
        "played_at",
        "game",
        "hero_hole_cards",
        "players",
        "actions",
        "board",
        "showdown",
        "results",
    }


def test_missing_required_fields_reports_absent_fields() -> None:
    complete_hand = {field: None for field in CANONICAL_HAND_REQUIRED_FIELDS}

    assert missing_required_fields(complete_hand) == []
    assert missing_required_fields({"hand_id": "1"}) == [
        field for field in CANONICAL_HAND_REQUIRED_FIELDS if field != "hand_id"
    ]

