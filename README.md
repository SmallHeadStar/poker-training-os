# Poker Training OS

`poker-training-os` is a local, post-session poker training diagnosis system for the user's own GG PokerCraft sessions.

The current V0.1 architecture is **H2N4 Bridge + Session Review Orchestrator**. H2N4 handles the low-level tracker work. Poker Training OS reads H2N4 exports or user-entered H2N4 summaries, then creates issue cards, a review queue, GTO study cards, training-cycle updates, and Chinese session review reports.

It is not a HUD, bot, live advice tool, solver connector, H2N4 automation tool, or full tracker replacement.

## V0.1 Flow

```text
GG session zip/txt
-> session manifest
-> H2N4 import/export checklist
-> H2N4 exports or manual summaries
-> PTS ingest
-> session_summary.json
-> issue_cards.json
-> review_queue.csv
-> gto_study_cards.md
-> session_review.md
```

The first product test is simple: can one real session produce a useful `session_review.md` that makes the next training focus clearer?

## What This Is

- A personal post-session review and training tool.
- A local-first bridge above H2N4 exports.
- A structured workflow for turning session results into review decisions.
- A Codex-friendly project with clear agent roles and acceptance criteria.

## What This Is Not

- Not a real-time HUD.
- Not live decision assistance.
- Not a bot.
- Not GG client automation.
- Not H2N4 UI automation.
- Not a reader or writer for H2N4 internal databases in V0.1.
- Not a shared opponent database.
- Not a GTO solver replacement.

## First Development Milestones

1. Verify what H2N4 can export locally.
2. Lock the session folder and H2N4 export contract.
3. Generate a session manifest and H2N4 import/export checklist.
4. Ingest `session_summary.yaml`, H2N4 CSV exports, or manual CSV/YAML fallbacks.
5. Normalize source-tagged outputs.
6. Generate Top 3 issue cards and a review queue.
7. Generate `session_review.md`.
8. Add UI only after the bridge and report contracts are stable.

The previous native parser/detector slice is now a fallback or later milestone, not the V0.1 default.

## Key Docs

- `AGENTS.md`: project rules for Codex and other agents.
- `docs/01_mvp_scope.md`: V0.1 scope and later scope.
- `docs/session_review_workflow.md`: full session review workflow.
- `docs/h2n_bridge.md`: H2N4 bridge modes and forbidden adapters.
- `docs/h2n_export_contract.md`: expected H2N4 export folders and manifests.
- `docs/output_layer.md`: V0.1 output files and source labels.
- `docs/dashboard_v0_1.md`: minimal dashboard boundary.
- `docs/agents/00_agent_map.md`: four-agent responsibility map.

## Dependency Management

Use `uv` for local dependency management once the first lockfile is introduced. Core dependencies are DuckDB, Polars, Pydantic, and YAML support once the bridge ingest code is added. pandas and Streamlit are optional extras.
