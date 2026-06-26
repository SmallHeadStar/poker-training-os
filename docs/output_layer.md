# Output Layer

This document defines Poker Training OS V0.1 outputs.

## Output Root

Recommended path:

```text
reports/sessions/<session_id>/
```

Example:

```text
D:\PokerTrainingOS\reports\sessions\2026-06-26_z10\
```

## Required Outputs

V0.1 should write:

```text
session_review.md
session_summary.json
h2n_metrics.csv
position_results.csv
issue_cards.json
review_queue.csv
gto_study_cards.md
training_cycle_update.json
```

If an output cannot be generated, write a clear missing-data note in `session_review.md`.

## Source Labels

Every row or object that contains a fact should carry one of:

```text
h2n4_csv
h2n4_manual
pts_generated
human_review
```

Use `pts_generated` only for outputs created by Poker Training OS from source facts.

## `session_summary.json`

Purpose:

- Machine-readable session summary.
- Used by reports and later dashboards.

Minimum fields:

```json
{
  "session_id": "2026-06-26_z10",
  "site": "GG Poker",
  "game": "NL10 Zoom",
  "hands": null,
  "profit_bb": null,
  "bb_100": null,
  "ev_bb_100": null,
  "rake_bb": null,
  "source": "h2n4_manual",
  "source_files": [],
  "missing_exports": []
}
```

## `h2n_metrics.csv`

Purpose:

- Flat normalized metric table from H2N4 exports and manual fallbacks.

Minimum columns:

```text
session_id
metric_scope
metric_name
metric_value
unit
source
source_file
notes
```

Example scopes:

```text
overall
action_profit
smart_report
pool
```

## `position_results.csv`

Purpose:

- Position-level results from H2N4 position exports or manual fallback.

Minimum columns:

```text
session_id
position
hands
profit_bb
bb_100
ev_bb_100
source
source_file
notes
```

## `issue_cards.json`

Purpose:

- Top review candidates for the session.

Minimum object shape:

```json
{
  "issue_id": "issue_001",
  "session_id": "2026-06-26_z10",
  "title": "",
  "severity": "review",
  "source": "pts_generated",
  "evidence_sources": [],
  "evidence_summary": "",
  "representative_hands": [],
  "why_review": "",
  "user_verdict": null,
  "next_action": ""
}
```

`severity` is review priority, not proof of a mistake.

## `review_queue.csv`

Purpose:

- Concrete hands or buckets to review.

Minimum columns:

```text
queue_id
session_id
issue_id
priority
bucket
hand_ref
source
source_file
review_status
user_label
notes
```

## `gto_study_cards.md`

Purpose:

- Manual study prompts for selected spots.

Required sections per card:

```text
Spot
Why This Matters
Hands To Review
Questions
Study Target
Source Limits
```

V0.1 must not present solver output.

## `training_cycle_update.json`

Purpose:

- Proposed next focus, requiring user confirmation.

Minimum shape:

```json
{
  "session_id": "2026-06-26_z10",
  "source": "pts_generated",
  "requires_user_confirmation": true,
  "next_focus": [],
  "review_before_next_session": [],
  "notes": ""
}
```

## `session_review.md`

Purpose:

- Human-readable Chinese review report.

Required sections:

```text
# Session Review
## Session Summary
## H2N4 Loss Summary
## Top 3 Issue Cards
## Review Queue
## GTO Study Cards
## Next Training Focus
## Missing Data / Source Limits
```

The report must distinguish:

- H2N4-exported facts.
- Manually entered facts.
- PTS-generated review suggestions.
- Human review verdicts.
