"""Requirement-based validation and negative-path integration tests."""

from helpers.assertions import (
    assert_reply_contains,
    assert_reply_has_success_shape,
    assert_reply_received,
    assert_server_alive,
)
from helpers.commands import add_phone_user_cmd, sign_in_cmd, sign_up_cmd
from helpers.server import run_command_batch


def test_missing_phone_number_returns_controlled_validation_error(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        [
            sign_up_cmd("owner", "1234", "owner@example.com"),
            sign_in_cmd("owner", "1234"),
            {"command_name": "add_phone_user", "parameters": {"username": "ali"}},
        ],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "phone_number")
    finally:
        session.server.stop()
