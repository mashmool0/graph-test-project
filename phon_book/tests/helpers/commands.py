"""Reusable command payload builders for client/server integration tests."""


def sign_up_cmd(username, password, email):
    return {
        "command_name": "sign_up",
        "parameters": {
            "username": username,
            "password": password,
            "email": email,
        },
    }


def sign_in_cmd(username, password):
    return {
        "command_name": "sign_in",
        "parameters": {
            "username": username,
            "password": password,
        },
    }


def logout_cmd(username):
    return {
        "command_name": "logout",
        "parameters": {
            "username": username,
        },
    }


def add_phone_user_cmd(username, phone_number, explanation=None):
    params = {
        "username": username,
        "phone_number": phone_number,
    }
    if explanation is not None:
        params["explanation"] = explanation
    return {
        "command_name": "add_phone_user",
        "parameters": params,
    }


def remove_phone_user_cmd(username):
    return {
        "command_name": "remove_phone_user",
        "parameters": {
            "username": username,
        },
    }


def edit_phone_user_cmd(username, phone_number, new_username, new_phone_number):
    return {
        "command_name": "edit_phone_user",
        "parameters": {
            "username": username,
            "phone_number": phone_number,
            "new_username": new_username,
            "new_phone_number": new_phone_number,
        },
    }


def add_phone_number_cmd(username, phone_number):
    return {
        "command_name": "add_phone_number",
        "parameters": {
            "username": username,
            "phone_number": phone_number,
        },
    }


def get_all_phone_users_cmd():
    return {
        "command_name": "get_all_phone_users",
        "parameters": {},
    }


def get_phone_user_by_name_cmd(username):
    return {
        "command_name": "get_phone_user_by_name",
        "parameters": {
            "username": username,
        },
    }


def get_phone_user_by_number_cmd(phone_number):
    return {
        "command_name": "get_phone_user_by_number",
        "parameters": {
            "phone_number": phone_number,
        },
    }
