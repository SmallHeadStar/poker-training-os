"""Command-line helpers for local artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from poker_training_os.parsers.gg_pokercraft import parse_hands_from_file
from poker_training_os.pipeline import run_session_import
from poker_training_os.reporting import write_basic_report_artifacts, write_session_artifacts
from poker_training_os.reports import build_basic_reports
from poker_training_os.validation import compare_report_csv, validate_h2n4_baseline_package


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="poker-training-os")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parse_parser = subparsers.add_parser("parse", help="Parse GG PokerCraft text to canonical JSON")
    parse_parser.add_argument("input", type=Path, help="Path to a manually exported hand-history text file")
    parse_parser.add_argument("-o", "--output", type=Path, help="Path to write canonical JSON")
    parse_parser.add_argument("--pretty", action="store_true", help="Write indented JSON for review")
    parse_parser.add_argument("--hero-name", help="Optional exact Hero screen name when it cannot be inferred")

    import_parser = subparsers.add_parser(
        "import-session",
        help="Parse GG PokerCraft text and write canonical JSON, DuckDB, and session artifacts",
    )
    import_parser.add_argument("input", type=Path, help="Path to a manually exported hand-history text file")
    import_parser.add_argument("output_dir", type=Path, help="Directory for generated local artifacts")
    import_parser.add_argument("--hero-name", help="Optional exact Hero screen name when it cannot be inferred")

    report_parser = subparsers.add_parser("report-basic", help="Write basic report artifacts from canonical JSON")
    report_parser.add_argument("canonical_json", type=Path, help="Path to one canonical hand or a list of hands")
    report_parser.add_argument("output_dir", type=Path, help="Directory for session_summary.json and basic_reports.csv")

    session_parser = subparsers.add_parser("report-session", help="Write all v0.1 session artifacts")
    session_parser.add_argument("canonical_json", type=Path, help="Path to one canonical hand or a list of hands")
    session_parser.add_argument("output_dir", type=Path, help="Directory for session artifacts")

    parity_parser = subparsers.add_parser("validate-h2n4", help="Compare our basic_reports.csv with H2N4 baseline CSV")
    parity_parser.add_argument("ours_csv", type=Path, help="Path to our basic_reports.csv")
    parity_parser.add_argument("h2n4_baseline_csv", type=Path, help="Path to normalized H2N4 baseline CSV")
    parity_parser.add_argument("-o", "--output", type=Path, help="Optional JSON file for comparison result")
    parity_parser.add_argument("--tolerance", type=float, default=0.01, help="Numeric tolerance for rounded values")

    package_parser = subparsers.add_parser(
        "validate-h2n4-package",
        help="Validate H2N4 baseline package metadata and CSV schemas",
    )
    package_parser.add_argument("package_dir", type=Path, help="Directory containing H2N4 baseline package files")
    package_parser.add_argument("-o", "--output", type=Path, help="Optional JSON file for validation result")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "parse":
        hands = parse_hands_from_file(args.input, hero_name=args.hero_name)
        payload: object = hands[0] if len(hands) == 1 else hands
        text = json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text + "\n", encoding="utf-8")
        else:
            print(text)
        return 0

    if args.command == "import-session":
        result = run_session_import(args.input, args.output_dir, hero_name=args.hero_name)
        printable = {
            **result,
            "canonical_hands": str(result["canonical_hands"]),
            "duckdb": str(result["duckdb"]),
            "artifacts": {key: str(value) for key, value in result["artifacts"].items()},
        }
        print(json.dumps(printable, ensure_ascii=False, indent=2))
        return 0

    if args.command == "report-basic":
        payload = json.loads(args.canonical_json.read_text(encoding="utf-8"))
        hands = payload if isinstance(payload, list) else [payload]
        reports = build_basic_reports(hands)
        write_basic_report_artifacts(reports, args.output_dir)
        return 0

    if args.command == "report-session":
        payload = json.loads(args.canonical_json.read_text(encoding="utf-8"))
        hands = payload if isinstance(payload, list) else [payload]
        write_session_artifacts(hands, args.output_dir)
        return 0

    if args.command == "validate-h2n4":
        result = compare_report_csv(args.ours_csv, args.h2n4_baseline_csv, tolerance=args.tolerance)
        text = json.dumps(result, ensure_ascii=False, indent=2)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text + "\n", encoding="utf-8")
        else:
            print(text)
        return 0 if result["status"] == "pass" else 1

    if args.command == "validate-h2n4-package":
        result = validate_h2n4_baseline_package(args.package_dir)
        text = json.dumps(result, ensure_ascii=False, indent=2)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text + "\n", encoding="utf-8")
        else:
            print(text)
        return 0 if result["status"] == "pass" else 1

    parser.error(f"Unknown command: {args.command}")
    return 2
