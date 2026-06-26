# Poker Training OS

`poker-training-os` is a local, post-session poker training diagnosis system for the user's own GG PokerCraft hand histories.

The system imports exported hands, parses them into structured facts, emits decision nodes, tags candidate leaks, and generates Chinese review reports. It is not a HUD, bot, live advice tool, or GTO solver.

## V0.1 Flow

```text
5-10 sanitized GG fixtures
-> raw hand split
-> canonical JSON
-> base tables
-> decision nodes
-> DominatedBroadway candidate matcher
-> Markdown review report
-> tests
```

Later versions can add more parser fixtures, more candidate matchers, review labels, basic leak ranking, training-cycle comparison, Streamlit, and AI summaries grounded in computed facts.

## What This Is

- A personal review and training tool.
- A local-first post-session analyzer.
- A structured workflow for finding repeated poker leak candidates.
- A Codex-friendly project with clear agent roles and acceptance criteria.

## What This Is Not

- Not a real-time HUD.
- Not live decision assistance.
- Not a bot.
- Not a GG client automation tool.
- Not a shared opponent database.
- Not a GTO solver replacement.

## First Development Milestones

1. Correct architecture contracts.
2. Collect 5-10 sanitized GG hand fixtures.
3. Define expected canonical JSON.
4. Implement deterministic parser for base facts.
5. Emit explicit decision nodes.
6. Add the first DominatedBroadway candidate matcher.
7. Generate a Markdown review report.
8. Add UI only after the core slice is verified.

## Key Docs

- `AGENTS.md`: project rules for Codex and other agents.
- `docs/01_mvp_scope.md`: V0.1 scope and later scope.
- `docs/03_data_schema.md`: physical data contract.
- `docs/04_tag_dictionary.md`: tag dimensions.
- `docs/05_stats_dictionary.md`: stat formulas.
- `docs/06_leak_detectors.md`: detector candidate rules.
- `docs/agents/00_agent_map.md`: four-agent responsibility map.

## Dependency Management

Use `uv` for local dependency management once the first lockfile is introduced. Core dependencies are DuckDB, Polars, and Pydantic. pandas and Streamlit are optional extras.
