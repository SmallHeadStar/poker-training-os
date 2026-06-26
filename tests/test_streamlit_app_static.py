from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_streamlit_app_compiles_and_uses_session_import_pipeline() -> None:
    app_path = ROOT / "streamlit_app.py"
    source = app_path.read_text(encoding="utf-8")

    compile(source, str(app_path), "exec")
    assert "run_session_import" in source
    assert "Hero screen name" in source
    assert "hero_name=hero_name" in source
    assert "implemented_provisional" not in source
    assert "provisional until same-sample H2N4 baseline comparison passes" in source
