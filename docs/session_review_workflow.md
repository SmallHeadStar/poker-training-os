# Session Review Workflow

This document defines the V0.1 end-to-end workflow for one post-session review.

## Goal

Run one real GG session through this chain:

```text
GG session zip/txt
-> session manifest
-> H2N4 import package/checklist
-> H2N4 export checklist
-> PTS ingest
-> issue cards
-> review queue
-> GTO study cards
-> training cycle update
-> session_review.md
```

V0.1 proves the review loop. It does not prove full automation.

## Inputs

Required:

- A local session folder.
- One or more GG PokerCraft exported zip/txt files owned by the user.
- `session_manifest.yaml`.

Optional depending on H2N4 export verification:

- H2N4 overall CSV.
- H2N4 position CSV.
- H2N4 filtered hand text exports.
- H2N4 Action Profit or Smart Report CSV/manual copy.
- H2N4 Player Pool report CSV/manual copy.
- H2N4 marked hands export.
- `session_summary.yaml` manual fallback.

## Step 1: Prepare Session Folder

Recommended local layout:

```text
D:\PokerTrainingOS\
  inbox\
    sessions\
      <session_id>\
        session.zip
        session_manifest.yaml
```

`session_id` should be stable and human-readable, for example:

```text
2026-06-26_z10
```

## Step 2: Create Session Manifest

`session_manifest.yaml` should identify the session and expected bridge path:

```yaml
session_id: 2026-06-26_z10
site: GG Poker
game: NL10 Zoom
source_files:
  - session.zip
h2n4_status: pending_import
expected_exports:
  - overall
  - positions
  - filtered_hands
  - pool
  - marked_hands
notes: ""
```

The manifest is a workflow control file. It is not a source of poker results unless a field explicitly says it is user-entered.

## Step 3: H2N4 Import Checklist

Poker Training OS should generate or present a checklist for the user:

```text
1. Open H2N4.
2. Import the GG PokerCraft session zip/txt.
3. Confirm the imported hand count.
4. Record whether import succeeded.
5. Export available reports into exports/h2n/<session_id>/.
```

V0.1 does not automate H2N4.

## Step 4: H2N4 Export Checklist

The user verifies these local questions:

```text
Can H2N4 export Overall as CSV?
Can H2N4 export Position report as CSV?
Can H2N4 export Filtered Hands as text/hand files?
Can H2N4 export or copy Action Profit / Smart Report?
Can H2N4 export Marked Hands?
```

Each answer should be reflected in the export folder's `manifest.yaml`.

## Step 5: PTS Ingest

Poker Training OS reads:

```text
exports/h2n/<session_id>/overall/
exports/h2n/<session_id>/positions/
exports/h2n/<session_id>/filtered_hands/
exports/h2n/<session_id>/pool/
exports/h2n/<session_id>/marked_hands/
```

If H2N4 cannot export a report, PTS may read manual fallback files such as:

```text
session_summary.yaml
position_results.csv
manual_action_profit.csv
```

Every ingested value must carry a source label.

## Step 6: Issue Cards

Issue cards are the Top 3 review candidates for the session.

Each issue card should include:

```text
issue_id
title
severity
source
source_files
evidence_summary
representative_hands
why_review
user_verdict
next_action
```

V0.1 issue cards are conservative. They should say "worth reviewing", not "confirmed mistake", until the user labels them.

## Step 7: Review Queue

The review queue turns issue cards and filtered hand buckets into a concrete list of hands or spots to inspect.

Minimum fields:

```text
queue_id
issue_id
session_id
source
hand_ref
bucket
priority
review_status
user_label
notes
```

## Step 8: GTO Study Cards

GTO study cards are manual study prompts, not solver output.

They should include:

```text
spot_type
why_this_spot
hands_to_review
questions_to_answer
study_target
```

V0.1 must not call a solver or present generated GTO numbers as facts.

## Step 9: Training Cycle Update

`training_cycle_update.json` records the next focus:

```json
{
  "session_id": "2026-06-26_z10",
  "next_focus": [],
  "source": "pts_generated",
  "requires_user_confirmation": true
}
```

The user can accept, edit, or reject the focus.

## Step 10: Session Review

`session_review.md` should include:

- Session summary.
- H2N4 loss summary.
- Top 3 issue cards.
- Review queue.
- GTO study cards.
- Next training focus.
- Source limitations and missing exports.

All conclusions must be grounded in source-tagged facts.

## V0.1 Done Definition

One real session is complete when:

```text
1. Session files are in the standard folder.
2. H2N4 export status is recorded.
3. PTS can read available exports or manual fallbacks.
4. PTS writes the V0.1 output files.
5. session_review.md clearly answers what to study next.
```
