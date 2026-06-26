# Local Run Guide

## Environment

Use Python with the project `src` directory on `PYTHONPATH`.

In this Codex workspace the bundled Python is:

```powershell
C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe
```

The temporary dependency directory used in this workspace is:

```powershell
work\python-packages
```

## Generate artifacts from a GG PokerCraft export

```powershell
$env:PYTHONPATH = "work\python-packages;src"
C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m poker_training_os import-session tests\fixtures\gg_pokercraft_cash_hand.txt outputs\demo_session
```

If the export does not expose Hero private cards clearly enough for automatic inference, provide the exact screen name:

```powershell
$env:PYTHONPATH = "work\python-packages;src"
C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m poker_training_os import-session path\to\gg_export.txt outputs\my_session --hero-name YourScreenName
```

This writes:

- `canonical_hands.json`
- `poker_training.duckdb`
- `session_review.md`
- `session_summary.json`
- `basic_reports.csv`
- `loss_map.csv`
- `issue_cards.json`
- `review_queue.csv`
- `gto_study_cards.md`
- `training_cycle_update.json`

All H2N4-like analytical values remain `implemented_provisional` until same-sample H2N4 baseline comparison passes.

## Run the Streamlit app

```powershell
$env:PYTHONPATH = "work\python-packages;src"
C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m streamlit run streamlit_app.py --global.developmentMode false --server.port 8501 --server.headless true
```

Then open:

```text
http://localhost:8501
```

The app can import the included sample or a local GG PokerCraft export path. The optional Hero screen name field is only needed when automatic Hero inference is not reliable. It then displays session summary, basic reports, loss map, issue cards, review queue, and provisional parity status.

## Validate an H2N4 baseline package

```powershell
$env:PYTHONPATH = "work\python-packages;src"
C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m poker_training_os validate-h2n4-package path\to\h2n4_baseline_package
```

Schema validation does not prove H2N4 parity. It only checks that the evidence package has the required manifest and CSV columns.

## Compare basic reports against H2N4

```powershell
$env:PYTHONPATH = "work\python-packages;src"
C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m poker_training_os validate-h2n4 outputs\demo_session\basic_reports.csv path\to\h2n4_basic_reports_baseline.csv
```

Counts must match exactly. Rounded values use explicit tolerance.
