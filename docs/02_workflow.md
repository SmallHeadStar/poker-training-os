# Workflow

## Product Workflow

```text
1. Import
   User manually exports GG PokerCraft hands and imports the files.

2. Clean
   System splits raw files into individual hands, hashes them, removes duplicates, and records parse errors.

3. Parse
   Parser converts raw text into base facts: hand, players, actions, board, showdown, result.

4. Tag
   Spot tagger derives poker semantics: SRP/3BP/4BP, IP/OOP, position relation, hand class, board texture, action line.

5. Calculate
   Stats engine computes formulas: bb/100, EV bb/100, VPIP, PFR, 3bet, call 3bet, node result.

6. Detect
   Leak detectors search tagged hands for repeated patterns and compute loss, confidence, and representative hands.

7. Review
   Review coach creates Chinese summaries and asks the user to confirm whether a spot was a mistake, cooler, tilt, or exploit.

8. Train
   Training module turns confirmed leaks into weekly tasks and retests the next import.
```

## Development Workflow

```text
Docs first
-> fixtures second
-> deterministic parser third
-> tags fourth
-> formulas fifth
-> detectors sixth
-> reports seventh
-> UI last
```

## Codex Task Workflow

Every Codex task should follow:

```text
Read AGENTS.md
-> choose one role from docs/agents
-> inspect related docs/tests/code
-> implement one narrow change
-> add/update tests
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
2. Data Pipeline converts raw hand histories into reliable base facts.
3. Analysis Engine turns facts into tags, stats, and leak results.
4. Review Delivery turns analysis into reports, UI, training tasks, and final acceptance checks.

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
No detector outcome bias
No live-play boundary violation
Downstream handoff is clear
```
