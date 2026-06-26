import csv
import json

from poker_training_os.cli import main
from poker_training_os.validation import validate_h2n4_baseline_package
from poker_training_os.validation.baseline_package import BASELINE_SCHEMAS, MANIFEST_FILENAME


def test_validate_h2n4_baseline_package_reports_missing_everything(tmp_path) -> None:
    result = validate_h2n4_baseline_package(tmp_path)

    assert result["status"] == "fail"
    assert result["manifest"]["missing"] is True
    assert result["artifacts"]["h2n4_basic_reports_baseline.csv"]["missing"] is True
    assert result["parity_note"] == "schema_valid_only_not_h2n4_parity"


def test_validate_h2n4_baseline_package_requires_manifest_metadata(tmp_path) -> None:
    (tmp_path / MANIFEST_FILENAME).write_text(json.dumps({"h2n4_version": "4.x"}), encoding="utf-8")

    result = validate_h2n4_baseline_package(tmp_path)

    assert result["status"] == "fail"
    assert "fixture_id" in result["manifest"]["missing_fields"]
    assert "raw_label_map" in result["manifest"]["missing_fields"]


def test_validate_h2n4_baseline_package_requires_csv_columns(tmp_path) -> None:
    _write_complete_manifest(tmp_path)
    _write_csv(tmp_path / "h2n4_basic_reports_baseline.csv", ["section", "metric", "position"])

    result = validate_h2n4_baseline_package(tmp_path)

    assert result["status"] == "fail"
    assert "numerator" in result["artifacts"]["h2n4_basic_reports_baseline.csv"]["missing_columns"]


def test_validate_h2n4_baseline_package_passes_when_schema_is_complete(tmp_path) -> None:
    _write_complete_manifest(tmp_path)
    for filename, fields in BASELINE_SCHEMAS.items():
        _write_csv(tmp_path / filename, list(fields))

    result = validate_h2n4_baseline_package(tmp_path)

    assert result["status"] == "pass"
    assert result["manifest"]["missing_fields"] == []
    assert all(artifact["missing_columns"] == [] for artifact in result["artifacts"].values())


def test_cli_validate_h2n4_package_writes_result_and_returns_failure_for_missing_package(tmp_path) -> None:
    output = tmp_path / "result.json"

    exit_code = main(["validate-h2n4-package", str(tmp_path / "missing-package"), "-o", str(output)])

    result = json.loads(output.read_text(encoding="utf-8"))
    assert exit_code == 1
    assert result["status"] == "fail"
    assert result["parity_note"] == "schema_valid_only_not_h2n4_parity"


def _write_complete_manifest(root) -> None:
    payload = {
        "h2n4_version": "4.x",
        "export_date": "2026-06-26",
        "fixture_id": "fixture-demo",
        "source_hand_history_files": ["GG20260626-0001 - Hold'em.txt"],
        "hero_aliases": ["Hero"],
        "game_type": "NLHE cash",
        "stake": "$0.05/$0.10",
        "currency": "USD",
        "timezone": "unknown",
        "bb_conversion_rule": "use hand big blind",
        "includes_rake": True,
        "includes_all_in_ev": False,
        "raw_label_map": {"VPIP": "vpip"},
        "notes": "test manifest",
    }
    (root / MANIFEST_FILENAME).write_text(json.dumps(payload), encoding="utf-8")


def _write_csv(path, fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
