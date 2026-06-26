# Compliance Boundary

This document is a conservative project boundary, not legal advice.

## Allowed Product Shape

The product is designed as:

```text
Local
post-session
manual import
user's own hands
review and training
```

## Disallowed Product Shape

Do not implement:

- Real-time HUD.
- Real-time suggestions.
- Poker client scraping.
- Screen recognition of active tables.
- Automatic interaction with the GG client.
- Shared opponent databases.
- Imported hands not played by the user.
- Live opponent targeting.
- Botting or automated decision execution.

## Design Defaults

- Store data locally by default.
- Do not upload hand histories unless the user explicitly designs a later cloud mode.
- Prefer anonymized opponent identifiers in examples and fixtures.
- Make the UI wording clearly post-session and review-oriented.
- Never call a feature "live advice", "HUD", "auto-play", or similar.

## Agent Rule

Any agent that proposes a feature touching live gameplay must stop and route the question to `Compliance Guard Agent` before implementation.
