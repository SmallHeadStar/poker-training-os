# AGENTS.md

## Project

This repository is `poker-training-os`, a local post-session poker training and leak diagnosis system for the user's own GG PokerCraft hand histories.

The product goal is not to replace Hand2Note, build a HUD, or create a solver. The goal is to import post-session hands, structure them, tag decision nodes, find repeated leak candidates, build a review queue, and turn results into training decisions.

## Non-Negotiable Product Boundaries

Allowed:

- Manual import of the user's own exported GG PokerCraft hand histories.
- Offline post-session analysis.
- Local-first storage and processing.
- Deterministic parsing, tagging, and metric calculation.
- Leak candidate detection based on documented rules and test fixtures.
- Chinese review summaries based on computed facts.

Not allowed:

- Real-time HUD.
- Real-time poker decisions.
- Screen scraping a poker table.
- Reading or controlling a running GG client.
- Auto-playing, auto-clicking, or reducing live decision responsibility.
- Shared opponent databases.
- Data mining hands not played by the user.
- Using AI output as the source of truth for parsed facts or metric formulas.

## Current V0.1

V0.1 is one vertical slice:

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

Do not start training cycles, Streamlit pages, AI summaries, full stats dashboards, or the second and third detector before V0.1 is stable.

## Data Layer Rules

- `RAW` data is original imported hand text and import metadata.
- `BASE` data is deterministic parsed fact: hands, players, actions, board, showdown, result.
- `DERIVED` data is deterministic decision-node semantics: pot type, player-count context, IP/OOP, board features, hand class, line before action.
- `METRIC` data is formula-driven output: bb/100, EV bb/100, VPIP, PFR, 3bet, node observations.
- `LEAK` data is detector candidate output based on documented decision-time rules.
- `REVIEW` data is the user's manual judgement.
- `TRAINING` data is later-cycle action planning and progress tracking.

AI may explain `METRIC`, `LEAK`, `REVIEW`, and `TRAINING` data. AI must not invent or alter `RAW`, `BASE`, `DERIVED`, or `METRIC` facts.

Detector matching must not depend on final result, showdown, or hand net loss. Match candidates from information available at the decision point. Store outcomes separately as evidence, then let the user review the verdict.

## Tech Stack

- Python 3.11+.
- DuckDB for local analytical storage.
- Polars is the primary DataFrame engine.
- pandas is allowed only in explicit compatibility adapters.
- Pydantic for typed contracts.
- Streamlit is optional UI tooling, not a core dependency.
- Use `uv` for local dependency management once the first lockfile is introduced.

## Agent Operating Model

Use `docs/agents/00_agent_map.md` before selecting a role. The MVP uses only four core agents:

- `Product Orchestrator Agent`: product scope, workflow, task split, compliance boundary checks.
- `Data Pipeline Agent`: import, raw cleaning, parser, schema, parser fixtures.
- `Analysis Engine Agent`: decision-node tags, stats, leak candidate matchers.
- `Review Delivery Agent`: Markdown reports, later UI, user-facing training output.

QA, docs, compliance, and release are not separate early-stage persistent agents. They are checklists or temporary review modes inside the four core roles.

Default sequence for any substantial task:

```text
Read AGENTS.md
-> read the relevant role card
-> inspect current code/docs/tests
-> state the intended scope
-> implement only that scope
-> add or update tests
-> run the narrowest meaningful verification
-> summarize facts, not guesses
```

For multi-agent work, `Product Orchestrator Agent` may split the work, but each subtask still needs one of the four roles, allowed files, expected output, and acceptance criteria.

## Engineering Rules

- Keep parser logic deterministic and heavily tested.
- Model one hand as many `decision_nodes`; do not collapse all decisions into one hand-level spot.
- Keep action amount semantics explicit: incremental amount, raise-to amount, amount-to-call, pot before action, all-in flag.
- Keep stat formulas documented in `docs/05_stats_dictionary.md`.
- Keep tag definitions documented in `docs/04_tag_dictionary.md`.
- Keep detector rules documented in `docs/06_leak_detectors.md`.
- Add tests before or alongside new parser, tagging, stat, or detector behavior.
- Prefer small, reviewable changes.
- Do not build UI before parser, schema, tags, and detector contracts are stable.
- Do not introduce live-poker features, background GG client access, or network upload of hand histories.

## Default Commands

Use these once the Python project is installed:

```bash
python -m pytest
python -m pytest tests/parser
python -m pytest tests/tagging
python -m pytest tests/stats
python -m pytest tests/detectors
python -m ruff check .
python -m mypy src
```

## PR / Task Summary Format

Every completed task should report:

```text
Changed:
- ...

Verified:
- ...

Notes / risks:
- ...
```

If verification could not be run, say exactly why and what remains unverified.
