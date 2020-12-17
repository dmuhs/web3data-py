"""Unit test package for web3data."""

from web3data.chains import Chains

API_PREFIX = "https://web3api.io/api/v2/"
HEADERS = {"foo": "bar", "baz": "qux"}
RESPONSE = {"test": "data"}
CHAINS = (
    Chains.BTC,
    Chains.BCH,
    Chains.BSV,
    Chains.ETH,
    Chains.ETH_RINKEBY,
    Chains.LTC,
    Chains.ZEC,
)
