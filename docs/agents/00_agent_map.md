# Agent Map

The MVP uses four agents. Keep it small until real work proves a role needs to split.

## Role Summary

| Agent | Owns | Also Checks |
|---|---|---|
| Product Orchestrator | Product scope, workflow, task split, boundaries | compliance, docs consistency |
| Data Pipeline | Import, raw cleaning, parser, schema, parser fixtures | parse QA, duplicate handling |
| Analysis Engine | Decision-node tags, stats, leak detectors | formulas, detector false positives |
| Review Delivery | Chinese reports, training plans, UI | UX wording, final QA |

## Default Routing

- Need to decide what to build or how to split it: `Product Orchestrator Agent`
- Raw files, import batches, parser, expected JSON, schema: `Data Pipeline Agent`
- Tags, bb/100, VPIP/PFR, 3bet, detector rules: `Analysis Engine Agent`
- Markdown report, training task, review queue, Streamlit UI: `Review Delivery Agent`

## Normal Flow

```text
Product Orchestrator
-> Data Pipeline
-> Analysis Engine
-> Review Delivery
```

Most tasks should start at the lowest relevant layer. Example: a parser bug goes directly to `Data Pipeline Agent`; it does not need all four agents.

## Acceptance Reviewer Mode

Keep the four long-lived agents. For review, use a temporary read-only Acceptance Reviewer mode rather than adding a fifth persistent agent.

Acceptance Reviewer mode checks:

- Contract compliance.
- Test, lint, and typecheck results.
- Cross-layer drift.
- Detector outcome bias.
- P0/P1/P2 findings.

It does not own implementation directories and should not make code changes unless explicitly asked.

## Contract Update Rule

The agent that changes a contract must update the related dictionary:

- Parser output -> `docs/03_data_schema.md`
- Tags -> `docs/04_tag_dictionary.md`
- Stats -> `docs/05_stats_dictionary.md`
- Detectors -> `docs/06_leak_detectors.md`
- Workflow -> `docs/02_workflow.md`
