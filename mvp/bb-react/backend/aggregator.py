import pandas

from collections import Counter
from wallet_processor import WalletProcessor
from wallet_stats import WalletStats

class Sr71Radar:
    """
        Top level class to process a set of wallets and aggregate metrics
        for them.

        TODO: Differentiate NFTs that are sent as scams or actually bought
    """

    def __init__(self):
        self._wallet_processor = WalletProcessor()

    def scan(self, wallet_addresses, output_csv_file_path=""):
        targets = self._process_wallets(wallet_addresses)
        return self._aggregate(targets, output_csv_file_path)

    def _process_wallets(self, wallet_addresses):
        wallet_stats_list = []
        for address in wallet_addresses:
            wallet_stats = self._wallet_processor.process(address)
            wallet_stats_list.append(wallet_stats)

        return wallet_stats_list

    def _aggregate(self, wallet_stats_list, output_csv_file_path=""):
        """ Aggregates wallet data to produce metrics.

        Existing Metrics:
        - Average eth balance
        - Average usd balance
        - Average # NFTs / wallet
        - Top 3 NFT contracts interacted with
        - % Active Wallets:= Wallet with a transaction in <= 1 month
        - % NFT Active Wallets:= NFT transaction in <1= month
        - % of wallets with at least 1 NFT

        """
        data_frame = pandas.DataFrame(columns=["eth_balance", "usd_balance", "is_active_wallet", "nft_count"])
        contract_counter = Counter()
        for wallet_stats in wallet_stats_list:
            contract_counter.update(wallet_stats.contract_stats.contract_counter)
            # Refactor this to create data frame at very end.
            # See https://stackoverflow.com/questions/13784192/creating-an-empty-pandas-dataframe-then-filling-it
            # Zero index because we only look at eth holdings for now.
            eth_balance = wallet_stats.wallet_holdings[0].coin_value
            usd_balance = wallet_stats.wallet_holdings[0].usd_value
            is_active_wallet = wallet_stats.is_active_wallet
            is_active_nft_wallet = wallet_stats.is_active_nft_wallet
            wallet_address = wallet_stats.address
            transaction_count = wallet_stats.transaction_count
            # NFT data
            nft_count = wallet_stats.get_nft_count()
            data_frame = data_frame.append(\
                {"wallet_address":wallet_address,\
                 "eth_balance":eth_balance,\
                 "usd_balance":usd_balance,\
                 "is_active_wallet":is_active_wallet,\
                 "is_active_nft_wallet":is_active_nft_wallet,\
                 "nft_count":nft_count,\
                 "transaction_count":transaction_count
                },
                ignore_index=True)

        if output_csv_file_path:
            #### Not working for some reason. Needs debugging
            data_frame.to_csv(output_csv_file_path)
        else:
            print("Not writing to CSV")

        mean_eth_balance = data_frame.eth_balance.mean()
        mean_usd_balance = data_frame.usd_balance.mean()
        mean_nft_count = data_frame.nft_count.mean()
        median_nft_count = data_frame.nft_count.median()
        top_three_nft_contracts = dict(contract_counter.most_common(3))
        # use value_counts later when prubby not watching
        is_active_wallet_percent = data_frame.is_active_wallet.sum()/data_frame.shape[0]
        is_active_nft_wallet_percent = data_frame.is_active_nft_wallet.sum()/data_frame.shape[0]
        wallets_with_nft_percent = data_frame[data_frame.nft_count >= 1].shape[0]/data_frame.shape[0]

        result = {
            "totalWallets": len(wallet_stats_list),
            "activeWalletCount": data_frame.is_active_wallet.sum(),
            "meanEthBalance": mean_eth_balance,
            "meanUsdBalance": mean_usd_balance,
            "mean_nft_count": mean_nft_count, # Todo update name to camelCase
            "median_nft_count": median_nft_count,
            "topThreeNftContracts": top_three_nft_contracts,
            "isActiveWalletPercent": is_active_wallet_percent,
            "isActiveNftWalletPercent": is_active_nft_wallet_percent,
            "walletsWithNftPercent": wallets_with_nft_percent
        }
        print("result: ", result)
        return result
