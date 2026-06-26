# poker-training-os

Local, post-session poker analysis for a single player's exported GG PokerCraft hand histories.

The project is inspired by the information architecture of professional poker trackers, but it is not a Hand2Note clone, HUD, real-time assistant, opponent database, screen reader, or automation tool. Its purpose is a personal training loop:

1. Import manually exported hand histories.
2. Normalize them into a canonical hand model.
3. Store and query analysis tables locally.
4. Generate reports, spot features, simplified action-result views, issue cards, review queues, and study prompts.
5. Produce session review artifacts and a compact Streamlit dashboard for after-session work.

## Current phase

H2N4-parity-first provisional implementation: parser, base reports, spot features, action-result-like rows, session artifacts, and a compact dashboard exist, but analytical outputs remain provisional until same-sample H2N4 baseline exports pass comparison.

## Tooling

- Python
- DuckDB
- Polars
- pytest
- Streamlit
- Markdown / CSV / JSON outputs

pandas may be used only as a compatibility layer, not as the core computation engine.

## First parser target

The parser starts with GG PokerCraft NLHE cash / Rush & Cash style text exports and emits the canonical hand model described in `docs/data_contracts.md`.

## H2N4 parity rule

Unit tests are necessary but not sufficient. Every stat, filter, report, and derived output remains provisional until the same hand-history sample is processed in H2N4 and `poker-training-os`, then compared with explicit tolerance. See `docs/parity_status.md` and `docs/h2n4_parity_validation.md`.

## Local run

See `docs/local_run.md` for CLI and Streamlit commands.
