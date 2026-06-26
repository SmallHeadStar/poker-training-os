import json
from pathlib import Path

import duckdb

from poker_training_os.cli import main
from poker_training_os.pipeline import run_session_import


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "gg_pokercraft_cash_hand.txt"


def test_run_session_import_writes_canonical_db_and_artifacts(tmp_path) -> None:
    result = run_session_import(FIXTURE, tmp_path)

    assert result["status"] == "ok"
    assert result["hand_count"] == 1
    assert result["parity_status"] == "implemented_provisional"
    assert result["canonical_hands"].exists()
    assert result["duckdb"].exists()
    assert (tmp_path / "session_summary.json").exists()
    assert (tmp_path / "loss_map.csv").exists()

    canonical = json.loads(result["canonical_hands"].read_text(encoding="utf-8"))
    assert canonical[0]["hand_id"] == "HD1000000001"

    with duckdb.connect(str(result["duckdb"])) as con:
        assert con.execute("select count(*) from hands").fetchone()[0] == 1
        assert con.execute("select count(*) from actions where player = 'Hero'").fetchone()[0] > 0


def test_run_session_import_keeps_real_hero_name_for_reports_and_db(tmp_path) -> None:
    input_path = tmp_path / "renamed_session.txt"
    output_dir = tmp_path / "out"
    input_path.write_text(FIXTURE.read_text(encoding="utf-8").replace("Hero", "student_hero"), encoding="utf-8")

    result = run_session_import(input_path, output_dir)

    canonical = json.loads(result["canonical_hands"].read_text(encoding="utf-8"))
    summary = json.loads((output_dir / "session_summary.json").read_text(encoding="utf-8"))
    assert canonical[0]["hero"]["player"] == "student_hero"
    assert summary["hands"] == 1
    assert summary["total_profit_bb"] == 28.5

    with duckdb.connect(str(result["duckdb"])) as con:
        assert con.execute("select count(*) from actions where player = 'student_hero'").fetchone()[0] > 0


def test_cli_import_session_runs_end_to_end(tmp_path, capsys) -> None:
    exit_code = main(["import-session", str(FIXTURE), str(tmp_path)])
    captured = capsys.readouterr()

    payload = json.loads(captured.out)
    assert exit_code == 0
    assert payload["hand_count"] == 1
    assert payload["parity_status"] == "implemented_provisional"
    assert Path(payload["canonical_hands"]).exists()
    assert Path(payload["artifacts"]["session_review"]).exists()
