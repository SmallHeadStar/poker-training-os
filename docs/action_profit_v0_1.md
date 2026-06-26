# Simplified Action Profit v0.1

## Principle

This module separates three concepts:

- `hand_net_bb`: full-hand observed result.
- `observed_result`: observed result attached to an action row for filtering and grouping.
- `action_profit_bb`: H2N-style observed result from Hero's stack right before the action to Hero's stack at hand end.
- `decision_incremental_bb`: kept as a compatibility alias for `action_profit_bb` in v0.1.

It must not treat full-hand profit as the EV of one action.

## H2N reference formula

H2N4 Action Profit is the primary target. H2N3 Decision Analysis provides the formula background:

`Action Profit = stack_at_end_of_hand - stack_right_before_action`

Fold action profit is always zero because Hero's stack does not change after folding.

In big blinds, using canonical observed accounting:

`action_profit_bb = hand_net_bb + hero_contributed_before_action_bb`

This remains provisional until compared to H2N4 Action Profit exports on the same hand sample.

## v0.1 rules

| Case | `observed_result` | `action_profit_bb` | Reason |
| --- | --- | --- | --- |
| Hero folds | `0` | `0` | Folding adds no further chips to the pot at that decision. |
| Hero checks | Full-hand observed result | `hand_net_bb + contributed_before_action_bb` | Stack before check is after prior commitments. |
| Hero calls/bets/raises | Full-hand observed result | `hand_net_bb + contributed_before_action_bb` | Action Profit is measured from right before the action. |

## Required count fields

Every action-result row includes:

- `action_opportunity_count`
- `action_taken_count`

In v0.1 these are both `1` for observed Hero decisions. Later phases can add explicit missed-action alternatives.

## Warning

All rows include an attribution warning. `action_profit_bb` is H2N-style observed action result, not solver EV and not proof the action was strategically correct.
