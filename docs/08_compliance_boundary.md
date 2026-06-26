# Compliance Boundary

This document is a conservative project boundary, not legal advice.

## Allowed Product Shape

The product is designed as:

```text
Local
post-session
manual import
manual H2N4 export
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
- Automatic interaction with H2N4.
- Direct H2N4 internal database reads or writes in V0.1.
- Shared opponent databases.
- Imported hands not played by the user.
- Live opponent targeting.
- Botting or automated decision execution.
- Solver/GTO automatic integration in V0.1.

## H2N4 Boundary

Allowed:

- Generate a checklist telling the user what to import/export manually.
- Read files the user explicitly exported from H2N4.
- Read manual YAML/CSV files the user created from H2N4 reports.
- Mark H2N4 export capabilities as `pending local verification`.

Not allowed:

- Click H2N4 UI controls.
- Scrape H2N4 screens.
- Inspect H2N4 internal databases.
- Modify H2N4 internal files.
- Treat H2N4 exports as available before local verification.

## Design Defaults

- Store data locally by default.
- Do not upload hand histories unless the user explicitly designs a later cloud mode.
- Prefer anonymized opponent identifiers in examples and fixtures.
- Make UI wording clearly post-session and review-oriented.
- Never call a feature "live advice", "HUD", "auto-play", or similar.
- Show source labels for generated facts.

## Agent Rule

Any agent that proposes a feature touching live gameplay, H2N4 automation, H2N4 internals, or solver automation must stop and route the question to `Product Orchestrator Agent` before implementation. Do not add a separate persistent compliance agent during MVP work.
