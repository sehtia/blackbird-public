import currency_utils
import json
import pandas

from blockchain import Blockchain, WalletHolding
from crypto_client import CryptoClient
from dataclasses import asdict, dataclass
from wallet_stats import WalletStats, ContractStats

class WalletProcessor:
    """ Processes wallet data for a given wallet.

    Need intermediate data structure for aggregating data across all wallets.

    Future awesome metric behavior that P doesn't understand:
    - Look at when transactions occur to determine behavior. "Safe wallet holder
    vs P wallet holder". We talmbout the interweb.
    """

    def __init__(self):
        self.crypto_client = CryptoClient()


    def process(self, address):
        """ Processes transactions for a given wallet adddress.

        Results to process for are defined here: {Add internal link}.
        Results can further be cached for higher performance.
        """
        address = self.crypto_client.to_checksum_address(address)
        wei_balance = self.crypto_client.get_balance_wei(address)
        eth_balance = currency_utils.wei_to_eth(wei_balance)
        eth_to_usd_price = self.crypto_client.get_eth_to_usd_price()
        usd_balance = currency_utils.wei_to_usd(wei_balance, eth_to_usd_price)
        # TODO(): Need a walletholding for each currency.
        wallet_holding = WalletHolding(Blockchain.ETH, coin_value=eth_balance, usd_value=usd_balance)

        is_active_wallet = False
        is_active_nft_wallet = False
        active_transaction = None
        contract_stats = ContractStats()

        all_transactions  = self.crypto_client.get_transaction_history(address)
        for transaction in all_transactions:
            # Get active transactions
            if transaction.is_within_last_30_days():
                is_active_wallet = True
                active_transaction = transaction
                if transaction.has_nft_transfer():
                    is_active_nft_wallet = True

            if transaction.has_nft_transfer():
                # TODO(): Add other types of smart contracts
                # TODO(): Add type of nft token
                nft_transfers = transaction.get_nft_transfers()
                for nft_transfer in nft_transfers:
                    contract_stats.add_nft_transfer(nft_transfer)
            # Continue further processing of transactions here

        # Essentially a record for each wallet
        nft_holdings = self.crypto_client.get_nfts_for_wallet(address)
        wallet_stats = WalletStats(
            address,
            len(all_transactions),
            [wallet_holding],
            is_active_wallet,
            is_active_nft_wallet,
            active_transaction,
            contract_stats,
            nft_holdings)

        return wallet_stats

    def get_transaction_history(self, address):
        """ Not used as of 2022-08-06. """
        transaction_history = self.crypto_client.get_transaction_history(address)
        # wallet_history = WalletHistory(transaction_history)
        print("transaction_history SIZE: ", len(transaction_history))
        transaction_list_map = [asdict(transaction) for transaction in transaction_history]
        return json.dumps(transaction_list_map)#, cls=BytesEncoder)
        # return asdict(transaction_history)
