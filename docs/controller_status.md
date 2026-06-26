# Controller Status

## Source of truth

`PRODUCT.md` is the highest-priority product definition and acceptance standard. `AGENTS.md` controls controller/subagent workflow.

The original goal's technical stack, phase route, output files, and UI requirements remain active only when they do not conflict with `PRODUCT.md`.

## Current controller decision

Do not expand later-phase feature breadth until the core H2N4 parity questions in parser, stats, and filter semantics are addressed.

## Feature status table

| Area | Current status | Reason | Next gating evidence |
| --- | --- | --- | --- |
| Product boundaries | complete | Post-session-only, user-exported-HH-only, no HUD/live/client/screen/opponent DB boundaries are documented. | Keep enforced in future feature docs and UI copy. |
| H2N4 parity policy | complete | `PRODUCT.md`, `docs/parity_status.md`, and comparator tests enforce provisional status without baseline. | Maintain as features evolve. |
| GG PokerCraft parser | provisional | Synthetic-style fixture and unit tests exist, including explicit/inferred Hero screen-name handling, but real anonymized GG exports and H2N4 parser comparison are missing. | Real fixture snapshots plus H2N4 same-sample hand/action/result baseline. |
| Canonical model | provisional | Required top-level fields exist and `hero.player` is now the downstream identity source, but side pots, split pots, all-ins, multiple runouts, tournament summaries, and stack-before/after are incomplete. | Expanded data contract and real fixture coverage. |
| DuckDB base tables | provisional | Base tables write and query, but schema is not validated against real H2N4-equivalent workflows. | H2N4 baseline-driven parser/model validation. |
| Basic stats and reports | provisional | Unit tests cover intended numerator/denominator behavior, but H2N4 same-sample baseline is absent. | `h2n4_basic_reports_baseline.csv` and position report comparison. |
| Spot filters/features | provisional | Exact-match feature rows exist, but H2N4 custom-filter opportunity semantics are not validated. | `h2n4_spot_filter_baseline.csv` with filter definitions and opportunity counts. |
| Action-profit-like analysis | provisional | Uses H2N-style formula background, but H2N4 Action Profit exports are not compared. | `h2n4_action_profit_baseline.csv`. |
| Loss miner and issue cards | provisional | Built on provisional upstream spot/result data. | Validated loss/filter reports. |
| Session artifacts | provisional | Files generate and include provisional warnings. | Upstream parser/report/filter parity evidence. |
| Streamlit dashboard | provisional | Displays generated artifacts and provisional status; UI should not expand before core parity. | Stable validated artifacts. |

## Immediate next phase

1. Collect or create anonymized real GG PokerCraft fixture batch.
2. Import the same batch into H2N4.
3. Export normalized H2N4 baselines for basic reports, position results, spot filters, and Action Profit.
4. Harden parser/canonical model against fixture mismatches.
5. Harden stats and filters only where baseline differences prove a gap.

## Blocked items

No analytical feature can move from `provisional` to `complete` until H2N4 same-sample baseline evidence exists.
