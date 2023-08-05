from binascii import unhexlify
from pymongo.cursor import Cursor
from blockfrost import BlockFrostApi
import json
import requests
from .models import AssetInfo

LOVELACE = 1000000

def fix_decimals(order, decimal_places):
    
    if decimal_places != 0:
        order['price'] = int((order['price'] * 10**decimal_places) * LOVELACE)
        order['amount'] = order['amount'] / 10**decimal_places


def resolve_asset(id, assets_collection: Cursor, blockfrost_api: BlockFrostApi) -> AssetInfo:
    asset_info = [asset for asset in assets_collection.find({"asset_id": id})]
    info = None
    if len(asset_info) == 0:
        blockfrostasset_id = id.replace('.', '') 
        info = blockfrost_api.asset(blockfrostasset_id, return_type='json')
        info['asset_id'] = info['policy_id'] + '.' +  (info['asset_name'] or '')
        assets_collection.insert_one(info)
    
    else:
        info = asset_info[0]
    
    return info

def build_whale_message(tx_hash, exchange_name, asset_name, percent_change):
    message = exchange_name + "\n"
    message += f"Whale splash for {asset_name}: {percent_change}%\n"
    message += f'transaction: https://cardanoscan.io/transaction/{tx_hash}\n'

    return message

def send_message(message):
    url = "http://telegram:7000/message"

    payload = json.dumps({
        "text": message
    })

    response = requests.request("POST", url, data=payload)
    assert response.status_code == 200