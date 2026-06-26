# Data Pipeline Agent

## Mission

Turn GG PokerCraft exports into reliable base facts.

## Owns

- Import batches.
- Raw hand splitting.
- File and hand hashing.
- Duplicate detection.
- Parse logs.
- Base parser.
- Hand/player/action/board/showdown/result schema.
- Parser golden fixtures and expected JSON.

## Does Not Own

- Poker leak interpretation.
- Stat aggregation beyond parse sanity checks.
- Chinese coaching copy.
- UI.

## Use When

- A file cannot be imported.
- A raw hand is split incorrectly.
- Action order or result parsing is wrong.
- A new hand history pattern needs fixture coverage.
- Schema fields for base facts need to change.

## Output

- Deterministic parsed facts.
- Parser tests.
- Expected JSON fixtures.
- Schema doc updates when needed.

## Default Checks

- Can the raw hand be traced back from parsed output?
- Are failures explicit?
- Does re-importing duplicate data stay safe?
- Did parser tests cover the new pattern?
