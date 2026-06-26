# Workflow

## Product Workflow

```text
1. Prepare Session
   User places a GG PokerCraft session zip/txt in a local session inbox.

2. Create Manifest
   Poker Training OS records `session_manifest.yaml` with session id, site, stake, files, and expected outputs.

3. H2N4 Import Package
   Poker Training OS prepares a checklist for the user to import the session into H2N4.

4. H2N4 Export
   User manually exports available H2N4 reports, filtered hands, pool reports, and marked hands.

5. Export Check
   Poker Training OS checks `exports/h2n/<session_id>/` for required folders and `manifest.yaml` files.

6. Ingest
   Poker Training OS reads H2N4 CSV/text exports or manual YAML/CSV summaries.

7. Normalize
   The system normalizes fields and attaches source labels such as `h2n4_csv`, `h2n4_manual`, `pts_generated`, and `human_review`.

8. Issue Cards
   Deterministic rules create Top 3 issue cards from source-tagged evidence.

9. Review Queue
   Representative hands and filtered-hand buckets become a review queue.

10. Study Cards
   The system creates GTO study cards for manual off-table study. V0.1 does not call a solver.

11. Session Review
   Review Delivery creates `session_review.md` in Chinese from source-grounded facts.

12. Training Focus
   The session review writes a next-cycle focus that can be checked against the next session.
```

## Standard Local Folder Layout

```text
D:\PokerTrainingOS\
  inbox\
    sessions\
      <session_id>\
        session.zip

  exports\
    h2n\
      <session_id>\
        overall\
        positions\
        filtered_hands\
        pool\
        marked_hands\

  reports\
    sessions\
      <session_id>\
```

The repository may contain examples and tests. Real user session data should stay in the local working folders and should not be committed.

## Development Workflow

```text
Docs first
-> local H2N4 export verification second
-> fixture export folders third
-> ingest contracts fourth
-> output renderer fifth
-> issue cards sixth
-> dashboard last
```

The native parser workflow is deferred:

```text
native fixtures
-> deterministic parser
-> tags
-> formulas
-> detectors
```

Use it only as a fallback or later milestone.

## Codex Task Workflow

Every Codex task should follow:

```text
Read AGENTS.md
-> choose one role from docs/agents
-> inspect related docs/tests/code
-> implement one narrow change
-> add/update tests when behavior changes
-> run verification
-> summarize changed and verified
```

## Four-Agent Workflow

Use four core agents in a simple chain:

```text
Product Orchestrator Agent
-> Data Pipeline Agent
-> Analysis Engine Agent
-> Review Delivery Agent
```

This is a workflow, not a bureaucracy. Most early tasks should use only one agent. Use multiple agents only when the output of one layer becomes the input of the next.

### Flow

1. Product Orchestrator defines the task, scope, boundary, and acceptance criteria.
2. Data Pipeline manages session manifests, H2N4 export contracts, ingest, and parser fallback.
3. Analysis Engine turns source-tagged facts into normalized metrics, issue cards, and review queue scoring.
4. Review Delivery turns outputs into reports, study cards, UI, and training-task presentation.

QA, docs, compliance, and release checks are embedded in these four roles instead of becoming separate agents.

## Agent Flow Protocol

Keep this lightweight. Do not create extra process documents unless this section becomes too large.

### 1. Task Entry

New tasks enter through `Product Orchestrator Agent` when they are new features, product decisions, cross-module work, or unclear requests.

The orchestrator produces a short task card:

```text
Task:
Owner agent:
Supporting agent(s):
Inputs:
Outputs:
Out of scope:
Acceptance:
```

If the task is obviously single-module, it may go directly to that module's agent after the scope is clear.

### 2. Handoff Between Agents

When one agent hands work to another, it must leave a short handoff note:

```text
From:
To:
Completed:
Output files / contracts:
Downstream can rely on:
Downstream must not assume:
Open questions:
Recommended next step:
```

Agents should pass contracts and facts, not vague intentions.

### 3. Dependency Requests

If an agent needs information owned by another agent, it should first read the relevant docs. If the answer is missing or requires a contract change, it sends the question back through `Product Orchestrator Agent`.

Use this format:

```text
From:
Needed from:
Question / dependency:
Why it matters:
Expected answer:
```

One agent should not silently change another agent's contract.

### 4. Acceptance

Final acceptance is triggered by `Product Orchestrator Agent` using read-only Acceptance Reviewer mode.

Acceptance checks:

```text
Scope respected
Contracts updated
Tests added or explained
No direct H2N4 DB access in V0.1
No H2N4 UI automation
No live-play boundary violation
Source labels present on generated facts
Downstream handoff is clear
```
