import pandas

from blockchain import Blockchain, WalletHolding, NftHolding
from collections import Counter
from dataclasses import dataclass, field
from transaction import Transaction
from typing import List, Dict

@dataclass
class ContractStats:
    """
    Maybe add wallet address in the future. Not needed rn.
    """

    contract_counter : Counter = field(default_factory=lambda:Counter())

    def add_nft_transfer(self, nft_transfer):
        contract_address = nft_transfer.contract_address
        self.contract_counter.update({contract_address: 1})

@dataclass
class WalletStats:

    address: str

    transaction_count: int

    wallet_holdings: [WalletHolding]

    is_active_wallet: bool

    is_active_nft_wallet: bool

    active_transaction: Transaction

    contract_stats : ContractStats

    nft_holdings: List[NftHolding] = field(default_factory=list)

    # transaction_history: [Transaction] = [] # Do we need to store this?
    def __post_init__(self):
        if not self.nft_holdings:
            self.nft_holdings = []

    def get_transaction_count(self):
        return len(self.transaction_history)

    def get_nft_count(self):
        return len(self.nft_holdings)


    # def get_stats():
    #     """ Returns stats as dictionary."""
