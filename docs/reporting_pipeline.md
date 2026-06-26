# Reporting Pipeline v0.1

## Input

One canonical hand JSON object or a list of canonical hand JSON objects.

## Outputs

The session writer generates:

- `session_review.md`
- `session_summary.json`
- `basic_reports.csv`
- `loss_map.csv`
- `issue_cards.json`
- `review_queue.csv`
- `gto_study_cards.md`
- `training_cycle_update.json`

All generated report values are provisional until H2N4 same-sample parity evidence exists.

## Claim separation

`session_review.md` uses explicit sections:

- Observation
- Hypothesis
- Human Verdict
- Training Action

Unknown human verdicts remain `unknown` until the user reviews the queue.
