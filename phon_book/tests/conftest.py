"""Shared pytest fixtures for the phon_book test suite."""

from pathlib import Path

import pytest

from tests.helpers.server import (
    DEFAULT_IP,
    DEFAULT_PORT,
    make_isolated_workspace,
    remove_db,
    start_server,
)


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


@pytest.fixture

def server_runner(clean_workspace, python_bin):
    server = start_server(clean_workspace, python_bin, ip=DEFAULT_IP, port=DEFAULT_PORT)
    try:
        yield server
    finally:
        server.stop()
