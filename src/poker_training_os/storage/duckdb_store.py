"""Persist canonical hands into DuckDB base tables using Polars dataframes."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import duckdb
import polars as pl


def write_hands_to_duckdb(hands: list[dict[str, Any]], db_path: str | Path) -> None:
    """Create or replace base tables for canonical hands."""

    db = Path(db_path)
    db.parent.mkdir(parents=True, exist_ok=True)

    hand_rows = [_hand_row(hand) for hand in hands]
    player_rows = [row for hand in hands for row in _player_rows(hand)]
    action_rows = [row for hand in hands for row in _action_rows(hand)]
    result_rows = [row for hand in hands for row in _result_rows(hand)]

    with duckdb.connect(str(db)) as con:
        _write_table(con, "hands", pl.DataFrame(hand_rows))
        _write_table(con, "players", pl.DataFrame(player_rows))
        _write_table(con, "actions", pl.DataFrame(action_rows))
        _write_table(con, "results", pl.DataFrame(result_rows))


def _write_table(con: duckdb.DuckDBPyConnection, table_name: str, frame: pl.DataFrame) -> None:
    rows = frame.to_dicts()
    columns = frame.columns
    schema = ", ".join(f"{_quote(column)} {_duckdb_type([row.get(column) for row in rows])}" for column in columns)
    con.execute(f"DROP TABLE IF EXISTS {_quote(table_name)}")
    con.execute(f"CREATE TABLE {_quote(table_name)} ({schema})")
    if rows:
        placeholders = ", ".join("?" for _ in columns)
        column_sql = ", ".join(_quote(column) for column in columns)
        values = [[row.get(column) for column in columns] for row in rows]
        con.executemany(f"INSERT INTO {_quote(table_name)} ({column_sql}) VALUES ({placeholders})", values)


def _duckdb_type(values: list[Any]) -> str:
    concrete = [value for value in values if value is not None]
    if not concrete:
        return "TEXT"
    if all(isinstance(value, bool) for value in concrete):
        return "BOOLEAN"
    if all(isinstance(value, int) and not isinstance(value, bool) for value in concrete):
        return "BIGINT"
    if all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in concrete):
        return "DOUBLE"
    return "TEXT"


def _quote(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def _hand_row(hand: dict[str, Any]) -> dict[str, Any]:
    game = hand.get("game") or {}
    hero = hand.get("hero") or {}
    source = hand.get("source") or {}
    return {
        "hand_id": hand.get("hand_id"),
        "played_at": hand.get("played_at"),
        "table_type": game.get("table_type"),
        "stake": game.get("stake"),
        "small_blind": game.get("small_blind"),
        "big_blind": game.get("big_blind"),
        "hero_position": hero.get("position"),
        "hero_hole_cards": " ".join(hand.get("hero_hole_cards") or []),
        "source_file": source.get("file"),
    }


def _player_rows(hand: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "hand_id": hand.get("hand_id"),
            "seat": player.get("seat"),
            "player": player.get("player"),
            "position": player.get("position"),
            "starting_stack": player.get("starting_stack"),
            "starting_stack_bb": player.get("starting_stack_bb"),
            "is_hero": player.get("is_hero"),
        }
        for player in hand.get("players", [])
    ]


def _action_rows(hand: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for action in hand.get("actions", []):
        rows.append(
            {
                "hand_id": hand.get("hand_id"),
                "order_index": action.get("order"),
                "street": action.get("street"),
                "player": action.get("player"),
                "action_type": action.get("action_type"),
                "amount": action.get("amount"),
                "amount_bb": action.get("amount_bb"),
                "facing_amount_bb": action.get("facing_amount_bb"),
                "pot_before_bb": action.get("pot_before_bb"),
                "raw_text": action.get("raw_text"),
            }
        )
    return rows


def _result_rows(hand: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "hand_id": hand.get("hand_id"),
            "player": result.get("player"),
            "seat": result.get("seat"),
            "position": result.get("position"),
            "contributed": result.get("contributed"),
            "returned": result.get("returned"),
            "collected": result.get("collected"),
            "net": result.get("net"),
            "net_bb": result.get("net_bb"),
            "raw_summary": result.get("raw_summary"),
        }
        for result in hand.get("results", [])
    ]
