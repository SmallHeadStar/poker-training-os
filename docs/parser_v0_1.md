# Parser v0.1

## Scope

The first parser targets manually exported GG PokerCraft No-Limit Hold'em hand-history text.

Supported in v0.1:

- Cash hand headers such as `Poker Hand #HD...`.
- Rush & Cash hand headers such as `Poker Hand #RC...`.
- Basic tournament headers such as `Poker Hand #TM...`.
- Table, button, seat, stack, and approximate position assignment.
- Hero identity from an explicit import option, or inferred from the `Dealt to <player> [cards]` private-card line.
- Hero hole cards.
- Preflop, flop, turn, river, showdown, and summary sections.
- Folds, checks, calls, bets, raises, blinds, antes, shows, collected pots, and returned uncalled bets.
- Board cards.
- Per-player observed contribution, collection, returned amount, and net result.

## Output rule

The parser returns canonical JSON. Analysis code must consume this normalized object, not raw hand-history text.

## Known limitations

- Current fixtures are synthetic PokerCraft-style samples. Real anonymized GG exports are still required before H2N4 parser parity can be claimed.
- Hero name inference assumes the export exposes exactly one private-card `Dealt to ... [cards]` line for the user, or the user supplies the exact Hero screen name at import time.
- Position assignment is derived from occupied seats and button seat. It is suitable for reports, but unusual table mechanics may need review.
- `amount` on a raise is normalized to the chips newly committed by the action. The original raise size and final street wager are preserved as `raise_amount` and `to_amount`.
- Net results are observed accounting results from parsed actions and collection lines. They are not EV.
- Parser timestamps are emitted as local naive ISO-8601 strings because the exported text examples do not always include a timezone.
- Unsupported or unexpected lines are kept as parser warnings.
- Side pots, split pots, multiway all-ins, multiple runouts, and tournament summaries are high-risk gaps until covered by real golden tests.

## Golden tests

The test suite includes synthetic PokerCraft-style fixtures based on observed public export structure. Future real user exports should be added as anonymized golden fixtures before broadening parser behavior.
