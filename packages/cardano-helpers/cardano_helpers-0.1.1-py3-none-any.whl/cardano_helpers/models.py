from dataclasses import dataclass
from typing import List

@dataclass
class Order:
    price: int
    assetId: str
    amount: int
    type: str

@dataclass
class Metadata:
	name: str
	description: str
	ticker: str
	url: str
	logo: str
	decimals: int

@dataclass
class AssetInfo:
	asset: str
	policy_id: str
	asset_name: str
	fingerprint: str
	quantity: int
	initial_mint_tx_hash: str
	mint_or_burn_count: int
	metadata: Metadata
	asset_id: str

@dataclass
class Pool:
    price:          int
    assetId:        str
    queue:          int
    quantity_ada:   int
    quantity_asset: int
    decimalA:       int
    decimalB:       int

@dataclass
class Asset:
    policy: str
    asset: str
    amount: int

@dataclass
class Input:
    tx_id: str
    index: int

@dataclass
class UTXO:
    address: str
    amount: int
    assets: List[Asset]

@dataclass
class Transaction:
    hash: str
    fee: int
    ttl: int
    validity_interval_start: int
    network_id: str
    input_count: int
    output_count: int
    mint_count: int
    total_output: int
    metadata: List
    inputs: List[Input]
    outputs: List[UTXO]
    mint: List
    timestamp: int