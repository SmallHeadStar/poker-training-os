# H2N4 Reference Map

## Working rule

We can borrow concepts from Hand2Note documentation, public discussions, and open-source parser examples, but we do not treat any local implementation as accurate until it passes same-sample H2N4 export comparison.

## Primary H2N4 references

| Capability | Reference | What we use it for |
| --- | --- | --- |
| Reports and Action Profit | https://hand2note.com/Help/Features/reports | Report workflow, action-profit-oriented leak finding. |
| Smart Reports | https://hand2note.com/Help/Features/smart-reports | Relevant stats after a filter and next-action style report organization. |
| Custom Filter in Reports | https://hand2note.com/Help/Features/custom-filter-in-reports | Structured filter builder target and filter-generated reports. |
| Report Navigation | https://hand2note.com/Help/Features/report-navigation | Interactive stat, range, faced-next, and next-action navigation model. |
| Supported Sites | https://hand2note.com/Help/supported-sites | GG can be analyzed from hand histories; this project remains post-session only. |
| Action Profit | https://hand2note.com/Help/Features/action-profit | Primary H2N4 feature reference for Action Profit workflows. |
| Decision Analysis formula background | https://hand2note3.hand2note.com/Help/Index/DecisionAnalysis | Supplemental formula background: result from stack right before action to stack at hand end; fold equals zero. |

## Open-source and public implementation references

| Area | Reference | Use |
| --- | --- | --- |
| PokerCraft export shape | https://github.com/McDic/pokercraft-local | Public parser examples and synthetic fixture calibration. |
| H2N4 API boundary | https://github.com/hand2note/Hand2Note4.Api | Compliance boundary awareness; not used for HUD/live automation. |

## Feature priority

1. Parser parity: H2N4 and our importer must agree on hand count, Hero, positions, actions, board, showdown, and results.
2. Basic report parity: hands, total bb, bb/100, position results, VPIP, PFR, RFI, 3Bet, call/fold/4Bet vs 3Bet, WTSD, W$SD, WWSF.
3. Filter parity: structured custom-filter-like fields must reproduce H2N4 filtered report rows.
4. Action Profit parity: action profit must match H2N4 exported values; H2N3 formula docs are only supplemental until H2N4 baseline confirms exact behavior.
5. Smart/next-action reports: after filters, show relevant follow-up stats and opportunity counts.
6. Training outputs: issue cards and study cards should only claim evidence quality from validated upstream reports.

## Current blocker

No real H2N4 baseline export is present yet. Therefore all analytical outputs are provisional.
