from dataclasses import dataclass
from enum import Enum


class Blockchain(str, Enum):
    ETH = "Ethereum"
    BTC = "Bitcoin"
    MATIC = "Polygon"
    BAT = "Basic Attention Token"
    DAI = "Dai"
    ILL = "Illuminati Finance"

    _LAYER_ONE = {ETH, BTC}

    def is_layer_one(self):
        return self.value in LAYER_ONE

class TokenType(str, Enum):
    ERC721 = "erc721"
    ERC1155 = "erc1155"
    UNKNOWN = "unknown"


@dataclass
class WalletHolding:
    blockchain: Blockchain
    coin_value: float
    usd_value: float

@dataclass
class NftHolding:
    """ Values currently fromm https://docs.alchemy.com/reference/getnfts """
    blockchain: Blockchain
    contract_address: str
    token_id: str

    balance: int = 1
    token_type: TokenType = None
    title: str = ""
    description: str = ""
