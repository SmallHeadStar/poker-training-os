# Parser Parity Backlog

## Current parser status

The GG PokerCraft parser is `implemented_provisional`.

It covers a narrow NLHE cash-style golden fixture and emits canonical JSON, but it is not yet real-format complete and is not H2N4-parity validated.

## High-risk format gaps

- Real GG PokerCraft exports beyond the synthetic fixture.
- Rush & Cash real hand histories.
- Tournament MTT hands and Game Summaries.
- Spin & Gold / SNG histories.
- Side pots and main pot / side pot collection lines.
- Split pots and chopped pots.
- Multiway all-ins.
- Run-it-twice or multiple board runouts.
- Insurance, Jackpot, Bingo, Fortune, Tax, or similar special result lines.
- Tournament chip units, buy-ins, bounty fields, prize fields, and levels.
- Heads-up, 3-max, 4-max, 9-max, missing seats, and table-balancing position labels.
- H2N4 position naming differences.

## Required real golden fixture set

Before parser parity can be claimed, add anonymized real exports for:

1. Regular cash 6-max.
2. Rush & Cash.
3. Tournament MTT plus Game Summary.
4. Spin & Gold or SNG.
5. All-in with side pot.
6. Split pot or chopped pot.
7. Hero folds before showdown and no showdown collection.
8. Tournament chips or non-dollar currency sample.

## Snapshot test requirement

Each real fixture should have an expected canonical JSON snapshot covering:

- hand count
- hand id
- game metadata
- Hero identity and position
- all players and positions
- full action sequence
- board and runouts
- showdown
- per-player results
- parser warnings

## H2N4 parser parity evidence needed

For the same fixture batch, export or normalize H2N4 evidence for:

- hand count
- Hero position by hand
- total result by hand
- position result
- action sequence or decision summary if available
- showdown and board interpretation

Any mismatch should be classified as `parser_gap` or `normalization_gap` before downstream stats are trusted.

