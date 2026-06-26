from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_product_and_agents_files_exist_as_controller_sources() -> None:
    assert (ROOT / "PRODUCT.md").exists()
    assert (ROOT / "AGENTS.md").exists()


def test_controller_status_preserves_product_priority_and_provisional_rule() -> None:
    status = (ROOT / "docs" / "controller_status.md").read_text(encoding="utf-8")

    assert "`PRODUCT.md` is the highest-priority product definition" in status
    assert "Do not expand later-phase feature breadth" in status
    assert "No analytical feature can move from `provisional` to `complete`" in status

