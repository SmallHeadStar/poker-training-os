# Agent Workflow for poker-training-os

## Product Source of Truth

Before development, read `PRODUCT.md` for the product definition, H2N4-parity-first priority, product boundaries, completion standard, and provisional rules.

This file controls agent workflow and collaboration rules. If this file conflicts with `PRODUCT.md` about what the product is, `PRODUCT.md` wins.

## Multi-Agent Workflow

When scope grows beyond a small isolated change, switch to a controller plus subagents workflow.

### Controller Agent

The controller agent is responsible for:

- Maintaining product boundaries and architecture.
- Splitting work into small phases.
- Assigning focused research, implementation, or QA tasks.
- Reading and integrating subagent outputs.
- Making final code changes or approving small scoped subagent changes.
- Running pytest and parity validation.
- Maintaining a status table of `complete`, `provisional`, and `blocked` features.

The controller must not expand to later phases while unresolved parity questions remain in core parser, stats, or filter semantics.

### Subagent Output Contract

Each subagent must output:

- Scope covered.
- Files or modules inspected.
- Findings.
- Recommended changes.
- Tests needed.
- Risks and unknowns.
- Whether H2N4 parity evidence exists.

Subagents must not claim completion unless the controller verifies the result.

## Recommended Subagent Roles

### H2N4 Parity Research Agent

Researches H2N4-style stat, report, and filter semantics:

- Numerator and denominator rules.
- Opportunity definitions.
- Edge cases.
- Baseline requirements.
- Mismatch categories.

### GG Parser Agent

Focuses on GG PokerCraft hand-history parsing:

- Real export formats.
- Canonical model completeness.
- Parser edge cases.
- Golden fixtures.
- Parser warnings.

### Stats and Reports Agent

Focuses on Hero-centric stats and report outputs:

- VPIP.
- PFR.
- RFI.
- 3Bet.
- Call 3Bet.
- Fold to 3Bet.
- 4Bet.
- WTSD.
- W$SD.
- WWSF.
- Position results.
- bb/100.

### Filter and Spot Feature Agent

Designs structured spot features and group/filter behavior similar to H2N4-style reports:

- Pot type.
- Position combo.
- IP/OOP.
- Preflop line.
- Board family.
- Action line.
- Facing bet size bucket.
- Hero decision.

### QA and Parity Validation Agent

Owns verification:

- Test coverage.
- H2N4 baseline comparison.
- Diff classification.
- Regression risks.
- Provisional feature tracking.

### Dashboard Agent

Builds Streamlit UI only after data contracts and reports are stable.

The dashboard must stay compact, dark, and post-session focused.

## Coordination Rules

- Do not let multiple agents edit the same file at the same time.
- Prefer research-only subagents when definitions are uncertain.
- The controller must summarize subagent results before implementation.
- The controller must run tests after integration.
- The controller must clearly list remaining risks after each phase.
- Any H2N4-like behavior without baseline evidence must remain marked as `provisional`.
