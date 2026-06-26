# Codex Operating Model

## Layers

```text
AGENTS.md
= durable project constitution

docs/agents/*.md
= four core role cards and boundaries

.github/codex/prompts/*.md
= reusable task prompts

GitHub issues / local task prompts
= concrete task scope and acceptance criteria
```

## Why Not Build a Complex Agent Platform First

The project needs clear role boundaries more than automation. Start with four role cards and a few prompt templates. Add more roles only after repeated manual workflows prove that one role is overloaded.

## Standard Task Prompt Shape

```text
Role:
Use <agent role>.

Context:
Read AGENTS.md and these docs: ...

Task:
Implement exactly ...

Allowed files:
...

Forbidden files:
...

Acceptance:
...

Verification:
...
```

## When To Use Multiple Agents

Use multiple agents when:

- A task needs raw parsing first, then tags/stats/detectors.
- A task changes both analysis logic and report/UI output.
- Product scope must be clarified before implementation.

Do not use multiple agents just to make a small code edit look sophisticated. For MVP work, one agent is usually enough.
