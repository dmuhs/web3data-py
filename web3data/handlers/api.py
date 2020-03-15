"""This module contains the main API handler class."""

from web3data import __version__
from web3data.chains import Chains
from web3data.handlers.address import AddressHandler
from web3data.handlers.block import BlockHandler
from web3data.handlers.contract import ContractHandler
from web3data.handlers.market import MarketHandler
from web3data.handlers.signature import SignatureHandler
from web3data.handlers.token import TokenHandler
from web3data.handlers.transaction import TransactionHandler


class APIHandler:
    """The API handler object for client requests."""

    def __init__(self, api_key: str, blockchain_id: str, chain: Chains):
        """Return a new API handler instance.

        :param api_key: The API key to attach to request headers
        :param blockchain_id: The ID of the blockchain to query for
        :param chain: The enum value for the blockchain to query for
        """

        self.api_key = api_key
        self.blockchain_id = blockchain_id
        self.chain = chain

        # TODO: Validation
        headers = {
            "x-api-key": self.api_key,
            "x-amberdata-blockchain-id": self.blockchain_id,
            "User-Agent": f"web3data-py v{__version__}",
        }
        self.address = AddressHandler(headers, chain)
        self.token = TokenHandler(headers, chain)
        self.contract = ContractHandler(headers, chain)
        self.transaction = TransactionHandler(headers, chain)
        self.block = BlockHandler(headers, chain)
        self.signature = SignatureHandler(headers, chain)
        self.market = MarketHandler(headers, chain)
