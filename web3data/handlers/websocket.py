"""This module implements the websocket handler."""

import json
from typing import Iterable, Union
from uuid import uuid4

import websocket

from web3data.exceptions import APIError


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
        """Send a message to the websocket server.

        :param payload: The payload to JSON serialize and send
        """
        self.ws.send(json.dumps(payload))  # pragma: no cover

    def register(self, params: Union[Iterable[str], str], callback=None):
        """Register a new event to listen for and its callback.

        This will subscribe to the given event identifiers and execute
        the provided callback function once the specified event is coming
        in. Please note that the listening and callback-handling routine
        only starts once the websocket client is running.

        The callback function should take two parameters:
        :code:`ws` and :code:`message`. The first parameter is the websocket
        client instance, which allows the user to update the client context.
        The latter argiment is the message, deserialized from the JSON object
        received by the websocket server.

        :param params: The event to subscribe to
        :param callback: The callback function to execute
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
        """Unregister a subscription from the websocket server.

        Given an external ID (i.e. the subscription ID), this will
        remove the subscription data including locally stored payloads
        and identifiers. It will also trigger an unsubscribe message
        for the subscription being sent to the websocket server.

        :param external_id: The subscription ID to remove
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
        """Run the websocket listening loop.

        This is a blocking endless loop that will send the subscription
        events to the websocket server, handle the responses, and then
        distribute the incoming messages across the registered callbacks.

        Any keyword arguments passed to this method are passed on to the
        websocket client's :code:`run_forever` method. Please consult the
        project's documentation for more details:
        https://pypi.org/project/websocket_client/

        :param kwargs: Additional arguments to pass to the websocket client
        """
        self.ws.run_forever(**kwargs)  # pragma: no cover

    def _on_message(self, ws, message):
        """An internal message handler to distribute responses.

        This internal callback will try to parse the incoming message and
        handle it based on whether it is a data message (in which case it will
        be routed to its respective subscription and its callback), a subscription
        acknowledgement message, or an unsubscription acknowledgement message.

        In the case of a subscription acknowledgement, the newly found subscription
        ID (aka external ID) is added to the client's mapping for future routing of
        data messages.

        In both latter cases, the given internal ID is removed from the internal
        set of messages to expect.

        :param ws: The websocket client instance
        :param message: The raw received message as serialized JSON
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
        else:
            raise APIError(f"Received unknown message: {message}")

    def _on_error(self, ws, error):
        """An internal handler for websocket errors.

        :param ws: The websocket client instance
        :param error: The error message
        """
        self.on_error(ws, error)

    def on_error(self, ws, error):
        """A user-defined handler for websocket errors.

        :param ws: The websocket client instance
        :param error: The error message
        """
        # to be overwritten by user if needed
        pass  # pragma: no cover

    def _on_close(self, ws):
        """An internal handler for websocket close events.

        :param ws: The websocket client instance
        """
        self.on_close(ws)

    def on_close(self, ws):
        """A user-defined handler for websocket close events.

        :param ws: The websocket client instance
        """
        # to be overwritten by user if needed
        pass  # pragma: no cover

    def _on_open(self, ws):
        """An internal handler for websocket open events.

        This handler will iterate over all internal identifiers
        and submit subscription a request for each. If no payload
        information can be found, a :code:`ValueError` is raised.

        After the requests have been sent, the user-defined on-open
        handler is called.

        :param ws: The websocket client instance
        """
        for internal_id in self.internal_registry.keys():
            payload = self.internal_registry.get(internal_id, {}).get("payload")
            if payload is None:
                raise ValueError(
                    f"Payload for internal ID {internal_id} does not exist"
                )
            self._websocket_send(payload)

        self.on_open(ws)

    def on_open(self, ws):
        """A user-defined handler for websocket open events.

        :param ws: The websocket client instance
        """
        # to be overwritten by user if needed
        pass  # pragma: no cover
