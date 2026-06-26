"""Build issue cards and review queue rows from mined spots."""

from __future__ import annotations

from typing import Any


ALLOWED_REVIEW_LABELS = (
    "confirmed_error",
    "acceptable_play",
    "cooler",
    "sample_noise",
    "villain_specific",
    "tilt_related",
    "need_gto_review",
    "unknown",
)


def build_issue_cards(mined_spots: dict[str, list[dict[str, Any]]], limit: int = 10) -> list[dict[str, Any]]:
    """Convert mined loss spots into reviewable issue cards."""

    candidates = [
        spot
        for source, spots in mined_spots.items()
        for spot in spots
        if source == "top_loss_combined_spots" or spot.get("reliability_level") != "low"
    ]
    candidates = sorted(candidates, key=lambda spot: (spot["total_hand_net_bb"], -spot["sample_count"]))[:limit]
    return [_issue_card(index + 1, spot) for index, spot in enumerate(candidates)]


def build_review_queue(issue_cards: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Create one review queue row per representative hand."""

    rows = []
    for card in issue_cards:
        for hand_id in card["representative_hands"]:
            rows.append(
                {
                    "hand_id": hand_id,
                    "issue_name": card["issue_name"],
                    "source": card["source"],
                    "reliability": card["reliability"],
                    "human_label": "unknown",
                    "review_status": "pending",
                    "notes": "",
                }
            )
    return rows


def _issue_card(index: int, spot: dict[str, Any]) -> dict[str, Any]:
    spot_key = spot.get("spot_key") or {}
    title = _issue_name(index, spot)
    evidence = {
        "sample_count": spot["sample_count"],
        "total_hand_net_bb": spot["total_hand_net_bb"],
        "avg_hand_net_bb": spot["avg_hand_net_bb"],
        "max_5_loss_share": spot["max_5_loss_share"],
        "warning": spot["warning"],
    }
    return {
        "issue_name": title,
        "observation": (
            f"{_spot_text(spot_key)} shows {spot['total_hand_net_bb']} bb over "
            f"{spot['sample_count']} observed decisions."
        ),
        "evidence": evidence,
        "common_pattern": spot_key,
        "representative_hands": spot["representative_hands"],
        "review_question": _review_question(spot_key),
        "gto_study_hint": _gto_hint(spot_key),
        "next_cycle_metric": _next_cycle_metric(spot),
        "source": spot["source"],
        "reliability": spot["reliability_level"],
    }


def _issue_name(index: int, spot: dict[str, Any]) -> str:
    key = spot.get("spot_key") or {}
    primary = key.get("preflop_line") or key.get("pot_type") or key.get("hero_position") or spot["source"]
    decision = key.get("hero_decision")
    suffix = f" / {decision}" if decision else ""
    return f"Issue {index}: {primary}{suffix}"


def _spot_text(spot_key: dict[str, Any]) -> str:
    parts = [f"{field}={value}" for field, value in spot_key.items() if value not in (None, "preflop")]
    return ", ".join(parts) if parts else "This spot"


def _review_question(spot_key: dict[str, Any]) -> str:
    decision = spot_key.get("hero_decision")
    line = spot_key.get("preflop_line") or "this line"
    if decision:
        return f"When {line} reaches this spot, is Hero's {decision} supported by range, sizing, and opponent context?"
    return f"Is the loss in {line} caused by strategy, runout, opponent pool, or sample noise?"


def _gto_hint(spot_key: dict[str, Any]) -> str:
    line = spot_key.get("preflop_line") or "spot"
    board = spot_key.get("board_family")
    if board and board != "preflop":
        return f"Review solver strategy for {line} on {board} boards with the same action line."
    return f"Review baseline ranges and frequencies for {line}."


def _next_cycle_metric(spot: dict[str, Any]) -> dict[str, Any]:
    return {
        "source": spot["source"],
        "target": "reduce_or_explain_observed_loss",
        "baseline_total_hand_net_bb": spot["total_hand_net_bb"],
        "baseline_sample_count": spot["sample_count"],
    }

