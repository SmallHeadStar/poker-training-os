# Dashboard V0.1

The dashboard is not the V0.1 priority. This document defines the maximum allowed dashboard scope once the bridge outputs are stable.

## Principle

Dashboard V0.1 is a viewer for generated session outputs. It must not become a tracker clone, HUD, solver UI, or H2N4 automation surface.

## Allowed Panels

Dashboard V0.1 only includes:

- Session Summary.
- H2N4 Loss Summary.
- Issue Cards Top 3.
- Review Queue.
- Next Training Focus.

No broad stats dashboard, graph-heavy tracker clone, or player-pool explorer in V0.1.

## Data Sources

Every displayed value must show one source label:

```text
h2n4_csv
h2n4_manual
pts_generated
human_review
```

If a value has no source label, do not display it as a fact.

## Panel Contracts

### Session Summary

Reads:

```text
session_summary.json
```

Shows:

- Session id.
- Site/game/stake.
- Hands.
- Profit bb.
- bb/100.
- EV bb/100 when available.
- Rake bb when available.
- Missing export warnings.

### H2N4 Loss Summary

Reads:

```text
h2n_metrics.csv
position_results.csv
```

Shows:

- Largest negative report areas.
- Position losses.
- Source limitations.

Use neutral wording such as "review area" unless the user confirmed a mistake.

### Issue Cards Top 3

Reads:

```text
issue_cards.json
```

Shows:

- Title.
- Evidence summary.
- Why review.
- Representative hands.
- User verdict when available.

### Review Queue

Reads:

```text
review_queue.csv
```

Shows:

- Priority.
- Bucket.
- Hand reference.
- Review status.
- User label.

### Next Training Focus

Reads:

```text
training_cycle_update.json
```

Shows:

- Proposed focus.
- Review-before-next-session items.
- Confirmation status.

## Out Of Scope

- Real-time data.
- Live table overlays.
- H2N4 automation buttons.
- Direct H2N4 DB browsing.
- Solver integration.
- Full graphing dashboard.
- Player-pool targeting UI.
- Opponent-specific live recommendations.

## Acceptance

Dashboard V0.1 is acceptable only after:

- The output files in `docs/output_layer.md` exist for at least one session.
- Source labels are present.
- Missing data is handled gracefully.
- Wording is clearly post-session.
