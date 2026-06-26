# Product Definition for poker-training-os

## Product Intent

`poker-training-os` is a H2N4-parity-first local post-session poker training analyzer for personal GG PokerCraft exports.

It is intended to reproduce, as closely as possible, the core post-session analytical workflow of Hand2Note / H2N4 for a single user's hand histories.

The priority is accurate reproduction and validation of core Hand2Note-style analytical behavior, not fast feature breadth or UI polish.

## H2N4-Style Analytical Parity

The goal is H2N4-style analytical parity in:

- Hand-history import and normalization.
- Stats definitions and opportunity logic.
- Reports and grouped reports.
- Filter semantics.
- Position, line, and spot breakdowns.
- Action-profit-like post-session analysis.
- Leak discovery and issue-card generation.
- Review queue and training focus outputs.

This does not mean cloning H2N4 as a commercial product. The project must not copy H2N4 branding, icons, UI text, commercial interface details, HUD behavior, live assistance, opponent database features, or real-time table workflows.

In short: reproduce the analytical logic and post-session training value as much as possible; do not clone the product surface or violate the post-session-only boundary.

## Product Boundaries

The project must remain:

- Post-session only.
- Based only on user-exported hand histories.
- No HUD.
- No live advice.
- No screen reading.
- No running GG client reading.
- No automation of poker-client actions.
- No shared opponent database.

## Required Definition for Every Analytical Feature

Every stat, report, filter, and derived analysis must define:

- Numerator.
- Denominator.
- Opportunity rules.
- Edge cases.
- Sample requirements.
- Known limitations.
- H2N4 comparison status.

## Completion Standard

Nothing should be marked complete merely because unit tests pass.

A stat, report, filter, or derived analysis is complete only when:

- It has a documented definition.
- It has tests for expected numerator, denominator, and output behavior.
- It can be compared against a normalized H2N4 baseline for the same hand sample.
- Its H2N4 comparison result is within the explicit tolerance, or each mismatch is explained and classified.

If H2N4 baseline data is unavailable, implement the feature and comparison harness if useful, but mark the feature as `provisional`.

## Provisional Rule

Any H2N4-like behavior without baseline evidence must remain marked as `provisional`.

The project may still move forward with provisional features, but reports, docs, and status summaries must not imply H2N4 parity has been proven.

