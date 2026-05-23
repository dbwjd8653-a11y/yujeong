import pytest


def run(file: str) -> None:
    pytest.main([file, "-v", "-s"])
