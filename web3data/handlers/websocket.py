"""This module implements the websocket handler."""

import json
from typing import Tuple, Union
from uuid import uuid4

import websocket


class WebsocketHandler:
    """The subhandler for websocket-related queries."""

    def __init__(self, api_key: str, blockchain_id: str, url: str = None):
        """Return a new :code:`WebsocketHandler` instance.

        :param api_key: The API key to attach to payloads
        :param blockchain_id: The ID of the blockchain to query for
        :param url: The websocket server URL
        """

        self.api_key = api_key
        self.blockchain_id = blockchain_id
        self.url = url or "wss://ws.web3api.io/"

        self.expected_ids = set()  # internal IDs that still need confirmation
        self.internal_registry = {}  # internal ID -> payload and callback
        self.external_registry = {}  # subscription ID -> internal ID

        self.ws = websocket.WebSocketApp(
            self.url,
            on_message=lambda ws, message: self._on_message(ws, message),
            on_error=lambda ws, message: self._on_error(ws, message),
            on_close=lambda ws: self._on_close(ws),
            on_open=lambda ws: self._on_open(ws),
            header=[
                f"x-api-key: {self.api_key}",
                f"x-amberdata-blockchain-id: {self.blockchain_id}",
            ],
        )

    def _websocket_send(self, payload):
        """

        :param payload:
        """
        self.ws.send(json.dumps(payload))

    def register(self, params: Union[Tuple[str], str], callback=None):
        """

        :param params:
        :param callback:
        """
        params = (params,) if type(params) is str else params

        internal_id = str(uuid4())
        self.expected_ids.add(internal_id)
        self.internal_registry[internal_id] = {
            "callback": callback or (lambda: None),
            "payload": {
                "id": internal_id,
                "jsonrpc": "2.0",
                "method": "subscribe",
                "params": params,
            },
        }

    def unregister(self, external_id):
        """

        :param external_id:
        """
        internal_id = self.external_registry[external_id]
        del self.internal_registry[internal_id]
        del self.external_registry[external_id]

        internal_id = str(uuid4())
        self.expected_ids.add(internal_id)
        payload = {
            "jsonrpc": "2.0",
            "method": "unsubscribe",
            "params": [external_id],
            "id": internal_id,
        }
        self._websocket_send(payload)

    def run(self, **kwargs):
        """

        :param kwargs:
        """
        self.ws.run_forever(**kwargs)

    def _on_message(self, ws, message):
        """

        :param ws:
        :param message:
        """
        message = json.loads(message)

        if message.get("params"):
            # handle data message and execute user callback
            external_id = message.get("params", {}).get("subscription")
            internal_id = self.external_registry[external_id]
            subscription = self.internal_registry[internal_id]
            callback = subscription["callback"]
            callback(ws, message)
        elif type(message.get("result")) is str:
            # handle subscription acknowledgement
            internal_id = message.get("id")
            self.external_registry[message.get("result")] = internal_id
            self.expected_ids.remove(internal_id)
        elif type(message.get("result")) is bool:
            # handle unsubscription acknowledgement
            internal_id = message.get("id")
            self.expected_ids.remove(internal_id)

    def _on_error(self, ws, error):
        """

        :param ws:
        :param error:
        """
        self.on_error(ws, error)

    def on_error(self, ws, error):
        """

        :param ws:
        :param error:
        """
        # to be overwritten by user if needed
        pass

    def _on_close(self, ws):
        """

        :param ws:
        """
        self.on_close(ws)

    def on_close(self, ws):
        """

        :param ws:
        """
        # to be overwritten by user if needed
        pass

    def _on_open(self, ws):
        """

        :param ws:
        """
        for internal_id in self.internal_registry.keys():
            payload = self.internal_registry.get(internal_id, {}).get(
                "payload"
            )
            if payload is None:
                raise ValueError(
                    f"Subscription failed: internal ID {internal_id} does not exist"
                )
            self._websocket_send(payload)

        self.on_open(ws)

    def on_open(self, ws):
        """

        :param ws:
        """
        # to be overwritten by user if needed
        pass
