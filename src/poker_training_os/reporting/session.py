"""End-to-end session artifact writer."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from poker_training_os.analysis import build_issue_cards, build_review_queue, mine_loss_spots
from poker_training_os.features import extract_spot_features
from poker_training_os.parity import provisional_items, validated_items
from poker_training_os.reporting.artifacts import write_basic_report_artifacts
from poker_training_os.reports import build_basic_reports


def write_session_artifacts(hands: list[dict[str, Any]], output_dir: str | Path) -> dict[str, Path]:
    """Generate the required v0.1 session artifacts."""

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    basic_reports = build_basic_reports(hands)
    paths = write_basic_report_artifacts(basic_reports, out)
    spot_rows = [row for hand in hands for row in extract_spot_features(hand)]
    loss_map = _flatten_loss_map(mine_loss_spots(spot_rows))
    issue_cards = build_issue_cards(mine_loss_spots(spot_rows))
    review_queue = build_review_queue(issue_cards)
    training_cycle = _training_cycle_update(issue_cards)

    paths["loss_map"] = out / "loss_map.csv"
    _write_csv(paths["loss_map"], loss_map)

    paths["issue_cards"] = out / "issue_cards.json"
    paths["issue_cards"].write_text(json.dumps(issue_cards, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    paths["review_queue"] = out / "review_queue.csv"
    _write_csv(paths["review_queue"], review_queue)

    paths["gto_study_cards"] = out / "gto_study_cards.md"
    paths["gto_study_cards"].write_text(_gto_study_cards(issue_cards), encoding="utf-8")

    paths["training_cycle_update"] = out / "training_cycle_update.json"
    paths["training_cycle_update"].write_text(
        json.dumps(training_cycle, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    paths["session_review"] = out / "session_review.md"
    paths["session_review"].write_text(
        _session_review(basic_reports, issue_cards, review_queue, training_cycle),
        encoding="utf-8",
    )

    return paths


def _flatten_loss_map(mined: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows = []
    for source, spots in mined.items():
        for spot in spots:
            rows.append(
                {
                    "source": source,
                    "spot_key": json.dumps(spot["spot_key"], ensure_ascii=False, sort_keys=True),
                    "sample_count": spot["sample_count"],
                    "total_hand_net_bb": spot["total_hand_net_bb"],
                    "avg_hand_net_bb": spot["avg_hand_net_bb"],
                    "max_5_loss_share": spot["max_5_loss_share"],
                    "reliability_level": spot["reliability_level"],
                    "representative_hands": json.dumps(spot["representative_hands"], ensure_ascii=False),
                    "warning": spot["warning"],
                }
            )
    return rows


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if rows:
        fields = list(rows[0].keys())
    else:
        fields = ["empty"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _gto_study_cards(issue_cards: list[dict[str, Any]]) -> str:
    lines = ["# GTO Study Cards", ""]
    if not issue_cards:
        lines.extend(["No issue cards generated for this session.", ""])
        return "\n".join(lines)
    for card in issue_cards:
        lines.extend(
            [
                f"## {card['issue_name']}",
                "",
                f"- Observation: {card['observation']}",
                f"- Study hint: {card['gto_study_hint']}",
                f"- Review question: {card['review_question']}",
                f"- Reliability: {card['reliability']}",
                "",
            ]
        )
    return "\n".join(lines)


def _training_cycle_update(issue_cards: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "focus_count": len(issue_cards),
        "focus_items": [
            {
                "issue_name": card["issue_name"],
                "next_cycle_metric": card["next_cycle_metric"],
                "reliability": card["reliability"],
            }
            for card in issue_cards
        ],
        "status": "needs_human_review" if issue_cards else "no_issues_generated",
        "parity_status": {
            "overall": "implemented_provisional" if provisional_items() else "h2n4_validated",
            "provisional_item_count": len(provisional_items()),
            "validated_item_count": len(validated_items()),
            "baseline_required": len(provisional_items()) > 0,
        },
    }


def _session_review(
    reports: dict[str, Any],
    issue_cards: list[dict[str, Any]],
    review_queue: list[dict[str, Any]],
    training_cycle: dict[str, Any],
) -> str:
    summary = reports["session_summary"]
    top_issue = issue_cards[0] if issue_cards else None
    lines = [
        "# Session Review",
        "",
        "## Observation",
        "",
        f"- Hands: {summary['hands']}",
        f"- Total profit bb: {summary['total_profit_bb']}",
        f"- BB/100: {summary['bb_per_100']}",
        f"- Issue cards generated: {len(issue_cards)}",
        "- Analytical status: implemented_provisional until same-sample H2N4 baseline comparison passes.",
        "",
        "## Hypothesis",
        "",
    ]
    if top_issue:
        lines.append(f"- Primary candidate: {top_issue['observation']}")
    else:
        lines.append("- No repeated losing spot met the current mining rules.")
    lines.extend(
        [
            "",
            "## Human Verdict",
            "",
            f"- Pending review queue items: {len(review_queue)}",
            "- Default label: unknown",
            "",
            "## Training Action",
            "",
            f"- Cycle status: {training_cycle['status']}",
        ]
    )
    if top_issue:
        lines.append(f"- First study prompt: {top_issue['gto_study_hint']}")
    return "\n".join(lines) + "\n"
