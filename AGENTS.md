# AGENTS.md

## Project

This repository is `poker-training-os`, a local post-session poker training and leak diagnosis system for the user's own GG PokerCraft sessions.

The current V0.1 architecture is **H2N4 Bridge + Session Review Orchestrator**.

H2N4 is responsible for low-level poker tracking, Reports, Smart Reports, Action Profit, Filtered Hands, and Player Pool analysis. Poker Training OS reads H2N4 exports or explicitly entered manual summaries, then turns them into issue cards, review queues, GTO study cards, training-cycle updates, and Chinese session review reports.

The product goal is not to replace Hand2Note/H2N4, build a HUD, create a solver, or recreate a full tracker. The goal is to run a reliable post-session review workflow from the user's own session data.

## Non-Negotiable Product Boundaries

Allowed:

- Manual import of the user's own exported GG PokerCraft session zip/txt files.
- Manual H2N4 import and export by the user.
- Offline post-session analysis.
- Local-first storage and processing.
- Reading documented H2N4 export files and user-entered YAML/CSV summaries.
- Deterministic parsing of export files, manifest files, and report inputs.
- Issue card and review queue generation based on documented rules and source-tagged facts.
- Chinese review summaries based on source-tagged computed or manually entered facts.

Not allowed:

- Real-time HUD.
- Real-time poker decisions.
- Screen scraping a poker table.
- Reading or controlling a running GG client.
- Automatically controlling H2N4 or its UI.
- Reading or writing H2N4 internal databases in V0.1.
- Auto-playing, auto-clicking, or reducing live decision responsibility.
- Shared opponent databases.
- Data mining hands not played by the user.
- Solver/GTO automatic integration in V0.1.
- Using AI output as the source of truth for parsed facts, metrics, or H2N4-derived values.

## Current V0.1

V0.1 is one bridge-and-review slice:

```text
GG session zip/txt
-> session manifest
-> H2N4 import/export checklist
-> user runs H2N4 import and exports available files
-> Poker Training OS ingests H2N4 exports or manual summaries
-> session_summary.json
-> issue_cards.json
-> review_queue.csv
-> gto_study_cards.md
-> session_review.md
```

Do not start a full parser, Streamlit app, solver connector, H2N4 automation, or full stats dashboard before this V0.1 chain is stable.

The previous parser-native vertical slice remains a later or fallback route:

```text
sanitized GG fixtures
-> raw hand split
-> canonical JSON
-> base tables
-> decision nodes
-> deterministic leak matchers
-> Markdown review report
-> tests
```

Use that route only if H2N4 exports are insufficient or a later milestone explicitly revives native parsing.

## Data Layer Rules

- `RAW` data is original imported session files, H2N4 export files, and import metadata.
- `H2N_EXPORT` data is source-tagged output from H2N4 folders such as overall, positions, filtered_hands, pool, and marked_hands.
- `MANUAL_INPUT` data is user-entered YAML/CSV copied from H2N4 when export is unavailable.
- `BASE` data is deterministic parsed fact from an allowed source file.
- `DERIVED` data is deterministic post-session semantics produced by Poker Training OS.
- `METRIC` data is formula-driven output or H2N4-exported metric values with source provenance.
- `ISSUE` data is Poker Training OS issue card output based on documented rules.
- `REVIEW` data is the user's manual judgement.
- `TRAINING` data is later-cycle action planning and progress tracking.

Every output fact must carry a source label:

```text
h2n4_csv
h2n4_manual
pts_generated
human_review
```

AI may explain `METRIC`, `ISSUE`, `REVIEW`, and `TRAINING` data. AI must not invent or alter `RAW`, `H2N_EXPORT`, `MANUAL_INPUT`, `BASE`, `DERIVED`, or `METRIC` facts.

Issue matching must not depend on final result alone. If hand outcomes are used, store them as evidence and present them as review context, not as proof of a mistake.

## Tech Stack

- Python 3.11+.
- DuckDB for local analytical storage when persistence is needed.
- Polars is the primary DataFrame engine for CSV and tabular processing.
- pandas is allowed only in explicit compatibility adapters.
- Pydantic for typed contracts.
- YAML is allowed for user-authored session manifests and manual summaries.
- Streamlit is optional UI tooling, not a core dependency.
- Use `uv` for local dependency management once the first lockfile is introduced.

## Agent Operating Model

Use `docs/agents/00_agent_map.md` before selecting a role. The MVP uses only four core agents:

- `Product Orchestrator Agent`: product scope, workflow, task split, compliance boundary checks.
- `Data Pipeline Agent`: session manifests, H2N4 export contracts, export ingestion, parser fallback.
- `Analysis Engine Agent`: metric normalization, issue cards, review queue scoring, deterministic analysis rules.
- `Review Delivery Agent`: Markdown reports, GTO study cards, later UI, user-facing training output.

QA, docs, compliance, and release are not separate early-stage persistent agents. They are checklists or temporary review modes inside the four core roles.

Default sequence for any substantial task:

```text
Read AGENTS.md
-> read the relevant role card
-> inspect current code/docs/tests
-> state the intended scope
-> implement only that scope
-> add or update tests when behavior changes
-> run the narrowest meaningful verification
-> summarize facts, not guesses
```

For multi-agent work, `Product Orchestrator Agent` may split the work, but each subtask still needs one of the four roles, allowed files, expected output, and acceptance criteria.

## Engineering Rules

- Keep all H2N4 export parsing deterministic and heavily tested.
- Do not treat H2N4 export capability as verified until the user confirms it locally.
- Do not automate H2N4 UI actions.
- Do not read or write H2N4 internal databases in V0.1.
- Keep source provenance explicit on every generated output.
- Keep metric formulas and imported metric semantics documented in `docs/05_stats_dictionary.md`.
- Keep issue card rules documented before implementation.
- Add tests before or alongside new ingestion, normalization, report, or issue-card behavior.
- Prefer small, reviewable changes.
- Do not build UI before the bridge contracts, output contracts, and report renderer are stable.
- Do not introduce live-poker features, background GG client access, or network upload of hand histories.

## Default Commands

Use these once the Python project is installed:

```bash
python -m pytest
python -m pytest tests/parser
python -m pytest tests/tagging
python -m pytest tests/stats
python -m pytest tests/detectors
python -m pytest tests/reports
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
