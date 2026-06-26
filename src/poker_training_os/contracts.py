"""Executable project contracts for the early phases."""

from __future__ import annotations

from dataclasses import dataclass


PRODUCT_BOUNDARIES: tuple[str, ...] = (
    "post_session_only",
    "manual_exported_hand_histories_only",
    "no_realtime_hud",
    "no_running_client_reading",
    "no_screen_recognition",
    "no_automatic_actions",
    "no_live_table_advice",
    "no_shared_opponent_database",
    "not_full_h2n4_clone",
)

REQUIRED_PHASE0_DOCS: tuple[str, ...] = (
    "docs/product_positioning.md",
    "docs/h2n4_parity_checklist.md",
    "docs/mvp_scope.md",
    "docs/data_contracts.md",
    "docs/reporting_contract.md",
    "docs/dashboard_v0_1.md",
)

CANONICAL_HAND_REQUIRED_FIELDS: tuple[str, ...] = (
    "schema_version",
    "source",
    "hand_id",
    "played_at",
    "game",
    "hero",
    "players",
    "hero_hole_cards",
    "actions",
    "board",
    "showdown",
    "results",
    "parser_warnings",
)


@dataclass(frozen=True)
class ReportingArtifact:
    """A required output file and the kind of information it carries."""

    filename: str
    format: str
    purpose: str


REPORTING_ARTIFACTS: tuple[ReportingArtifact, ...] = (
    ReportingArtifact("session_review.md", "markdown", "human session review"),
    ReportingArtifact("session_summary.json", "json", "session metadata and KPIs"),
    ReportingArtifact("basic_reports.csv", "csv", "basic report tables"),
    ReportingArtifact("loss_map.csv", "csv", "loss spot summaries"),
    ReportingArtifact("issue_cards.json", "json", "structured issue cards"),
    ReportingArtifact("review_queue.csv", "csv", "hands and spots for human labeling"),
    ReportingArtifact("gto_study_cards.md", "markdown", "study prompts"),
    ReportingArtifact("training_cycle_update.json", "json", "next-cycle training focus"),
)


def missing_required_fields(hand: dict[str, object]) -> list[str]:
    """Return canonical hand fields absent from a parsed hand record."""

    return [field for field in CANONICAL_HAND_REQUIRED_FIELDS if field not in hand]

