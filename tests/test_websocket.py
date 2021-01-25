import json
from json.decoder import JSONDecodeError
from types import FunctionType
from unittest.mock import Mock

import pytest

from web3data.exceptions import APIError
from web3data.handlers.websocket import WebsocketHandler

DATA_RESPONSE = json.dumps(
    {
        "jsonrpc": "2.0",
        "method": "subscription",
        "params": {
            "result": {
                "blockchainId": "1c9c969065fcd1cf",
                "number": 7452758,
                "hash": "0x087ad0362e03cc781b2f252333d68caa52575bc72976d6350d7608561c57770a",
            },
            "subscription": "e0b0f42177341bff16987e1b12904d7dc8a6e4417dee0291fa134b5044763482",
        },
    }
)

SUBSCRIPTION_RESPONSE = json.dumps(
    {
        "jsonrpc": "2.0",
        "id": 1,
        "result": "242d29d5c0ec9268f51a39aba4ed6a36c757c03c183633568edb0531658a9799",
    }
)
UNSUBSCRIPTION_RESPONSE = json.dumps({"jsonrpc": "2.0", "id": 1, "result": True})
UNKNOWN_RESPONSE = json.dumps(
    {"jsonrpc": "2.0", "id": 1, "result": {"invalid": "datatype"}}
)


def get_handler():
    handler = WebsocketHandler("test-key", "test-id")
    handler._websocket_send = Mock()
    return handler


def assert_handler_initialized(handler: WebsocketHandler):
    assert handler.url == "wss://ws.web3api.io/"
    assert not handler.expected_ids
    assert handler.external_registry == {}
    assert handler.internal_registry == {}


def test_register():
    handler = get_handler()
    assert_handler_initialized(handler)

    handler.register("test", lambda: None)
    internal_entry = list(handler.internal_registry.values())[0]

    assert handler.expected_ids
    assert handler.external_registry == {}
    assert handler.internal_registry != {}
    assert type(internal_entry["callback"]) == FunctionType
    assert internal_entry["payload"]["jsonrpc"] == "2.0"
    assert internal_entry["payload"]["method"] == "subscribe"
    assert internal_entry["payload"]["params"] == ("test",)


def test_unregister():
    handler = get_handler()
    assert_handler_initialized(handler)

    handler.internal_registry["internal-id"] = {"important": "things"}
    handler.external_registry["external-id"] = "internal-id"
    handler.unregister("external-id")

    assert not handler.internal_registry
    assert not handler.external_registry
    assert len(handler.expected_ids) == 1
    handler._websocket_send.assert_called_once()


def test_on_message_data():
    handler = get_handler()
    callback_mock = Mock()
    assert_handler_initialized(handler)

    # mock the registration callback
    handler.register("test", callback_mock)
    # connect external to internal ID
    handler.external_registry[
        "e0b0f42177341bff16987e1b12904d7dc8a6e4417dee0291fa134b5044763482"
    ] = list(handler.internal_registry.keys())[0]

    handler._on_message(None, DATA_RESPONSE)

    callback_mock.assert_called_with(None, json.loads(DATA_RESPONSE))


def test_on_message_subscription():
    handler = get_handler()
    assert_handler_initialized(handler)
    # add request ID to expected responses
    handler.expected_ids = {1}

    handler._on_message(None, SUBSCRIPTION_RESPONSE)

    # acknowledges, we don't expect another internal ID to come in
    assert handler.expected_ids == set()
    # successfully linked external to internal ID
    assert (
        handler.external_registry[
            "242d29d5c0ec9268f51a39aba4ed6a36c757c03c183633568edb0531658a9799"
        ]
        == 1
    )


def test_on_message_unsubscription():
    handler = get_handler()
    assert_handler_initialized(handler)
    # add request ID to expected responses
    handler.expected_ids = {1}

    handler._on_message(None, UNSUBSCRIPTION_RESPONSE)

    # acknowledges, we don't expect another internal ID to come in
    assert handler.expected_ids == set()


def test_on_message_unknown():
    handler = get_handler()
    assert_handler_initialized(handler)

    with pytest.raises(APIError):
        handler._on_message(None, UNKNOWN_RESPONSE)


def test_on_message_invalid():
    handler = get_handler()
    assert_handler_initialized(handler)

    with pytest.raises(JSONDecodeError):
        handler._on_message(None, "invalid")


@pytest.mark.parametrize(
    "hook,args",
    (("on_open", (None,)), ("on_close", (None,)), ("on_error", (None, None))),
)
def test_custom_callbacks(hook, args):
    handler = get_handler()
    setattr(handler, hook, Mock())

    # simulate callbacks from websocket client
    getattr(handler, f"_{hook}")(*args)

    getattr(handler, hook).assert_called_with(*args)


def test_subscriptions_on_open():
    handler = get_handler()
    mock_callback = Mock()
    assert_handler_initialized(handler)

    handler.register(("test", "foo"), mock_callback)

    handler._on_open(None)

    handler._websocket_send.assert_called_once()


def test_error_on_open():
    handler = get_handler()
    assert_handler_initialized(handler)

    # subscription without payload
    handler.internal_registry[1] = {}

    with pytest.raises(ValueError):
        handler._on_open(None)
