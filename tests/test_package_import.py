def test_package_import_smoke() -> None:
    import poker_training_os

    assert poker_training_os.__version__ == "0.1.0"
