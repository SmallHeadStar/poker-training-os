# H2N4 Parity Validation

## Why this exists

Unit tests prove our formulas behave as written. They do not prove that our numbers match Hand2Note. For stat accuracy, the required acceptance test is differential validation against H2N4 on the same hand sample.

No implemented analytical output may be called complete until this validation passes.

## Required validation loop

1. Prepare a fixed GG PokerCraft hand-history sample.
2. Import the same sample into H2N4.
3. Export or record the relevant H2N4 report values.
4. Assemble and validate the H2N4 baseline package described in `docs/h2n4_baseline_package.md`.
5. Import the sample into `poker-training-os`.
6. Generate our `session_summary.json` and `basic_reports.csv`.
7. Normalize the H2N4 output into `h2n4_basic_reports_baseline.csv`.
8. Run the parity comparator.
9. Investigate every mismatch before claiming metric parity.

## Baseline CSV contract

The H2N4 baseline comparison file should use the same columns as our `basic_reports.csv` where possible:

| Column | Meaning |
| --- | --- |
| `section` | Report area, for example `preflop`, `showdown`, or `position_results`. |
| `metric` | Normalized metric id, for example `vpip`, `pfr`, `three_bet`, `wtsd`, `w_sd`, or `wwsf`. |
| `position` | Position for grouped rows, otherwise blank. |
| `value` | Scalar value for non-frequency metrics when applicable. |
| `numerator` | Hit count for frequency stats. |
| `denominator` | Opportunity count for frequency stats. |
| `percent` | Frequency percent. |
| `hands` | Hand count for grouped rows. |
| `total_profit_bb` | Observed total result in big blinds. |
| `bb_per_100` | Observed bb/100. |

If H2N4 exports labels such as `3Bet`, `W$SD`, or `Fold to 3Bet`, normalize them into our metric ids before comparison.

## Required export metadata

Every H2N4 baseline package should include:

- H2N4 version/build.
- Export date.
- Original GG PokerCraft files or stable fixture id.
- Hero alias mapping.
- Game type, stake, currency, and timezone assumptions.
- BB conversion rule.
- Whether rake, all-in EV, jackpot, insurance, or special GG result fields are included.
- H2N raw report labels before normalization.
- Normalized metric ids used by this project.

## Comparison tolerance

Default numeric tolerance is `0.01`, which allows rounding differences but not formula differences. Counts should match exactly.

Required comparison fields:

- numerator
- denominator
- cases
- opportunities
- percent
- bb/100
- total bb result
- position results
- grouped report rows

## Action Profit baseline fields

`h2n4_action_profit_baseline.csv` should include:

- `filter_id`
- `filter_definition`
- `street`
- `hero_action`
- `hand_category`
- `cases`
- `opportunities`
- `total_action_profit_bb`
- `avg_action_profit_bb`
- `amount_won`
- `amount_won_bb`
- `next_villain_fold_count`
- `next_villain_call_count`
- `next_villain_raise_count`
- `h2n_raw_label`

## Required edge-case sample coverage

Basic report baselines should include hands for:

- Hero open raises and later faces a 3bet, then folds.
- Hero open raises and later faces a 3bet, then calls.
- Hero open raises and later faces a 3bet, then 4bets.
- Limper before Hero, Hero iso-raises, then faces a 3bet.
- RFI opportunities by each position.
- BB check or walk-like preflop cases.
- Squeeze and multi-raise preflop cases.
- Mucked showdown or summary-only showdown.
- Split pot or chopped pot.
- Saw-flop hands won without showdown.

## Mismatch categories

Every mismatch should be classified as one of:

- `parser_gap`: the canonical hand model missed or misread source data.
- `formula_gap`: our numerator or denominator differs from H2N4's stat logic.
- `normalization_gap`: labels, positions, stakes, or units were mapped incorrectly.
- `known_scope_limit`: H2N4 supports a case intentionally outside our MVP.
- `bug`: implementation is wrong and must be fixed.

## Current status

The repository currently has unit and golden tests plus a comparator harness only. It is not H2N4-parity certified because no real H2N4 export baseline has been provided.

See `docs/parity_status.md` for the machine-aligned status list.
