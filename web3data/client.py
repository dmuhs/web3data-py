"""This module contains the main API client class."""

from web3data.chains import Chains
from web3data.handlers.api import APIHandler


class Web3Data:
    """The Amberdata API client object."""

    def __init__(self, api_key: str):
        """Return a new API client instance.

        :param api_key: The Amberdata API key to perform requests with
        """
        self.btc = APIHandler(
            api_key=api_key,
            blockchain_id="408fa195a34b533de9ad9889f076045e",
            chain=Chains.BTC,
        )
        self.bch = APIHandler(
            api_key=api_key,
            blockchain_id="43b45e71cc0615b491cb699e7071fc06",
            chain=Chains.BCH,
        )
        self.bsv = APIHandler(
            api_key=api_key,
            blockchain_id="a818635d36dbe125e26167c4438e2217",
            chain=Chains.BSV,
        )
        self.eth = APIHandler(
            api_key=api_key, blockchain_id="1c9c969065fcd1cf", chain=Chains.ETH
        )
        self.eth_rinkeby = APIHandler(
            api_key=api_key,
            blockchain_id="1b3f7a72b3e99c13",
            chain=Chains.ETH_RINKEBY,
        )
        self.ltc = APIHandler(
            api_key=api_key,
            blockchain_id="f94be61fd9f4fa684f992ddfd4e92272",
            chain=Chains.LTC,
        )
        self.zec = APIHandler(
            api_key=api_key,
            blockchain_id="b7d4f994f33c709be4ce6cbae31d7b8e",
            chain=Chains.ZEC,
        )
