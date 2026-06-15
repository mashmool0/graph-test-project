"""Shared assertions for server reply shape and process state."""


def assert_server_alive(proc):
    assert proc.poll() is None, "expected server to remain alive"


def assert_server_stopped(proc):
    assert proc.poll() is not None, "expected server to have stopped"


def assert_reply_is_string(reply):
    assert isinstance(reply, str), f"expected string reply, got {type(reply)!r}"


def assert_reply_contains(reply, text):
    assert text in reply, f"expected {text!r} in reply: {reply!r}"


def assert_reply_has_success_shape(reply_text):
    assert '"command_name"' in reply_text, f"missing command_name in reply: {reply_text!r}"
    assert '"result"' in reply_text, f"missing result in reply: {reply_text!r}"
