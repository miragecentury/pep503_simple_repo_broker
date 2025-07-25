"""Test file for main."""

import importlib


class TestMain:
    """Test main."""

    def test_file_main_exist(self) -> None:
        """Test main file exists."""
        module = importlib.import_module("__main__", "pep503_simple_repo_broker")
        assert module is not None

    def test_main_exists(self) -> None:
        """Test that main exists."""
        from pep503_simple_repo_broker.__main__ import main  # noqa: PLC0415 # pylint: disable=import-outside-toplevel

        assert main is not None
