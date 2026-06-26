import csv

from poker_training_os.validation import compare_report_csv


FIELDS = [
    "section",
    "metric",
    "position",
    "value",
    "numerator",
    "denominator",
    "cases",
    "opportunities",
    "percent",
    "hands",
    "total_profit_bb",
    "bb_per_100",
]


def test_compare_report_csv_passes_with_rounding_tolerance(tmp_path) -> None:
    ours = tmp_path / "ours.csv"
    baseline = tmp_path / "h2n4.csv"
    rows = [
        {
            "section": "preflop",
            "metric": "vpip",
            "position": "",
            "numerator": "10",
            "denominator": "20",
            "percent": "50",
        }
    ]
    _write_csv(ours, rows)
    _write_csv(baseline, [{**rows[0], "percent": "50.004"}])

    result = compare_report_csv(ours, baseline)

    assert result["status"] == "pass"
    assert result["compared_rows"] == 1
    assert result["mismatches"] == []


def test_compare_report_csv_requires_exact_counts(tmp_path) -> None:
    ours = tmp_path / "ours.csv"
    baseline = tmp_path / "h2n4.csv"
    _write_csv(
        ours,
        [{"section": "preflop", "metric": "vpip", "position": "", "numerator": "10", "denominator": "20"}],
    )
    _write_csv(
        baseline,
        [{"section": "preflop", "metric": "vpip", "position": "", "numerator": "10.004", "denominator": "20"}],
    )

    result = compare_report_csv(ours, baseline)

    assert result["status"] == "fail"
    assert result["mismatches"][0]["field"] == "numerator"
    assert result["mismatches"][0]["difference"] == -0.004


def test_compare_report_csv_reports_formula_mismatches(tmp_path) -> None:
    ours = tmp_path / "ours.csv"
    baseline = tmp_path / "h2n4.csv"
    _write_csv(
        ours,
        [{"section": "preflop", "metric": "three_bet", "position": "", "numerator": "3", "denominator": "10"}],
    )
    _write_csv(
        baseline,
        [{"section": "preflop", "metric": "three_bet", "position": "", "numerator": "2", "denominator": "10"}],
    )

    result = compare_report_csv(ours, baseline)

    assert result["status"] == "fail"
    assert result["mismatches"] == [
        {
            "section": "preflop",
            "metric": "three_bet",
            "position": "",
            "field": "numerator",
            "ours": "3",
            "baseline": "2",
            "difference": 1.0,
        }
    ]


def test_compare_report_csv_reports_missing_rows(tmp_path) -> None:
    ours = tmp_path / "ours.csv"
    baseline = tmp_path / "h2n4.csv"
    _write_csv(ours, [{"section": "preflop", "metric": "vpip", "position": "", "percent": "40"}])
    _write_csv(baseline, [{"section": "showdown", "metric": "wtsd", "position": "", "percent": "30"}])

    result = compare_report_csv(ours, baseline)

    assert result["status"] == "fail"
    assert result["missing_in_ours"] == [{"section": "showdown", "metric": "wtsd", "position": ""}]
    assert result["missing_in_baseline"] == [{"section": "preflop", "metric": "vpip", "position": ""}]


def test_compare_report_csv_rejects_missing_required_columns(tmp_path) -> None:
    ours = tmp_path / "ours.csv"
    baseline = tmp_path / "h2n4.csv"
    ours.write_text("section,metric,position,percent\npreflop,vpip,,40\n", encoding="utf-8")
    _write_csv(baseline, [{"section": "preflop", "metric": "vpip", "position": "", "percent": "40"}])

    try:
        compare_report_csv(ours, baseline)
    except ValueError as error:
        assert "missing required columns" in str(error)
    else:
        raise AssertionError("Expected missing-column ValueError")


def test_compare_report_csv_rejects_duplicate_keys(tmp_path) -> None:
    ours = tmp_path / "ours.csv"
    baseline = tmp_path / "h2n4.csv"
    _write_csv(
        ours,
        [
            {"section": "preflop", "metric": "vpip", "position": "", "percent": "40"},
            {"section": "preflop", "metric": "vpip", "position": "", "percent": "41"},
        ],
    )
    _write_csv(baseline, [{"section": "preflop", "metric": "vpip", "position": "", "percent": "40"}])

    try:
        compare_report_csv(ours, baseline)
    except ValueError as error:
        assert "duplicate comparison keys" in str(error)
    else:
        raise AssertionError("Expected duplicate-key ValueError")


def _write_csv(path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in FIELDS})
