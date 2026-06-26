from pathlib import Path

import duckdb

from poker_training_os.parsers.gg_pokercraft import parse_hand
from poker_training_os.storage import write_hands_to_duckdb


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "gg_pokercraft_cash_hand.txt"


def test_write_hands_to_duckdb_base_tables(tmp_path) -> None:
    hand = parse_hand(FIXTURE.read_text(encoding="utf-8"), source_name=str(FIXTURE))
    db_path = tmp_path / "poker_training.duckdb"

    write_hands_to_duckdb([hand], db_path)

    with duckdb.connect(str(db_path)) as con:
        hand_count = con.execute("select count(*) from hands").fetchone()[0]
        player_count = con.execute("select count(*) from players").fetchone()[0]
        hero_net = con.execute("select net_bb from results where player = 'Hero'").fetchone()[0]
        hero_call_count = con.execute(
            "select count(*) from actions where player = 'Hero' and action_type = 'call'"
        ).fetchone()[0]

    assert hand_count == 1
    assert player_count == 6
    assert hero_net == 28.5
    assert hero_call_count == 2

