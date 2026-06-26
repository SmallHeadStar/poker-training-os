# H2N4 Export Contract

This document defines the V0.1 folder contract for H2N4 exports.

## Root

All H2N4 exports for one session live under:

```text
exports/h2n/<session_id>/
```

Recommended local example:

```text
D:\PokerTrainingOS\exports\h2n\2026-06-26_z10\
```

## Required Folder Names

Create these folders even when a capability is not available yet:

```text
overall/
positions/
filtered_hands/
pool/
marked_hands/
```

Each folder needs a `manifest.yaml`.

## Root Manifest

`exports/h2n/<session_id>/manifest.yaml`:

```yaml
session_id: 2026-06-26_z10
source_app: H2N4
exported_at_local: null
export_status:
  overall: pending
  positions: pending
  filtered_hands: pending
  pool: pending
  marked_hands: pending
notes: ""
```

Allowed status values:

```text
pending
available
manual_only
not_available
failed
not_checked
```

## Folder Manifest

Each export folder should include:

```yaml
session_id: 2026-06-26_z10
export_type: overall
source_app: H2N4
source_label: h2n4_csv
status: pending
files: []
manual_fallback: null
notes: ""
```

For manual-only data:

```yaml
session_id: 2026-06-26_z10
export_type: overall
source_app: H2N4
source_label: h2n4_manual
status: manual_only
files:
  - session_summary.yaml
manual_fallback: session_summary.yaml
notes: "Overall numbers copied from H2N4 report."
```

## Overall Folder

Path:

```text
exports/h2n/<session_id>/overall/
```

Accepted files:

```text
manifest.yaml
overall.csv
session_summary.yaml
manual_overall.csv
```

Minimum desired fields:

```text
hands
profit_bb
bb_100
ev_bb_100
rake_bb
source
```

## Positions Folder

Path:

```text
exports/h2n/<session_id>/positions/
```

Accepted files:

```text
manifest.yaml
positions.csv
position_results.csv
manual_positions.csv
```

Minimum desired fields:

```text
position
hands
profit_bb
bb_100
ev_bb_100
source
```

## Filtered Hands Folder

Path:

```text
exports/h2n/<session_id>/filtered_hands/
```

Recommended layout:

```text
filtered_hands/
  manifest.yaml
  river_call/
    hands.txt
    manifest.yaml
  3bet_pot_oop/
    hands.txt
    manifest.yaml
  utg_vs_bb_low_board/
    hands.txt
    manifest.yaml
```

Bucket manifest:

```yaml
session_id: 2026-06-26_z10
bucket: river_call
source_label: h2n4_csv
status: available
files:
  - hands.txt
notes: ""
```

## Pool Folder

Path:

```text
exports/h2n/<session_id>/pool/
```

Accepted files:

```text
manifest.yaml
pool.csv
manual_pool.csv
```

Pool exports are post-session population context. They must not become live opponent targeting.

## Marked Hands Folder

Path:

```text
exports/h2n/<session_id>/marked_hands/
```

Accepted files:

```text
manifest.yaml
marked_hands.txt
marked_hands.csv
```

Marked hands may feed the review queue directly.

## Validation Rules

V0.1 validators should check:

- Root export folder exists.
- Required subfolders exist.
- Each folder has `manifest.yaml`.
- Manifest status is one of the allowed values.
- Listed files exist.
- Source labels are valid.
- Missing exports produce warnings, not crashes, when a manual fallback exists.

Validators must not inspect H2N4 internal files.
