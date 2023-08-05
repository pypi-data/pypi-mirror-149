from typing import Callable, List
from .models import Pool


LOVELACE = 1000000

def get_unique_pools(pools) -> List[Pool]:
    unique_pools = {}
    for pool in pools:
        if pool['assetId'] not in unique_pools:
            unique_pools[pool['assetId']] = pool
        elif (
            pool['assetId'] in unique_pools and 
            (
                unique_pools[pool['assetId']]['volume'] < pool['volume'] or
                (
                    unique_pools[pool['assetId']]['volume'] == pool['volume'] and
                    unique_pools[pool['assetId']]['fee'] > pool['fee']
                )
            )
            
        ):
            unique_pools[pool['assetId']] = pool
    return list(unique_pools.values())

def calculate_impact(asset_quantity, asset_decimals, pool):
    asset_quantity  = float(asset_quantity)
    
    if asset_decimals and asset_decimals != 0:
        asset_quantity = asset_quantity / 10 ** asset_decimals

    quantity_ada    = float(pool['quantity_ada'])
    quantity_asset  = float(pool['quantity_asset'])
    current_price   = quantity_ada / quantity_asset
    new_stored_ada  = quantity_ada * quantity_asset / (quantity_asset + asset_quantity)
    new_price       = new_stored_ada / (quantity_asset + asset_quantity)
    slippage        = new_price / current_price
    percent_change  = (1 - slippage) * 100
    return percent_change

def calculate_lovelace_price(quantityA, quantityB):
    price_ada =  int(quantityA[0]) / int(quantityB[0])
    
    if quantityA[1] != quantityB[1]:
        price_ada = price_ada / 10**quantityA[1] - quantityB[1]
    
    price_lovelace = int(price_ada * LOVELACE)
    
    return price_lovelace

def generate_pools_info(
    pools, 
    get_asset_id:           Callable, 
    get_token_name:         Callable, 
    get_ticker:             Callable,
    get_fee:                Callable,
    get_pool_id:            Callable,
    get_pool_ada_quantity:  Callable,
    get_quantity_asset:     Callable,
    get_decimals_asset:     Callable,
    get_volume:             Callable,
    get_queue:              Callable,
    ) -> list:

    assets = []
    for pool in pools:
        row = {}
        row["assetId"]          = get_asset_id(pool)
        row["tokenName"]        = get_token_name(pool)
        row["ticker"]           = get_ticker(pool)
        row['fee']              = get_fee(pool)
        
        row["ident"]            = get_pool_id(pool)
        row['quantity_ada']     = get_pool_ada_quantity(pool)
        row['quantity_asset']   = get_quantity_asset(pool)
        row['decimal_asset']    = get_decimals_asset(pool)
        row['decimal_ada']      =  6
        
        qA = (row['quantity_asset'], row['decimal_asset'])
        qB = (row['quantity_ada'], row['decimal_ada'])

        row["price"] = calculate_lovelace_price(qA, qB)
        
        row['volume'] = get_volume(pool)
        row['queue'] = get_queue(pool)
        assets.append(row)
    return assets