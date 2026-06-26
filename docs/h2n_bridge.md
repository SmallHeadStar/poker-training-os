# H2N4 Bridge

This document defines how Poker Training OS may interact with H2N4 in V0.1.

## Principle

H2N4 owns low-level poker tracking and report calculation. Poker Training OS reads exported artifacts and creates a second-layer review workflow.

Poker Training OS must not recreate H2N4 before the bridge path is tested.

## Allowed Bridge Modes

### `h2n_import_package_provider`

Status: allowed.

Purpose:

- Prepare a local session folder and import checklist for the user.
- Record what files should be manually imported into H2N4.

Does not:

- Control H2N4.
- Click through H2N4 UI.
- Read H2N4 database files.

### `h2n_filtered_hands_export_provider`

Status: allowed, pending local format verification.

Purpose:

- Read filtered hand exports that the user manually saves from H2N4.
- Preserve hand references and bucket names.
- Feed review queue generation.

Expected folder:

```text
exports/h2n/<session_id>/filtered_hands/
```

### `h2n_report_csv_provider`

Status: pending local verification.

Purpose:

- Read H2N4 Overall, Position, Action Profit, or Smart Report CSV exports if H2N4 can export them.

Expected folders:

```text
exports/h2n/<session_id>/overall/
exports/h2n/<session_id>/positions/
```

Fallback:

- Use manual YAML/CSV files with source label `h2n4_manual`.

### `h2n_pool_report_provider`

Status: pending local verification.

Purpose:

- Read Player Pool report exports if H2N4 can export them.
- Use pool context as background evidence, not as live opponent targeting.

Expected folder:

```text
exports/h2n/<session_id>/pool/
```

### `h2n_marked_hands_provider`

Status: pending local verification.

Purpose:

- Read H2N4 marked hands exported by the user.
- Add marked hands to review queues or issue cards.

Expected folder:

```text
exports/h2n/<session_id>/marked_hands/
```

## Forbidden In V0.1

- Direct H2N4 database adapter.
- Reading H2N4 internal database files.
- Writing H2N4 internal database files.
- H2N4 UI automation.
- Screen scraping H2N4.
- Live GG client access.
- Real-time HUD behavior.
- Solver/GTO automatic integration.

## Source Labels

Bridge providers must output one of:

```text
h2n4_csv
h2n4_manual
pts_generated
human_review
```

Use `h2n4_csv` for values read from exported files.

Use `h2n4_manual` for values copied by the user into YAML/CSV because export is unavailable.

Use `pts_generated` for derived issue cards, review queues, study cards, and reports.

Use `human_review` for user labels and judgement.

## Verification Matrix

Track local H2N4 capability before implementation assumes it:

| Capability | Status | Evidence |
|---|---|---|
| Import GG PokerCraft zip/txt | pending local verification | |
| Export Overall CSV | pending local verification | |
| Export Position CSV | pending local verification | |
| Export Filtered Hands | pending local verification | |
| Export Action Profit / Smart Report | pending local verification | |
| Export Marked Hands | pending local verification | |

Do not turn a pending capability into required behavior until the user verifies it with real local files.
