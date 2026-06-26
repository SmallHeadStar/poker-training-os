# Issue Cards and Review Queue v0.1

## Purpose

Issue cards turn repeated losing spots into a small review backlog. They are not verdicts. The user must confirm, reject, or relabel them.

## Issue card fields

- `issue_name`
- `observation`
- `evidence`
- `common_pattern`
- `representative_hands`
- `review_question`
- `gto_study_hint`
- `next_cycle_metric`
- `source`
- `reliability`

## Review queue fields

- `hand_id`
- `issue_name`
- `source`
- `reliability`
- `human_label`
- `review_status`
- `notes`

## Allowed human labels

- `confirmed_error`
- `acceptable_play`
- `cooler`
- `sample_noise`
- `villain_specific`
- `tilt_related`
- `need_gto_review`
- `unknown`

## Interpretation rule

Cards must separate:

- observation: calculated loss pattern.
- hypothesis: why it may matter.
- human verdict: user label after review.
- training action: next study or practice item.

