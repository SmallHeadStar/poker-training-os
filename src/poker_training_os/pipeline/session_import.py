"""Import raw PokerCraft hands and generate local training artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from poker_training_os.parsers.gg_pokercraft import parse_hands_from_file
from poker_training_os.reporting import write_session_artifacts
from poker_training_os.storage import write_hands_to_duckdb


def run_session_import(
    hand_history_path: str | Path,
    output_dir: str | Path,
    *,
    db_filename: str = "poker_training.duckdb",
    hero_name: str | None = None,
) -> dict[str, Any]:
    """Parse a manually exported hand-history file and write local artifacts.

    This is post-session only. The input must be a user-exported hand-history file,
    never a running poker client, screen capture, or live table source.
    """

    input_path = Path(hand_history_path)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    hands = parse_hands_from_file(input_path, hero_name=hero_name)
    canonical_path = out / "canonical_hands.json"
    canonical_path.write_text(json.dumps(hands, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    db_path = out / db_filename
    write_hands_to_duckdb(hands, db_path)
    artifact_paths = write_session_artifacts(hands, out)

    return {
        "status": "ok",
        "input_file": str(input_path),
        "output_dir": str(out),
        "hand_count": len(hands),
        "canonical_hands": canonical_path,
        "duckdb": db_path,
        "artifacts": artifact_paths,
        "parity_status": "implemented_provisional",
        "parity_note": "H2N4-like outputs require same-sample H2N4 baseline comparison before validation.",
    }
