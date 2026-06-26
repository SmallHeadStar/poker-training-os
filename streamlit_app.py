from __future__ import annotations

from pathlib import Path

import streamlit as st

from poker_training_os.dashboard.data import load_session_dashboard
from poker_training_os.pipeline import run_session_import


st.set_page_config(page_title="poker-training-os", layout="wide")

st.markdown(
    """
    <style>
    .block-container { padding-top: 1.5rem; }
    .metric-band {
      border: 1px solid #233044;
      border-radius: 8px;
      padding: 12px 14px;
      background: #111827;
      min-height: 86px;
    }
    .metric-label { color: #93a4b8; font-size: 0.78rem; margin-bottom: 8px; }
    .metric-value { color: #f8fafc; font-size: 1.35rem; font-weight: 650; }
    .badge {
      display: inline-block;
      padding: 2px 8px;
      border-radius: 999px;
      font-size: 0.75rem;
      border: 1px solid #334155;
      background: #0b1220;
      color: #cbd5e1;
      margin-right: 6px;
    }
    .badge-high { color: #86efac; border-color: #166534; }
    .badge-medium { color: #fde68a; border-color: #854d0e; }
    .badge-low { color: #fca5a5; border-color: #7f1d1d; }
    </style>
    """,
    unsafe_allow_html=True,
)


ROOT = Path(__file__).parent
default_dir = ROOT / "outputs" / "demo_session"
default_fixture = ROOT / "tests" / "fixtures" / "gg_pokercraft_cash_hand.txt"


def _metric(column, label: str, value) -> None:
    column.markdown(
        f"<div class='metric-band'><div class='metric-label'>{label}</div>"
        f"<div class='metric-value'>{value}</div></div>",
        unsafe_allow_html=True,
    )


with st.sidebar:
    section = st.radio(
        "Navigation",
        ["Session Summary", "Basic Reports", "Loss Map", "Issue Cards", "Review Queue / Training Focus"],
        label_visibility="collapsed",
    )
    artifact_input = st.text_input("Artifact directory", value=str(default_dir))
    hh_input = st.text_input("GG PokerCraft export", value=str(default_fixture))
    hero_name_input = st.text_input("Hero screen name", value="", placeholder="Optional")
    hero_name = hero_name_input.strip() or None
    import_col, sample_col = st.columns(2)
    if import_col.button("Import"):
        try:
            run_session_import(Path(hh_input), Path(artifact_input), hero_name=hero_name)
            st.success("Imported")
        except Exception as exc:
            st.error(f"Import failed: {exc}")
    if sample_col.button("Sample"):
        try:
            run_session_import(default_fixture, Path(artifact_input))
            st.success("Sample imported")
        except Exception as exc:
            st.error(f"Sample failed: {exc}")

artifact_dir = Path(artifact_input)
dashboard = load_session_dashboard(artifact_dir)

st.title("poker-training-os")
st.caption("Post-session personal training review · provisional until same-sample H2N4 baseline comparison passes")

if dashboard["missing_files"]:
    st.warning("Missing session artifacts: " + ", ".join(dashboard["missing_files"]))

if section == "Session Summary":
    summary = dashboard["session_summary"]
    cols = st.columns(4)
    _metric(cols[0], "Hands", summary.get("hands", 0))
    _metric(cols[1], "Total bb", summary.get("total_profit_bb", 0))
    _metric(cols[2], "BB/100", summary.get("bb_per_100", 0))
    _metric(cols[3], "Issues", len(dashboard["issue_cards"]))
    parity = dashboard["training_cycle_update"].get("parity_status", {})
    if parity:
        st.info(
            f"Parity status: {parity.get('overall')} · "
            f"{parity.get('provisional_item_count', 0)} provisional items require H2N4 baseline evidence."
        )
    st.subheader("Session Review")
    st.markdown(dashboard["session_review"] or "No session review loaded.")

elif section == "Basic Reports":
    st.subheader("Basic Reports")
    st.dataframe(dashboard["basic_reports"], use_container_width=True, hide_index=True)

elif section == "Loss Map":
    st.subheader("Loss Map")
    st.dataframe(dashboard["loss_map"], use_container_width=True, hide_index=True)

elif section == "Issue Cards":
    st.subheader("Issue Cards")
    if not dashboard["issue_cards"]:
        st.info("No issue cards generated.")
    for card in dashboard["issue_cards"]:
        st.markdown(f"### {card['issue_name']}")
        st.markdown(
            f"<span class='badge'>source: {card['source']}</span>"
            f"<span class='badge badge-{card['reliability']}'>reliability: {card['reliability']}</span>",
            unsafe_allow_html=True,
        )
        st.write(card["observation"])
        st.write(card["review_question"])
        st.json(card["evidence"], expanded=False)

else:
    st.subheader("Review Queue")
    st.dataframe(dashboard["review_queue"], use_container_width=True, hide_index=True)
    st.subheader("Training Focus")
    st.json(dashboard["training_cycle_update"], expanded=True)
