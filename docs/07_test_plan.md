# Test Plan

## Current V0.1 Test Pyramid

Priority order for the H2N4 Bridge path:

```text
1. Session manifest validation tests
2. H2N4 export folder contract tests
3. CSV/YAML/manual fallback ingest tests
4. Source label propagation tests
5. Output file rendering tests
6. Missing-export behavior tests
7. Dashboard smoke tests, later
```

Native parser, tagging, stats, and detector tests remain useful for the fallback route, but they are not the current V0.1 gate.

## V0.1 Gate

V0.1 requires one bridge-and-review slice, not full product coverage:

- One sample session folder.
- `session_manifest.yaml`.
- H2N4 export root with required subfolders.
- `manifest.yaml` in each export folder.
- At least one manual fallback file such as `session_summary.yaml` if real CSV export is unavailable.
- Ingest output with source labels.
- `session_summary.json`.
- `issue_cards.json`.
- `review_queue.csv`.
- `gto_study_cards.md`.
- `session_review.md`.

## Manifest Tests

Test requirements:

- Session id is present.
- Source files are listed.
- Expected exports are valid.
- H2N4 status is explicit.
- Invalid status values fail clearly.

## Export Contract Tests

Test requirements:

- `exports/h2n/<session_id>/` exists.
- Required subfolders exist.
- Each folder has `manifest.yaml`.
- Listed files exist.
- Status values are valid.
- Missing but optional exports produce warnings, not crashes.

## Ingest Tests

Test requirements:

- H2N4 CSV rows keep source label `h2n4_csv`.
- Manual YAML/CSV rows keep source label `h2n4_manual`.
- PTS-generated outputs use `pts_generated`.
- Human labels use `human_review`.
- Unknown source labels fail.
- Missing numeric fields are represented explicitly.

## Issue Card Tests

Test requirements:

- Issue cards are generated from source-tagged evidence.
- Issue cards do not present losses as confirmed mistakes.
- Top 3 selection is deterministic.
- Missing evidence produces a lower-confidence or skipped card.

## Report Tests

Report tests should verify structure and grounding in source-tagged facts.

The report must distinguish:

- H2N4-exported facts.
- Manual H2N4 entries.
- PTS-generated issue cards.
- User review verdicts.
- Missing exports and source limitations.

## Later Native Parser Gate

Before reviving parser-native work, the project should explicitly re-accept:

- Sanitized GG fixtures.
- Canonical parser golden tests.
- Decision-node tests.
- Tagging tests.
- Candidate matcher tests.
- Report tests from native parsed facts.

Do not mix this gate into the H2N4 Bridge V0.1 unless Product Orchestrator changes the route.
