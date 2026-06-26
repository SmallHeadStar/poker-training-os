import csv
import json

from poker_training_os.reporting import write_basic_report_artifacts
from poker_training_os.reports import build_basic_reports


def test_write_basic_report_artifacts(tmp_path) -> None:
    reports = build_basic_reports(
        [
            {
                "hero": {"player": "Hero", "position": "BTN"},
                "actions": [{"order": 1, "street": "preflop", "player": "Hero", "action_type": "raise"}],
                "board": {"flop": [], "turn": [], "river": [], "full": []},
                "showdown": [],
                "results": [{"player": "Hero", "net_bb": 4}],
            }
        ]
    )

    paths = write_basic_report_artifacts(reports, tmp_path)

    summary = json.loads(paths["session_summary"].read_text(encoding="utf-8"))
    rows = list(csv.DictReader(paths["basic_reports"].open(encoding="utf-8", newline="")))
    vpip_row = next(row for row in rows if row["section"] == "preflop" and row["metric"] == "vpip")

    assert summary == {"hands": 1, "total_profit_bb": 4, "bb_per_100": 400}
    assert vpip_row["numerator"] == "1"
    assert vpip_row["denominator"] == "1"
    assert vpip_row["percent"] == "100"
    assert any(row["metric"] == "rfi" and row["position"] == "BTN" for row in rows)
