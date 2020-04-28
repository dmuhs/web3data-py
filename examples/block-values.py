from os import environ

from web3data import Web3Data


def block_handler(ws, message):
    block_number = message["params"]["result"]["number"]
    tx_records = w3d.eth.block.transactions(
        block_id=message["params"]["result"]["hash"],
        currency="usd",
        includePrice="true",
    )["payload"]["records"]
    tx_values = [
        float(tx.get("price", {}).get("value", {}).get("quote", 0)) for tx in tx_records
    ]
    print("{:15}${:.2f}".format(str(block_number), sum(tx_values)))


w3d = Web3Data(environ.get("AMBERDATA_API_KEY", ""))
w3d.eth.websocket.on_open = lambda ws: print("{:15}{}".format("Block", "Value"))
w3d.eth.websocket.register("block", block_handler)
w3d.eth.websocket.run()
