"""Requirement-based phonebook core integration tests."""

from helpers.assertions import (
    assert_reply_contains,
    assert_reply_has_success_shape,
    assert_reply_received,
    assert_server_alive,
)
from helpers.commands import (
    add_phone_number_cmd,
    add_phone_user_cmd,
    edit_phone_user_cmd,
    get_all_phone_users_cmd,
    get_phone_user_by_name_cmd,
    get_phone_user_by_number_cmd,
    remove_phone_user_cmd,
    sign_in_cmd,
    sign_up_cmd,
)
from helpers.server import run_command_batch


def authenticated_owner_setup():
    return [
        sign_up_cmd("owner", "1234", "owner@example.com"),
        sign_in_cmd("owner", "1234"),
    ]


def test_first_phonebook_operation_after_auth_on_clean_db_succeeds(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        authenticated_owner_setup() + [add_phone_user_cmd("ali", "12092")],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "phone user ali added successfully")
    finally:
        session.server.stop()


def test_duplicate_contact_name_is_rejected_without_server_failure(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        authenticated_owner_setup()
        + [
            add_phone_user_cmd("ali", "12092"),
            add_phone_user_cmd("ali", "77777"),
        ],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "exist")
    finally:
        session.server.stop()


def test_duplicate_phone_number_is_rejected_without_server_failure(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        authenticated_owner_setup()
        + [
            add_phone_user_cmd("ali", "12092"),
            add_phone_user_cmd("reza", "12092"),
        ],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "phone")
    finally:
        session.server.stop()


def test_add_phone_number_to_missing_contact_returns_controlled_not_found_result(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        authenticated_owner_setup() + [add_phone_number_cmd("ghost", "9999")],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "not")
    finally:
        session.server.stop()


def test_create_new_contact_with_initial_phone_number_succeeds(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        authenticated_owner_setup() + [add_phone_user_cmd("ali", "12092", "friend")],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "phone user ali added successfully")
    finally:
        session.server.stop()


def test_add_second_phone_number_to_existing_contact_succeeds(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        authenticated_owner_setup()
        + [
            add_phone_user_cmd("ali", "12092"),
            add_phone_number_cmd("ali", "44653112"),
        ],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "44653112")
    finally:
        session.server.stop()


def test_get_all_contacts_returns_existing_data(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        authenticated_owner_setup()
        + [
            add_phone_user_cmd("ali", "12092"),
            get_all_phone_users_cmd(),
        ],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "ali")
        assert_reply_contains(session.result.reply, "12092")
    finally:
        session.server.stop()


def test_get_existing_contact_by_name_returns_contact(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        authenticated_owner_setup()
        + [
            add_phone_user_cmd("ali", "12092"),
            get_phone_user_by_name_cmd("ali"),
        ],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "ali")
        assert_reply_contains(session.result.reply, "12092")
    finally:
        session.server.stop()


def test_get_existing_contact_by_phone_number_returns_contact(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        authenticated_owner_setup()
        + [
            add_phone_user_cmd("ali", "12092"),
            get_phone_user_by_number_cmd("12092"),
        ],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "ali")
        assert_reply_contains(session.result.reply, "12092")
    finally:
        session.server.stop()


def test_edit_only_contact_name_succeeds(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        authenticated_owner_setup()
        + [
            add_phone_user_cmd("ali", "12092"),
            edit_phone_user_cmd("ali", "12092", "ali_updated", "12092"),
            get_phone_user_by_name_cmd("ali_updated"),
        ],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "ali_updated")
        assert_reply_contains(session.result.reply, "12092")
    finally:
        session.server.stop()


def test_edit_only_phone_number_succeeds(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        authenticated_owner_setup()
        + [
            add_phone_user_cmd("ali", "12092"),
            edit_phone_user_cmd("ali", "12092", "ali", "66056477"),
            get_phone_user_by_number_cmd("66056477"),
        ],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "ali")
        assert_reply_contains(session.result.reply, "66056477")
    finally:
        session.server.stop()


def test_edit_contact_name_and_phone_number_together_succeeds(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        authenticated_owner_setup()
        + [
            add_phone_user_cmd("ali", "12092"),
            edit_phone_user_cmd("ali", "12092", "ali_updated", "66056477"),
            get_phone_user_by_name_cmd("ali_updated"),
            get_phone_user_by_number_cmd("66056477"),
        ],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "ali_updated")
        assert_reply_contains(session.result.reply, "66056477")
    finally:
        session.server.stop()


def test_delete_existing_contact_removes_it(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        authenticated_owner_setup()
        + [
            add_phone_user_cmd("ali", "12092"),
            remove_phone_user_cmd("ali"),
            get_phone_user_by_name_cmd("ali"),
        ],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "removed")
        assert_reply_contains(session.result.reply, "not")
    finally:
        session.server.stop()


def test_get_non_existing_contact_by_name_returns_not_found(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        authenticated_owner_setup() + [get_phone_user_by_name_cmd("ghost")],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "not")
    finally:
        session.server.stop()


def test_get_non_existing_contact_by_phone_number_returns_not_found(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        authenticated_owner_setup() + [get_phone_user_by_number_cmd("99999999")],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "not")
    finally:
        session.server.stop()


def test_delete_non_existing_contact_returns_controlled_result(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        authenticated_owner_setup() + [remove_phone_user_cmd("ghost")],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "not")
    finally:
        session.server.stop()


def test_edit_non_existing_contact_returns_controlled_not_found_result(clean_workspace, python_bin):
    session = run_command_batch(
        clean_workspace,
        python_bin,
        authenticated_owner_setup() + [edit_phone_user_cmd("ghost", "11111", "ghost2", "22222")],
    )
    try:
        assert_reply_received(session.result)
        assert_server_alive(session.server)
        assert_reply_has_success_shape(session.result.reply)
        assert_reply_contains(session.result.reply, "not")
    finally:
        session.server.stop()
