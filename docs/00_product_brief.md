# Product Brief

## One Sentence

Use H2N4 exports from the user's own GG PokerCraft sessions to create source-grounded issue cards, review queues, GTO study cards, training-cycle updates, and Chinese post-session review reports.

## User

The first user is the project owner: a GG Z10 player who wants to move toward Z25 with a better review loop.

The tool should answer:

- Am I actually beating Z10 after rake?
- Which H2N4 report areas explain the largest losses or weak spots?
- Which filtered hands should I review first?
- Which 1-3 issues should I train next?
- Did the next session improve after training focus changed?

## Product Positioning

H2N4 shows and calculates the tracker layer. Poker Training OS turns H2N4-exported data into training decisions.

The product should be a personal diagnosis and orchestration layer above H2N4 exports, not a generic tracker clone and not a replacement for H2N4.

## Current Architecture

```text
GG PokerCraft session zip/txt
-> user imports into H2N4
-> user exports H2N4 reports and filtered hands
-> Poker Training OS ingests exported files or manual summaries
-> Poker Training OS builds issue cards, review queue, study cards, and session review
```

H2N4 owns:

- Overall and positional results.
- Reports, Smart Reports, and Action Profit.
- Filtered hands.
- Player Pool analysis.
- Marked hands when export is available.

Poker Training OS owns:

- Session manifests.
- H2N4 export checklists and contracts.
- Source-tagged ingest of H2N4 CSV/YAML/manual data.
- Issue card generation from documented rules.
- Review queue assembly.
- GTO study card prompts for later manual study.
- Chinese session review reports.
- Training-cycle update files.

## Core Loop

```text
Prepare session folder
-> run H2N4 import/export manually
-> ingest H2N4 exports
-> summarize session results
-> identify Top 3 review issues
-> queue representative hands
-> write Chinese session review
-> choose next training focus
-> retest on next session
```

## Differentiation

- Focused on the user's Z10/Z25 growth path.
- H2N4 bridge instead of tracker duplication.
- Session-level training decisions instead of dashboard sprawl.
- Source labels on every fact: `h2n4_csv`, `h2n4_manual`, `pts_generated`, or `human_review`.
- AI explanations grounded in deterministic or user-entered facts.
- Small, testable modules that Codex can safely extend.
