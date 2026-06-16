"""Requirement-based authentication integration tests for Wave 1 and Wave 2 cases."""

from helpers.assertions import (
    assert_reply_contains,
    assert_reply_has_success_shape,
    assert_reply_is_string,
    assert_reply_received,
    assert_server_alive,
)
from helpers.commands import logout_cmd, sign_in_cmd, sign_up_cmd
from helpers.server import run_command_batch


# Cant Handle Errors and Server Will Crash
def test_sign_up_success_returns_structured_result(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        [sign_up_cmd("new_user", "1234", "new_user@example.com")],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "user new_user added successfully")
    finally:
        session.server.stop()


def test_sign_in_success_returns_structured_result(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        [
            sign_up_cmd("amir", "1234", "amir@example.com"),
            sign_in_cmd("amir", "1234"),
        ],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "user amir signed in successfully")
    finally:
        session.server.stop()


def test_login_by_email_is_supported_as_required(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        [
            sign_up_cmd("amir", "1234", "amir@example.com"),
            sign_in_cmd("amir@example.com", "1234"),
        ],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "signed in successfully")
    finally:
        session.server.stop()


def test_duplicate_email_registration_is_rejected(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        [
            sign_up_cmd("user_a", "1234", "same@example.com"),
            sign_up_cmd("user_b", "1234", "same@example.com"),
        ],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "email")
        assert_reply_contains(session.result.reply, "exist")
    finally:
        session.server.stop()


def test_duplicate_username_is_rejected_without_server_failure(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        [
            sign_up_cmd("dup", "1234", "dup1@example.com"),
            sign_up_cmd("dup", "1234", "dup2@example.com"),
        ],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "username")
        assert_reply_contains(session.result.reply, "exist")
    finally:
        session.server.stop()


def test_invalid_email_is_rejected(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        [sign_up_cmd("user_bad_email", "1234", "abc")],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "email")
        assert_reply_contains(session.result.reply, "invalid")
    finally:
        session.server.stop()


def test_wrong_password_is_rejected_without_server_failure(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        [
            sign_up_cmd("amir", "1234", "amir@example.com"),
            sign_in_cmd("amir", "wrong123"),
        ],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "wrong password")
    finally:
        session.server.stop()


def test_logout_success_returns_structured_result(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        [
            sign_up_cmd("amir", "1234", "amir@example.com"),
            sign_in_cmd("amir", "1234"),
            logout_cmd("amir"),
        ],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "user amir signed out successfully")
    finally:
        session.server.stop()


def test_missing_signup_username_returns_controlled_validation_error(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        [{"command_name": "sign_up", "parameters": {"password": "1234", "email": "m@example.com"}}],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "username")
    finally:
        session.server.stop()


def test_non_string_password_returns_controlled_validation_error(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        [{"command_name": "sign_up",
          "parameters": {"username": "typed", "password": 1234, "email": "typed@example.com"}}],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "password")
    finally:
        session.server.stop()
