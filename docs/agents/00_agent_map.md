# Agent Map

The MVP uses four agents. Keep it small until real work proves a role needs to split.

## Owner Rule

`Product Orchestrator Agent` is the OWNER agent.

It is the entry point for new or cross-module tasks. It decides scope, selects the responsible agent, defines acceptance criteria, and triggers final acceptance review. It should not take over low-level parser, analysis, or UI implementation.

Single-module tasks may go directly to the responsible agent after the scope is clear.

## Role Summary

| Agent | Owns | Also Checks |
|---|---|---|
| Product Orchestrator | OWNER: product scope, workflow, task split, boundaries | compliance, docs consistency, final acceptance routing |
| Data Pipeline | Import, raw cleaning, parser, schema, parser fixtures | parse QA, duplicate handling |
| Analysis Engine | Decision-node tags, stats, candidate matches, outcome evidence | formulas, result-bias checks |
| Review Delivery | Chinese reports, training plans, UI | presentation QA, UX wording |

## Default Routing

- Need to decide what to build or how to split it: `Product Orchestrator Agent`
- Raw files, import batches, parser, expected JSON, schema: `Data Pipeline Agent`
- Tags, bb/100, VPIP/PFR, 3bet, candidate matcher rules: `Analysis Engine Agent`
- Markdown report, training task, review queue, Streamlit UI: `Review Delivery Agent`

## Normal Flow

```text
Product Orchestrator
-> Data Pipeline
-> Analysis Engine
-> Review Delivery
```

Most tasks should start at the lowest relevant layer. Example: a parser bug goes directly to `Data Pipeline Agent`; it does not need all four agents.

Cross-module tasks must start with `Product Orchestrator Agent`, then move downstream only when the previous agent has produced a handoff note.

## Acceptance Reviewer Mode

Keep the four long-lived agents. For review, use a temporary read-only Acceptance Reviewer mode rather than adding a fifth persistent agent.

Acceptance Reviewer mode checks:

- Contract compliance.
- Test, lint, and typecheck results.
- Cross-layer drift.
- Detector outcome bias.
- Candidate matches depending on final results.
- P0/P1/P2 findings.

It does not own implementation directories and should not make code changes unless explicitly asked.

## Contract Update Rule

The agent that changes a contract must update the related dictionary:

- Parser output -> `docs/03_data_schema.md`
- Tags -> `docs/04_tag_dictionary.md`
- Stats -> `docs/05_stats_dictionary.md`
- Detectors -> `docs/06_leak_detectors.md`
- Workflow -> `docs/02_workflow.md`
