# Product Positioning

## One-line position

`poker-training-os` is a local, post-session, personal training analysis tool for GG Poker cash and zoom players who manually export their own PokerCraft hand histories.

## What it is

- A personal study system for hands the user has already played.
- A structured import, normalization, reporting, review, and training-cycle workflow.
- A compact analytical dashboard with reports, loss maps, issue cards, and review queues.
- An H2N4-inspired information architecture, focused on the small subset needed for individual training.

## What it is not

- Not a real-time HUD.
- Not live table assistance.
- Not a screen reader or GG client reader.
- Not an auto-player, betting bot, or decision engine for live play.
- Not a shared opponent database.
- Not a full Hand2Note 4 clone.
- Not a solver replacement.

## Product boundary

All analysis starts from hand-history files that the user manually exports after play. The system must not inspect running poker clients, observe tables, capture screens, or provide in-game advice.

## Target user

The first target user is a GG Poker cash or zoom player who wants to turn exported sessions into:

- Basic performance reports.
- Repeat-loss spot discovery.
- Action-result observations with clear limitations.
- Issue cards for human review.
- GTO study prompts.
- Next-cycle training focus.

## Success criteria

- Formula definitions are explicit and testable.
- Every calculated stat has a known numerator, denominator, sample requirement, and limitation.
- Reports separate observation, hypothesis, human verdict, and training action.
- Risky attribution is avoided. Whole-hand profit is not casually assigned to one decision.

