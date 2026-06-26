import json

from poker_training_os.dashboard import load_session_dashboard


def test_load_session_dashboard_reports_missing_files(tmp_path) -> None:
    dashboard = load_session_dashboard(tmp_path)

    assert "session_review.md" in dashboard["missing_files"]
    assert dashboard["session_summary"] == {}
    assert dashboard["basic_reports"] == []


def test_load_session_dashboard_reads_artifacts(tmp_path) -> None:
    (tmp_path / "session_review.md").write_text("# Review\n", encoding="utf-8")
    (tmp_path / "session_summary.json").write_text(json.dumps({"hands": 3}), encoding="utf-8")
    (tmp_path / "basic_reports.csv").write_text("section,metric,value\nsession,hands,3\n", encoding="utf-8")
    (tmp_path / "loss_map.csv").write_text("source,sample_count\ntop_loss_positions,2\n", encoding="utf-8")
    (tmp_path / "issue_cards.json").write_text(json.dumps([{"issue_name": "Issue 1"}]), encoding="utf-8")
    (tmp_path / "review_queue.csv").write_text("hand_id,human_label\nH1,unknown\n", encoding="utf-8")
    (tmp_path / "gto_study_cards.md").write_text("# Study\n", encoding="utf-8")
    (tmp_path / "training_cycle_update.json").write_text(json.dumps({"status": "needs_human_review"}), encoding="utf-8")

    dashboard = load_session_dashboard(tmp_path)

    assert dashboard["missing_files"] == []
    assert dashboard["session_summary"] == {"hands": 3}
    assert dashboard["basic_reports"] == [{"section": "session", "metric": "hands", "value": "3"}]
    assert dashboard["issue_cards"] == [{"issue_name": "Issue 1"}]
    assert dashboard["review_queue"] == [{"hand_id": "H1", "human_label": "unknown"}]

