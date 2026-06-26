# H2N4 Parity Status

## Project rule

This project is H2N4-parity-first. A stat, report, filter, or derived analysis can be implemented and unit-tested, but it is not complete until the same hand-history sample has been run through H2N4 and `poker-training-os`, then compared with explicit tolerance.

## Status values

- `not_started`: no implementation yet.
- `implemented_provisional`: implementation and unit tests exist, but no H2N4 baseline comparison has passed.
- `h2n4_validated`: same-sample H2N4 export comparison passed within tolerance.
- `out_of_scope`: intentionally outside this project's post-session personal training boundary.

## Current status

All implemented analytical outputs are currently `implemented_provisional`.

| Area | Item | Status | Missing H2N4 evidence |
| --- | --- | --- | --- |
| Parser | GG PokerCraft canonical JSON and Hero identity attribution | `implemented_provisional` | Same exported HH imported into H2N4 and compared to H2N4 hand/action/result and Hero alias interpretation. |
| Basic reports | hands | `implemented_provisional` | H2N4 same-sample hand count. |
| Basic reports | total_profit_bb | `implemented_provisional` | H2N4 same-sample bb result after rake and all-ins. |
| Basic reports | bb_per_100 | `implemented_provisional` | H2N4 same-sample bb/100. |
| Basic reports | position_results | `implemented_provisional` | H2N4 position report grouped by seat/position. |
| Preflop stats | VPIP | `implemented_provisional` | H2N4 numerator, denominator, and percent. |
| Preflop stats | PFR | `implemented_provisional` | H2N4 numerator, denominator, and percent. |
| Preflop stats | RFI by position | `implemented_provisional` | H2N4 RFI report by position, including opportunity count. |
| Preflop stats | 3Bet | `implemented_provisional` | H2N4 3Bet numerator, denominator, and percent. |
| Preflop stats | Call 3Bet | `implemented_provisional` | H2N4 facing-3bet opportunity and call count. |
| Preflop stats | Fold to 3Bet | `implemented_provisional` | H2N4 facing-3bet opportunity and fold count. |
| Preflop stats | 4Bet | `implemented_provisional` | H2N4 facing-3bet opportunity and 4bet count. |
| Postflop stats | WTSD | `implemented_provisional` | H2N4 Went to Showdown numerator/denominator. |
| Postflop stats | W$SD | `implemented_provisional` | H2N4 Won at Showdown numerator/denominator. |
| Postflop stats | WWSF | `implemented_provisional` | H2N4 Won When Saw Flop numerator/denominator. |
| Spot filters | structured spot features | `implemented_provisional` | H2N4 custom-filter report for matching spot definitions. |
| Action results | simplified action-profit-like rows | `implemented_provisional` | H2N4 action-profit/exported report comparison for same river-call and bet/check spots. |
| Loss miner | loss_map.csv | `implemented_provisional` | H2N4 grouped report exports for the same filters. |
| Issue cards | issue_cards.json | `implemented_provisional` | Depends on validated loss map evidence. |
| Dashboard | Streamlit v0.1 | `implemented_provisional` | Dashboard displays provisional values only. |

## Baseline files needed

Place normalized H2N4 exports next to our generated outputs when available:

- `h2n4_basic_reports_baseline.csv`
- `h2n4_position_results_baseline.csv`
- `h2n4_spot_filter_baseline.csv`
- `h2n4_action_profit_baseline.csv`

The existing comparator currently supports the `basic_reports.csv` shape. Additional comparator shapes should be added before marking filters or action-profit-like reports as validated.
