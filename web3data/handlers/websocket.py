"""This module implements the websocket handler."""

from typing import List, Tuple


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

    def subscribe(
        self,
        params: List[Tuple],
        json_rpc: str = "2.0",
        method: str = "subscribe",
        msg_id: int = 0,
        # TODO: add params for callbacks
    ):
        """Subscribe to one or multiple websocket topics.

        :param params: A list of tuples, each containing parameters to subscribe to
        :param json_rpc: The JSON RPC version
        :param method: The method to trigger on the websocket server
        :param msg_id: Client-generated ID to attach to the request
        """
        raise NotImplementedError(
            "Websocket integration is not supported yet."
        )
