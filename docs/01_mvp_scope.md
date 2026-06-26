# MVP Scope

## V0.1 In Scope

V0.1 validates the H2N4 Bridge + Session Review Orchestrator path.

In scope:

- Standard local session folder layout.
- `session_manifest.yaml` describing a single GG session.
- H2N4 import/export checklist generated from the session manifest.
- H2N4 export folder contract under `exports/h2n/<session_id>/`.
- Manual fallback files such as `session_summary.yaml` when H2N4 CSV export is unavailable.
- Ingest of available H2N4 CSV/YAML/text exports.
- Source-tagged normalized outputs.
- `session_review.md`.
- `session_summary.json`.
- `h2n_metrics.csv`.
- `position_results.csv`.
- `issue_cards.json`.
- `review_queue.csv`.
- `gto_study_cards.md`.
- `training_cycle_update.json`.
- Tests for ingest, source labels, output rendering, and missing-export handling once implementation begins.

## H2N4 Export Verification Questions

Before building deeper automation, locally verify:

```text
1. Can H2N4 import GG PokerCraft zip/txt exports?
2. Can Overall / Position reports be exported as CSV?
3. Can Filtered Hands be exported as hand files?
4. Can Action Profit / Smart Report tables be copied or exported?
5. Can Marked Hands be exported?
```

The result decides the implementation path:

| Verification result | Route |
|---|---|
| CSV reports + filtered hands work | Preferred H2N4 Bridge path |
| Only filtered hands work | Bridge path with more PTS-side summarization |
| Only manual copy works | V0.1 uses `session_summary.yaml` and manual CSV/YAML |
| Exports are unstable | Pause H2N4 Bridge and revisit native parser fallback |

Until verified, H2N4 export support is `pending local verification`.

## Later Scope

- Native GG hand parser fallback.
- More H2N4 report adapters after export formats are verified.
- More issue card types.
- Human review labels.
- Basic leak ranking across multiple sessions.
- Training-cycle comparison.
- Streamlit UI.
- AI Chinese summaries grounded in computed facts.
- Solver-assisted study references only after manual study-card workflow is stable.

## Out of Scope

- Real-time HUD or overlay.
- Live hand advice.
- GG client automation.
- H2N4 UI automation.
- Direct H2N4 database access in V0.1.
- Screen scraping.
- Shared opponent database.
- Data mining hands not played by the user.
- Full GTO solver integration.
- Full Hand2Note/H2N4 replacement.
- Broad commercial multi-user product.
- Streamlit UI in V0.1.
- Complex charting in V0.1.
- Complete native hand parser in V0.1.

## Planned Issue Themes

V0.1 issue cards should be report-driven and conservative. They may be generated from:

- Large negative session areas from H2N4 reports.
- Position results with notable losses or volume.
- Filtered hand buckets selected by the user.
- Marked hands exported by H2N4.
- Manual notes from `session_summary.yaml`.

Issue cards must distinguish:

```text
observed result
source file
why it is worth reviewing
representative hands
user verdict
next study action
```

The previous `DominatedBroadway3betCall` detector is deferred until native parser or sufficiently rich filtered-hand exports are available.

## V0.1 Acceptance

V0.1 is useful when one real session can produce:

- A valid session manifest.
- A clear H2N4 import/export checklist.
- A checked H2N4 export folder with manifests.
- A source-tagged `session_summary.json`.
- Top 3 issue cards.
- A review queue.
- GTO study cards for manual off-table study.
- A Markdown session review.
- A next training focus.

Do not judge V0.1 by feature count. Judge it by whether the first report helps decide what to study next.
