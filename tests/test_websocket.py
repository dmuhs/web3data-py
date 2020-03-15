import pytest

from web3data.handlers.websocket import WebsocketHandler


def test_websocket_raises():
    handler = WebsocketHandler("test-key", "test-id")
    assert handler.url == "wss://ws.web3api.io/"
    with pytest.raises(NotImplementedError):
        handler.subscribe([("foo", "bar")])
