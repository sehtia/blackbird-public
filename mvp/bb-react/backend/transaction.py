import datetime

from blockchain import Blockchain, TokenType
from dataclasses import dataclass, field
from typing import List

@dataclass
class NftTransfer:
    """ Data fields pertaining to a NFT transfer. """
    contract_address: str = ""
    token_id: str = ""
    token_type: TokenType = None

@dataclass
class Transaction:
    """ Transaction container class for all transaction types. """
    transaction_hash: str
    block_hash: str
    block_num : str
    from_address: str
    to_address: str

    block_timestamp: datetime

    blockchain: Blockchain

    # Value is null if transaction is NFT transfer
    value : float = None
    transaction_index: int = None
    # Gassy fields
    effective_gas_price: str = ""
    gas_used: str = ""
    total_gas_cost: str = ""
    # NFT fields
    erc_721_token: NftTransfer = None
    erc_1151_tokens: List[NftTransfer] = field(default_factory=list)

    def __post_init__(self):
        if not self.erc_1151_tokens:
            self.erc_1151_tokens = []

    def is_within_last_30_days(self):
        today_datetime = datetime.datetime.utcnow()
        # block_timestamp = datetime.datetime.date(self.block_timestamp)
        duration_since_transaction = today_datetime - self.block_timestamp
        # print(f'DURATION SINCE TRANSACTY PANTS: {duration_since_transaction.days}')
        return duration_since_transaction.days <= 30

    def is_gas_cost_set(self):
        if total_gas_cost == "" or effective_gas_price is None:
            return False
        return True

    def has_nft_transfer(self):
        if self.erc_721_token or self.erc_1151_tokens:
            return True
        return False

    def get_nft_transfers(self):
        if self.erc_721_token:
            return [self.erc_721_token]
        if self.erc_1151_tokens:
            return self.erc_1151_tokens
        return []
