"""Shared pytest fixtures for the phon_book test suite."""

import sys
from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).resolve().parent
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from helpers.server import make_isolated_workspace, remove_db


@pytest.fixture
def project_root():
    return Path(__file__).resolve().parents[1]


@pytest.fixture
def python_bin(project_root):
    return str(project_root / ".venv" / "bin" / "python")


@pytest.fixture
def isolated_workspace(project_root, tmp_path):
    return make_isolated_workspace(project_root, tmp_path)


@pytest.fixture
def clean_workspace(isolated_workspace):
    remove_db(isolated_workspace)
    return isolated_workspace
