"""Writers for session reporting artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


BASIC_REPORT_FIELDS = [
    "section",
    "metric",
    "position",
    "value",
    "numerator",
    "denominator",
    "percent",
    "hands",
    "total_profit_bb",
    "bb_per_100",
]


def write_basic_report_artifacts(reports: dict[str, Any], output_dir: str | Path) -> dict[str, Path]:
    """Write the Phase 2 report artifacts currently supported."""

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    session_summary_path = out / "session_summary.json"
    basic_reports_path = out / "basic_reports.csv"

    session_summary_path.write_text(
        json.dumps(reports["session_summary"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    with basic_reports_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=BASIC_REPORT_FIELDS)
        writer.writeheader()
        writer.writerows(_basic_report_rows(reports))

    return {
        "session_summary": session_summary_path,
        "basic_reports": basic_reports_path,
    }


def _basic_report_rows(reports: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    summary = reports["session_summary"]
    rows.extend(
        [
            _row("session", "hands", value=summary["hands"]),
            _row("session", "total_profit_bb", value=summary["total_profit_bb"]),
            _row("session", "bb_per_100", value=summary["bb_per_100"]),
        ]
    )

    for row in reports.get("position_results", []):
        rows.append(
            _row(
                "position_results",
                "net_result",
                position=row["position"],
                hands=row["hands"],
                total_profit_bb=row["total_profit_bb"],
                bb_per_100=row["bb_per_100"],
            )
        )

    for metric, value in reports.get("preflop", {}).items():
        if metric == "rfi_by_position":
            for rfi_row in value:
                rows.append(_frequency_row("preflop", "rfi", rfi_row, position=rfi_row["position"]))
        else:
            rows.append(_frequency_row("preflop", metric, value))

    for metric, value in reports.get("showdown", {}).items():
        rows.append(_frequency_row("showdown", metric, value))

    return rows


def _frequency_row(section: str, metric: str, value: dict[str, Any], position: str | None = None) -> dict[str, Any]:
    return _row(
        section,
        metric,
        position=position,
        numerator=value["numerator"],
        denominator=value["denominator"],
        percent=value["percent"],
    )


def _row(
    section: str,
    metric: str,
    *,
    position: str | None = None,
    value: Any = None,
    numerator: Any = None,
    denominator: Any = None,
    percent: Any = None,
    hands: Any = None,
    total_profit_bb: Any = None,
    bb_per_100: Any = None,
) -> dict[str, Any]:
    return {
        "section": section,
        "metric": metric,
        "position": position,
        "value": value,
        "numerator": numerator,
        "denominator": denominator,
        "percent": percent,
        "hands": hands,
        "total_profit_bb": total_profit_bb,
        "bb_per_100": bb_per_100,
    }

