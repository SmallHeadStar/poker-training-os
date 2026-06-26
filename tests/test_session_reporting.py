import csv
import json
from pathlib import Path

from poker_training_os.parsers.gg_pokercraft import parse_hand
from poker_training_os.reporting import write_session_artifacts


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "gg_pokercraft_cash_hand.txt"


def test_write_session_artifacts_outputs_required_files(tmp_path) -> None:
    hand = parse_hand(FIXTURE.read_text(encoding="utf-8"))

    paths = write_session_artifacts([hand], tmp_path)

    assert set(paths) == {
        "session_summary",
        "basic_reports",
        "loss_map",
        "issue_cards",
        "review_queue",
        "gto_study_cards",
        "training_cycle_update",
        "session_review",
    }
    assert all(path.exists() for path in paths.values())
    summary = json.loads(paths["session_summary"].read_text(encoding="utf-8"))
    review = paths["session_review"].read_text(encoding="utf-8")

    assert summary["hands"] == 1
    assert "## Observation" in review
    assert "## Hypothesis" in review
    assert "## Human Verdict" in review
    assert "## Training Action" in review
    assert "implemented_provisional" in review


def test_review_queue_csv_has_unknown_human_label(tmp_path) -> None:
    losing_hand = parse_hand(FIXTURE.read_text(encoding="utf-8").replace("Hero collected $5.50 from pot", "b2222222 collected $5.50 from pot"))
    paths = write_session_artifacts([losing_hand], tmp_path)
    rows = list(csv.DictReader(paths["review_queue"].open(encoding="utf-8", newline="")))

    assert rows
    assert {row["human_label"] for row in rows} == {"unknown"}


def test_training_cycle_marks_outputs_as_provisional(tmp_path) -> None:
    hand = parse_hand(FIXTURE.read_text(encoding="utf-8"))
    paths = write_session_artifacts([hand], tmp_path)

    training_cycle = json.loads(paths["training_cycle_update"].read_text(encoding="utf-8"))

    assert training_cycle["parity_status"]["overall"] == "implemented_provisional"
    assert training_cycle["parity_status"]["baseline_required"] is True
    assert training_cycle["parity_status"]["provisional_item_count"] > 0
