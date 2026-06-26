# H2N4 Baseline Package

## Purpose

The H2N4 baseline package is the evidence bundle required before any analytical feature can move from `implemented_provisional` to `h2n4_validated`.

This package proves that the same hand-history sample was processed in H2N4 and exported into normalized files that `poker-training-os` can compare.

## Directory layout

```text
h2n4_baseline_package/
  h2n4_baseline_manifest.json
  h2n4_basic_reports_baseline.csv
  h2n4_position_results_baseline.csv
  h2n4_spot_filter_baseline.csv
  h2n4_action_profit_baseline.csv
```

## Manifest fields

`h2n4_baseline_manifest.json` must include:

- `h2n4_version`
- `export_date`
- `fixture_id`
- `source_hand_history_files`
- `hero_aliases`
- `game_type`
- `stake`
- `currency`
- `timezone`
- `bb_conversion_rule`
- `includes_rake`
- `includes_all_in_ev`
- `raw_label_map`
- `notes`

## Baseline CSV files

- `h2n4_basic_reports_baseline.csv`: normalized basic report rows.
- `h2n4_position_results_baseline.csv`: H2N4 position report rows.
- `h2n4_spot_filter_baseline.csv`: H2N4 custom-filter or smart-report rows with cases/opportunities.
- `h2n4_action_profit_baseline.csv`: H2N4 Action Profit rows.

## Validation

Run package validation before running row-level parity comparisons. Package validation does not prove parity; it only proves that the evidence bundle is structurally usable.

