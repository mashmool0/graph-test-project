"""Requirement-based authorization and access-control integration tests."""

from helpers.assertions import (
    assert_reply_contains,
    assert_reply_has_success_shape,
    assert_reply_received,
    assert_server_alive,
)
from helpers.commands import add_phone_user_cmd, get_all_phone_users_cmd, sign_in_cmd, sign_up_cmd
from helpers.server import run_command_batch


def test_contact_creation_requires_authentication(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        [
            sign_up_cmd("owner", "1234", "owner@example.com"),
            add_phone_user_cmd("ali", "12092"),
        ],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "auth")
    finally:
        session.server.stop()


def test_contact_list_requires_authentication(clean_workspace, python_bin):
    setup_session = run_command_batch(
        clean_workspace,
        python_bin,
        [
            sign_up_cmd("owner", "1234", "owner@example.com"),
            sign_in_cmd("owner", "1234"),
            add_phone_user_cmd("ali", "12092"),
        ],
    )
    try:
        assert_reply_received(setup_session.result)
    finally:
        setup_session.server.stop()

    session = run_command_batch(
        clean_workspace,
        python_bin,
        [get_all_phone_users_cmd()],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "auth")
    finally:
        session.server.stop()
