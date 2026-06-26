# Auto Spot Miner v0.1

## Purpose

The miner finds repeated losing contexts from structured spot features. It helps the user discover training candidates without manually defining every filter.

## Required output fields

Each mined spot includes:

- `source`
- `spot_key`
- `sample_count`
- `total_hand_net_bb`
- `avg_hand_net_bb`
- `max_5_loss_share`
- `reliability_level`
- `representative_hands`
- `warning`

## v0.1 dimensions

- `hero_position`
- `pot_type`
- `preflop_line`
- `action_line_before`
- `board_family`
- Combined: `hero_position + pot_type + preflop_line + board_family + hero_decision`

## Reliability rules

- `low`: fewer than 10 samples, or the five largest losing hands explain more than 80% of the total loss.
- `medium`: fewer than 50 samples, or the five largest losing hands explain more than 50% of the total loss.
- `high`: at least 50 samples and losses are not strongly concentrated.

## Interpretation warning

The miner uses `hand_net_bb` as an observed loss signal. This is useful for triage, but it does not prove a specific action was wrong.

