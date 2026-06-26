# Agent Map

The MVP uses four agents. Keep it small until real work proves a role needs to split.

## Owner Rule

`Product Orchestrator Agent` is the OWNER agent.

It is the entry point for new or cross-module tasks. It decides scope, selects the responsible agent, defines acceptance criteria, and triggers final acceptance review. It should not take over low-level ingest, analysis, or UI implementation.

Single-module tasks may go directly to the responsible agent after the scope is clear.

## Role Summary

| Agent | Owns | Also Checks |
|---|---|---|
| Product Orchestrator | OWNER: product scope, workflow, task split, boundaries | compliance, H2N4 bridge boundaries, docs consistency, final acceptance routing |
| Data Pipeline | Session manifests, H2N4 export contracts, export ingest, manual fallback files, parser fallback | source labels, missing export handling, duplicate session files |
| Analysis Engine | Metric normalization, issue cards, review queue scoring, training focus rules | formula provenance, result-bias checks, source quality |
| Review Delivery | Chinese reports, GTO study cards, training-cycle output, later UI | presentation QA, UX wording, no live-play language |

## Default Routing

- Need to decide what to build or how to split it: `Product Orchestrator Agent`
- Session folders, H2N4 export manifests, CSV/YAML ingest, raw file checks: `Data Pipeline Agent`
- H2N4 metrics normalization, source-tagged issue cards, review priority: `Analysis Engine Agent`
- Markdown report, GTO study cards, training tasks, review queue presentation, dashboard: `Review Delivery Agent`

Native parser, tag, stat, and detector work is currently a fallback or later route. If a task revives that path, route through `Product Orchestrator Agent` first.

## Normal Flow

```text
Product Orchestrator
-> Data Pipeline
-> Analysis Engine
-> Review Delivery
```

Most tasks should start at the lowest relevant layer. Example: a missing H2N4 `manifest.yaml` validation rule goes directly to `Data Pipeline Agent`; it does not need all four agents.

Cross-module tasks must start with `Product Orchestrator Agent`, then move downstream only when the previous agent has produced a handoff note.

## Acceptance Reviewer Mode

Keep the four long-lived agents. For review, use a temporary read-only Acceptance Reviewer mode rather than adding a fifth persistent agent.

Acceptance Reviewer mode checks:

- Contract compliance.
- Test, lint, and typecheck results when applicable.
- Cross-layer drift.
- Source label coverage.
- H2N4 export support marked `pending local verification` until the user verifies it.
- No direct H2N4 DB adapter in V0.1.
- No H2N4 UI automation.
- No live-play boundary violation.
- P0/P1/P2 findings.

It does not own implementation directories and should not make code changes unless explicitly asked.

## Contract Update Rule

The agent that changes a contract must update the related dictionary or contract document:

- Workflow -> `docs/02_workflow.md` or `docs/session_review_workflow.md`
- H2N4 bridge mode -> `docs/h2n_bridge.md`
- H2N4 export folder -> `docs/h2n_export_contract.md`
- Output file -> `docs/output_layer.md`
- Dashboard scope -> `docs/dashboard_v0_1.md`
- Parser-native schema fallback -> `docs/03_data_schema.md`
- Native tags -> `docs/04_tag_dictionary.md`
- Native stats -> `docs/05_stats_dictionary.md`
- Native detectors -> `docs/06_leak_detectors.md`
