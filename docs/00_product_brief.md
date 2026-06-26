# Product Brief

## One Sentence

Import GG post-session hand histories, structure the hands, tag decision nodes, find repeated leaks, generate review queues, and turn them into training cycles.

## User

The first user is the project owner: a GG Z10 player who wants to move toward Z25 with a better review loop.

The tool should answer:

- Am I actually beating Z10 after rake?
- Which repeated spots lose the most money?
- Which hands should I review first?
- Which 1-3 nodes should I train this week?
- Did the next batch of hands improve after training?

## Product Positioning

Hand2Note and PokerCraft show data. This project turns data into training decisions.

The product should be a personal diagnosis layer above exported GG hands, not a generic tracker clone.

## Core Loop

```text
Import hands
-> calculate results
-> find repeated leak patterns
-> pick representative hands
-> explain the problem in Chinese
-> create training tasks
-> retest on the next import
```

## Differentiation

- Focused on the user's Z10/Z25 growth path.
- Node-level leak ranking instead of broad dashboard sprawl.
- Personal rules and repeated-error tracking.
- AI explanations grounded in deterministic calculations.
- Small, testable modules that Codex can safely extend.
