from binascii import unhexlify
import requests
from pymongo.cursor import Cursor
from .models import Transaction, Asset, Input, UTXO, AssetInfo
from typing import List

LOVELACE = 1000000


def create_transaction_object(oura_transaction: dict) -> Transaction:
    tx_data = oura_transaction['transaction']
    outputs = []
    for output in tx_data['outputs']:
        assets = []
        for asset in output['assets']:
            assets.append(Asset(**asset))
        del output['assets']
        outputs.append(UTXO(**output, assets=assets))

    inputs = [Input(**input) for input in tx_data['inputs']]

    del oura_transaction['transaction']['outputs']
    del oura_transaction['transaction']['inputs']

    transaction = Transaction(**oura_transaction['transaction'], outputs=outputs, inputs=inputs, timestamp=oura_transaction['timestamp'])
    return transaction


def get_decimals(asset_info: AssetInfo):
    if(
        'metadata' in asset_info
        and asset_info['metadata']
        and 'decimals' in asset_info['metadata']
    ):
        return asset_info['metadata']['decimals']
    else:
        return 0


def get_asset_name(asset_info: AssetInfo):
 
    if asset_info['asset_name']:
        name = unhexlify(asset_info['asset_name']).decode()
    else:
        name = 'Unknown'
    return name


def get_transactions(address: str, metadata: str, oura_transactions_collection: Cursor) -> List[Transaction]:
    query = {
        "transaction.outputs.address": address, 
        "transaction.metadata.map_json.msg": metadata
        }
    result = oura_transactions_collection.find(query)
    return [create_transaction_object(tx) for tx in result]