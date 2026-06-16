"""Shared assertions for server reply shape and process state."""

import json


def assert_server_alive(server):
    assert server.is_alive(), "expected server to remain alive"



def assert_server_stopped(server):
    assert not server.is_alive(), "expected server to have stopped"



def assert_reply_received(result):
    assert result.received, "expected a reply from server"



def assert_reply_is_string(reply):
    assert isinstance(reply, str), f"expected string reply, got {type(reply)!r}"



def assert_reply_contains(reply, text):
    assert text in reply, f"expected {text!r} in reply: {reply!r}"



def assert_reply_has_success_shape(reply_text):
    # The server double-encodes the batch result, so recv_json gives back a JSON
    # *string*. Decode it and check the documented {command_name, result} contract
    # for real, instead of only looking for substrings (which can pass even on a
    # malformed or error payload).
    try:
        payload = json.loads(reply_text)
    except (TypeError, ValueError):
        raise AssertionError(f"reply is not a JSON document: {reply_text!r}")
    assert isinstance(payload, list), f"expected a list of results, got {reply_text!r}"
    assert payload, f"expected at least one result object, got {reply_text!r}"
    for item in payload:
        assert isinstance(item, dict), f"expected result objects, got {item!r}"
        assert "command_name" in item, f"missing command_name in {item!r}"
        assert "result" in item, f"missing result in {item!r}"
