# AGENTS.md

## Project

This repository is `poker-training-os`, a local post-session poker training and leak diagnosis system for the user's own GG PokerCraft hand histories.

The product goal is not to replace Hand2Note, build a HUD, or create a solver. The goal is to import post-session hands, structure them, tag decision nodes, find repeated leaks, build a review queue, and turn results into a weekly training cycle.

## Non-Negotiable Product Boundaries

Allowed:

- Manual import of the user's own exported GG PokerCraft hand histories.
- Offline post-session analysis.
- Local-first storage and processing.
- Deterministic parsing, tagging, and metric calculation.
- Leak detection based on documented rules and test fixtures.
- AI-generated Chinese review summaries based on computed facts.
- Personal training plans and progress checks.

Not allowed:

- Real-time HUD.
- Real-time poker decisions.
- Screen scraping a poker table.
- Reading or controlling a running GG client.
- Auto-playing, auto-clicking, or reducing live decision responsibility.
- Shared opponent databases.
- Data mining hands not played by the user.
- Using AI output as the source of truth for parsed facts or metric formulas.

## Current MVP

The MVP should support this flow:

```text
GG hand history files
-> import and clean raw hands
-> parse base hand facts
-> tag poker spots and action lines
-> calculate core stats
-> detect repeated leaks
-> produce a Chinese review report
-> create the next training cycle
```

First leak detectors:

- `RangeAlarmIgnored`: Hero continues in strong value-heavy nodes after the range alarm is already clear.
- `DominatedBroadway3betCall`: Hero calls 3bets with dominated broadways, hits top pair, and overpays.
- `OopRiverBluffcatchOvercall`: Hero overcalls river out of position with weak bluffcatchers.

## Data Layer Rules

- `RAW` data is the original imported hand text and import metadata.
- `BASE` data is deterministic parsed fact: hands, players, actions, board, showdown, result.
- `DERIVED` data is deterministic poker semantics: pot type, IP/OOP, board texture, hand class, action line.
- `METRIC` data is formula-driven output: bb/100, EV bb/100, VPIP, PFR, 3bet, node result.
- `LEAK` data is detector output based on documented rules.
- `REVIEW` data is the user's manual judgement.
- `TRAINING` data is the action plan and progress tracking.

AI may explain `METRIC`, `LEAK`, `REVIEW`, and `TRAINING` data. AI must not invent or alter `RAW`, `BASE`, `DERIVED`, or `METRIC` facts.

## Agent Operating Model

Use `docs/agents/00_agent_map.md` before selecting a role. The MVP uses only four core agents:

- `Product Orchestrator Agent`: product scope, workflow, compliance checks, task split.
- `Data Pipeline Agent`: import, raw cleaning, parser, schema, parser fixtures.
- `Analysis Engine Agent`: spot tags, stats, leak detectors.
- `Review Delivery Agent`: Chinese reports, training plan, UI, acceptance review.

QA, docs, compliance, and release are not separate early-stage agents. They are checklists inside the four core roles.

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
- Keep stat formulas documented in `docs/05_stats_dictionary.md`.
- Keep tag definitions documented in `docs/04_tag_dictionary.md`.
- Keep leak detector rules documented in `docs/06_leak_detectors.md`.
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
