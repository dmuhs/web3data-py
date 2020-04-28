from os import environ

from web3data import Web3Data

w3d = Web3Data(environ.get("AMBERDATA_API_KEY", ""))
result = w3d.eth.rpc("eth_gasPrice", []).get("result")

if result is None:
    print("Unable to get the current gas price")
else:
    print(f"The current gas price is at {int(result, 16):,} wei")
