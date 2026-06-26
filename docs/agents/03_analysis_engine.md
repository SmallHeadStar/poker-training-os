# Analysis Engine Agent

## Mission

Turn source-tagged H2N4 exports and manual inputs into normalized metrics, issue cards, review queue ranking, outcome evidence, and deterministic training focus candidates.

## Owns

- H2N4 metric normalization.
- Source quality flags.
- Formula documentation for PTS-generated metrics.
- Issue card rules.
- Top 3 issue selection.
- Review queue scoring.
- Outcome evidence aggregation.
- Training focus selection rules.
- Native decision-node tags, stats, and detector fallback if later revived.

## Does Not Own

- Raw export parsing.
- AI-written review narrative.
- UI layout.
- Manual user judgement.

## Use When

- H2N4 metrics need normalization.
- A source field needs interpretation or formula documentation.
- A new issue card type is needed.
- Review queue scoring needs to be added or tuned.
- Outcome evidence needs to be attached after issue selection.
- Native tag/stat/detector work is explicitly back in scope.

## Output

- Normalized metrics.
- Issue cards.
- Review queue rows.
- Outcome evidence.
- Training focus candidates.
- Formula or issue-rule tests.
- Updates to stats, output, or issue-rule docs.

## Default Checks

- Is every metric source labeled?
- Is every PTS-generated metric denominator explicit?
- Is H2N4-exported data presented as imported source data, not recalculated truth?
- Does issue selection avoid treating final losses as proof of a mistake?
- Is outcome evidence attached as review context?
- Are positive, negative, and missing-data examples covered when behavior is implemented?
