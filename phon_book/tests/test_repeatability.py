"""Requirement-based repeatability and persistence integration tests."""

from helpers.assertions import (
    assert_reply_contains,
    assert_reply_has_success_shape,
    assert_reply_received,
    assert_server_alive,
)
from helpers.commands import sign_up_cmd
from helpers.server import run_command_batch


def test_repeat_run_duplicate_signup_is_handled_predictably(clean_workspace, python_bin):
    first_session = run_command_batch(
        clean_workspace,
        python_bin,
        [sign_up_cmd("repeat_user", "1234", "repeat@example.com")],
    )
    try:
        assert_reply_received(first_session.result)
        assert_server_alive(first_session.server)
        assert_reply_has_success_shape(first_session.result.reply)
    finally:
        first_session.server.stop()

    second_session = run_command_batch(
        clean_workspace,
        python_bin,
        [sign_up_cmd("repeat_user", "1234", "repeat@example.com")],
    )
    try:
        assert_reply_received(second_session.result)
        assert_server_alive(second_session.server)
        assert_reply_has_success_shape(second_session.result.reply)
        assert_reply_contains(second_session.result.reply, "exist")
    finally:
        second_session.server.stop()
