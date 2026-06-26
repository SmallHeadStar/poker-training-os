# Reporting Contract

## Required session outputs

| Artifact | Format | Purpose |
| --- | --- | --- |
| `session_review.md` | Markdown | Human-readable review with observations, hypotheses, verdicts, and training actions. |
| `session_summary.json` | JSON | Session metadata and KPI summary. |
| `basic_reports.csv` | CSV | H2N4-style basic stat tables. |
| `loss_map.csv` | CSV | Repeated losing spot summaries. |
| `issue_cards.json` | JSON | Structured issue cards for review. |
| `review_queue.csv` | CSV | Hands and spots awaiting human labels. |
| `gto_study_cards.md` | Markdown | Study prompts and solver-review hints. |
| `training_cycle_update.json` | JSON | Next-cycle focus and measurable follow-up metrics. |

## Required separation

Reports must label claims as one of:

- `observation`: directly calculated from the imported data.
- `hypothesis`: system-generated interpretation that needs review.
- `human_verdict`: user-confirmed label or judgment.
- `training_action`: concrete study or practice item.

## Reliability fields

Loss and issue outputs must include:

- `sample_count`
- `total_hand_net_bb`
- `avg_hand_net_bb`
- `max_5_loss_share`
- `reliability_level`
- `representative_hands`
- `warning`

## Attribution rule

`hand_net_bb`, `decision_incremental_bb`, and `observed_result` are separate fields. Whole-hand profit must not be treated as the EV of one decision unless the contract for that analysis explicitly supports it.

