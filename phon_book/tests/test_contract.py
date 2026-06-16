"""Requirement-based response-contract and error-handling integration tests."""

from helpers.assertions import (
    assert_reply_contains,
    assert_reply_has_success_shape,
    assert_reply_received,
    assert_server_alive,
)
from helpers.commands import sign_up_cmd
from helpers.server import run_command_batch


def test_success_reply_contains_command_name_and_result(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        [sign_up_cmd("contract_ok", "1234", "contract_ok@example.com")],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
    finally:
        session.server.stop()


def test_duplicate_username_failure_returns_structured_error_and_keeps_server_alive(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        [
            sign_up_cmd("contract_dup", "1234", "c1@example.com"),
            sign_up_cmd("contract_dup", "1234", "c2@example.com"),
        ],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "username")
    finally:
        session.server.stop()


def test_invalid_request_does_not_kill_server(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        [{"command_name": "sign_up", "parameters": {"password": "1234", "email": "m@example.com"}}],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
    finally:
        session.server.stop()


def test_error_output_does_not_leak_internal_details(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        [
            sign_up_cmd("contract_dup", "1234", "c1@example.com"),
            sign_up_cmd("contract_dup", "1234", "c2@example.com"),
        ],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert 'UNIQUE constraint failed' not in session.result.reply
        assert 'Traceback' not in session.result.reply
        assert 'SQL:' not in session.result.reply
    finally:
        session.server.stop()
