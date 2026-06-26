"""Machine-readable H2N4 parity status."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ParityItem:
    area: str
    item: str
    status: str
    required_evidence: str


PARITY_REGISTRY: tuple[ParityItem, ...] = (
    ParityItem("parser", "gg_pokercraft_canonical_json", "implemented_provisional", "same-sample H2N4 import interpretation"),
    ParityItem("basic_reports", "hands", "implemented_provisional", "H2N4 hand count"),
    ParityItem("basic_reports", "total_profit_bb", "implemented_provisional", "H2N4 total bb result"),
    ParityItem("basic_reports", "bb_per_100", "implemented_provisional", "H2N4 bb/100"),
    ParityItem("basic_reports", "position_results", "implemented_provisional", "H2N4 position report"),
    ParityItem("preflop", "vpip", "implemented_provisional", "H2N4 numerator denominator percent"),
    ParityItem("preflop", "pfr", "implemented_provisional", "H2N4 numerator denominator percent"),
    ParityItem("preflop", "rfi_by_position", "implemented_provisional", "H2N4 RFI by position opportunities"),
    ParityItem("preflop", "three_bet", "implemented_provisional", "H2N4 3Bet opportunities"),
    ParityItem("preflop", "call_3bet", "implemented_provisional", "H2N4 call 3Bet opportunities"),
    ParityItem("preflop", "fold_to_3bet", "implemented_provisional", "H2N4 fold to 3Bet opportunities"),
    ParityItem("preflop", "four_bet", "implemented_provisional", "H2N4 4Bet opportunities"),
    ParityItem("postflop", "wtsd", "implemented_provisional", "H2N4 Went to Showdown"),
    ParityItem("postflop", "w_sd", "implemented_provisional", "H2N4 Won at Showdown"),
    ParityItem("postflop", "wwsf", "implemented_provisional", "H2N4 Won When Saw Flop"),
    ParityItem("spot_filters", "structured_spot_features", "implemented_provisional", "H2N4 custom filter report"),
    ParityItem("action_results", "simplified_action_profit_like", "implemented_provisional", "H2N4 action profit export"),
    ParityItem("loss_miner", "loss_map", "implemented_provisional", "H2N4 grouped report exports"),
    ParityItem("issue_cards", "issue_cards", "implemented_provisional", "validated loss map evidence"),
    ParityItem("dashboard", "streamlit_v0_1", "implemented_provisional", "dashboard displays validated or provisional status"),
)


def provisional_items() -> list[ParityItem]:
    return [item for item in PARITY_REGISTRY if item.status == "implemented_provisional"]


def validated_items() -> list[ParityItem]:
    return [item for item in PARITY_REGISTRY if item.status == "h2n4_validated"]

