import pytest

from web3data.chains import Chains
from web3data.handlers import APIHandler
from web3data.handlers.address import AddressHandler
from web3data.handlers.block import BlockHandler
from web3data.handlers.contract import ContractHandler
from web3data.handlers.market import MarketHandler
from web3data.handlers.signature import SignatureHandler
from web3data.handlers.token import TokenHandler
from web3data.handlers.transaction import TransactionHandler

TEST_KEY = "test-key"
TEST_ID = "test-id"


@pytest.mark.parametrize(
    "handler",
    (
        APIHandler(TEST_KEY, TEST_ID, chain=Chains.AION),
        APIHandler(TEST_KEY, TEST_ID, chain=Chains.BCH),
        APIHandler(TEST_KEY, TEST_ID, chain=Chains.BSV),
        APIHandler(TEST_KEY, TEST_ID, chain=Chains.BTC),
        APIHandler(TEST_KEY, TEST_ID, chain=Chains.ETH),
        APIHandler(TEST_KEY, TEST_ID, chain=Chains.ETH_RINKEBY),
        APIHandler(TEST_KEY, TEST_ID, chain=Chains.LTC),
        APIHandler(TEST_KEY, TEST_ID, chain=Chains.XLM),
        APIHandler(TEST_KEY, TEST_ID, chain=Chains.ZEC),
    ),
)
def test_api_handler_initialized(handler):
    assert isinstance(handler.address, AddressHandler)
    assert isinstance(handler.block, BlockHandler)
    assert isinstance(handler.contract, ContractHandler)
    assert isinstance(handler.market, MarketHandler)
    assert isinstance(handler.signature, SignatureHandler)
    assert isinstance(handler.token, TokenHandler)
    assert isinstance(handler.transaction, TransactionHandler)
