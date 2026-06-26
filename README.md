# Poker Training OS

`poker-training-os` is a local, post-session poker training diagnosis system for the user's own GG PokerCraft hand histories.

The system imports exported hands, parses them into structured facts, tags decision nodes, calculates metrics, detects repeated leaks, and generates Chinese review reports and training plans.

## What This Is

- A personal review and training tool.
- A local-first post-session analyzer.
- A structured workflow for finding repeated poker leaks.
- A Codex-friendly project with clear agent roles and acceptance criteria.

## What This Is Not

- Not a real-time HUD.
- Not live decision assistance.
- Not a bot.
- Not a GG client automation tool.
- Not a shared opponent database.
- Not a GTO solver replacement.

## MVP Flow

```text
GG PokerCraft export
-> import batch
-> raw hand split and clean
-> base parser
-> spot tagging
-> stat calculation
-> leak detection
-> hand review queue
-> Chinese training report
-> next-cycle retest
```

## First Development Milestones

1. Create docs and agent operating rules.
2. Collect 10-20 sanitized GG hand fixtures.
3. Define expected JSON for parser golden tests.
4. Implement deterministic parser for base facts.
5. Implement spot tagging for the first leak scenarios.
6. Implement core stats and leak detectors.
7. Generate a Markdown review report.
8. Add a minimal Streamlit review UI after the core is verified.

## Key Docs

- `AGENTS.md`: project rules for Codex and other agents.
- `docs/02_workflow.md`: product and development workflow.
- `docs/agents/00_agent_map.md`: agent responsibility map.
- `docs/04_tag_dictionary.md`: spot and line tag definitions.
- `docs/05_stats_dictionary.md`: stat formulas.
- `docs/06_leak_detectors.md`: leak detector rules.
