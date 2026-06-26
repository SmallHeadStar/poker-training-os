# Stats Dictionary

All Phase 2 stats are Hero-centric and computed from canonical hands. They are session-review observations, not live advice and not EV estimates.

## H2N4 alignment notes

The first stat set follows the same broad semantics Hand2Note documents for basic reports:

- VPIP excludes mandatory blinds and antes.
- PFR means preflop raise frequency.
- 3bet means reraising after a preflop raise.
- WTSD, W$SD, and WWSF should be read together, not as isolated truth.
- Filtered reports should expose both hits and opportunities, because a frequency without its denominator is easy to misread.

References used for calibration:

- https://hand2note.com/Blog/Features/key-preflop-stats-player-profiling-and-basic-adjustments
- https://hand2note.com/Blog/Features/essential-postflop-stats
- https://hand2note.com/Help/Features/smart-reports

## Shared conventions

- `hand`: one canonical hand where Hero is seated.
- `hero_result.net_bb`: Hero's observed net result in big blinds for the full hand.
- `preflop voluntary action`: Hero call, bet, or raise before the flop, excluding blinds and antes.
- `preflop raise`: a normalized preflop `raise` action.
- `saw flop`: a flop board exists and Hero did not fold preflop.
- Percent stats return `null` when the denominator is zero.

## Metrics

| Metric | Numerator | Denominator | Sample requirement | Known limitations |
| --- | --- | --- | --- | --- |
| `hands` | Count of canonical hands containing Hero. | Not applicable. | At least 1 hand. | Imported hands must be deduplicated before reporting. |
| `total_profit_bb` | Sum of Hero `net_bb`. | Not applicable. | At least 1 hand with parsed results. | This is full-hand observed profit, not EV. |
| `bb_per_100` | `total_profit_bb * 100`. | Hero hand count. | Prefer 1,000+ hands for interpretation. | Short-session values are noisy. |
| `position_results` | Sum of Hero `net_bb` by Hero position. | Hero hands by position. | Prefer 100+ hands per position. | Position assignment is parser-derived and can be wrong if source seating is unusual. |
| `vpip` | Hands where Hero voluntarily calls, bets, or raises preflop. | Hero hand count. | Prefer 500+ hands. | Does not count forced blinds or antes. |
| `pfr` | Hands where Hero raises preflop. | Hero hand count. | Prefer 500+ hands. | Includes 3bets and 4bets, not only open raises. |
| `rfi_by_position` | Hands where Hero raises first in from that position. | Hero first-action opportunities where no player had voluntarily entered the pot before Hero. | Prefer 100+ opportunities per position. | Limped pots before Hero are excluded from RFI opportunities. |
| `three_bet` | Hands where Hero raises after exactly one prior preflop raise before Hero's first decision. | Hero first-decision opportunities facing exactly one prior raise. | Prefer 100+ opportunities. | Squeeze and multi-raise edge cases are simplified in v0.1. |
| `call_3bet` | Hands where Hero calls after open-raising an unopened pot and facing an opponent 3bet. | Hands where Hero open-raised an unopened pot and later faced a 3bet response. | Prefer 100+ opportunities. | Iso-raise-after-limper spots are excluded in v0.1 until H2N4 baseline confirms the correct bucket. |
| `fold_to_3bet` | Hands where Hero folds after open-raising an unopened pot and facing an opponent 3bet. | Hands where Hero open-raised an unopened pot and later faced a 3bet response. | Prefer 100+ opportunities. | Does not infer missing actions from summary text. |
| `four_bet` | Hands where Hero raises after open-raising an unopened pot and facing an opponent 3bet. | Hands where Hero open-raised an unopened pot and later faced a 3bet response. | Prefer 100+ opportunities. | Treated as observed frequency, not quality. |
| `wtsd` | Hands where Hero saw flop and showed down. | Hands where Hero saw flop. | Prefer 500+ saw-flop hands. | v0.1 requires Hero to appear in showdown reveals. |
| `w_sd` | Showdown hands where Hero's observed full-hand net is positive. | Hands where Hero showed down. | Prefer 200+ showdown hands. | Approximation of W$SD using observed Hero net; splits and rake can make interpretation subtle. |
| `wwsf` | Hands where Hero saw flop and won positive observed net. | Hands where Hero saw flop. | Prefer 500+ saw-flop hands. | Measures observed result, not whether Hero won the pot uncontested before showdown. |

## Attribution warning

These stats may aggregate `hand_net_bb`, but they must not label one action as the cause of that whole-hand result. Decision-level attribution belongs to the later simplified action-profit phase.
