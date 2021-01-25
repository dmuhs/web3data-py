import pytest

from web3data.client import Web3Data
from web3data.handlers import APIHandler

CLIENT = Web3Data("test-key")


@pytest.mark.parametrize(
    "client",
    (
        CLIENT.bch,
        CLIENT.bsv,
        CLIENT.btc,
        CLIENT.eth,
        CLIENT.eth_rinkeby,
        CLIENT.ltc,
        CLIENT.zec,
    ),
)
def test_client_initialized(client):
    assert isinstance(client, APIHandler)
    assert isinstance(client, APIHandler)
    assert isinstance(client, APIHandler)
    assert isinstance(client, APIHandler)
    assert isinstance(client, APIHandler)
    assert isinstance(client, APIHandler)
    assert isinstance(client, APIHandler)
    assert isinstance(client, APIHandler)
    assert isinstance(client, APIHandler)
