import datetime
import json
import pandas
import time

from aggregator import Sr71Radar
from blockchain import Blockchain, WalletHolding
from collections import Counter
from crypto_client import CryptoClient
from dataclasses import dataclass, field

@dataclass
class StakePosition:
    """ Not used rn """
    address: str
    timestamp: datetime
    amount: float

    def to_tuple(self):
        return (address, timestamp, amount)


class Sherlock:
    """

    TODO: Split into service and batch job
    What's the difference/tradeoffs between this CSV and hitting alchemy.


    Findings/Patterns/Thoughts:
    * Need an efficient data structure to store resulting stats.
        * This data structure could be flexible such that user defines metric
        names, metric unit, frequency of data, etc. Essentially metric metadata config

    * Need an internal data structure for standardized processing
        * Need to easily filter, search data from it

    * Approach: Create a cron job for raw root level data that requires an API
    fetch. E.g. aggregate all wallets across customers and run cron job to get
    wallet holdings once a day. With ability to run cron job for subset of
    wallets that updates wallet-holding db. The processing jobs can pull from
    that data faster than reading blockchain each time. (Show delay indicator
    in UI or chart or whatever - ya pull up)

    * Concurrency for requests: https://realpython.com/python-concurrency/
    """

    SHERLOCK_CONTRACT_ADDRESS = "0x0865a889183039689034dA55c1Fd12aF5083eabF"

    # Processing staking positions + wallet holdign = Elapsed Time:  124.98979711532593
    SHERLOCK_CONTRACT_ADDRESS_FIRST = "0xf8583f22C2f6f8cd27f62879A0fB4319bce262a6"

    STAKERS_FIRST_ROUND_CSV = 'sherlock_stakers_first_round.csv'
    STAKERS_SECOND_ROUND_CSV = 'sherlock_stakers_second_round.csv'

    def __init__(self):
        self.crypto_client = CryptoClient()
        self.transactions_df = self._get_all_valid_stakers()
        # update this to come from output csv
        self.staker_addresses = self.transactions_df.From.unique()
        self.sherlock_stats_df = pandas.DataFrame()

    def investigate(self):
        """

            # Staking positions = 83 first round + 274 second round
        """
        # self.get_stakers_time_series()
        # self._process_staker_wallets()
        # self.get_staking_pool_time_series()
        # self.get_staker_wallet_stats()
        # t0 = time.time()
        # self.accumulate_stats()
        self._process_staker_wallets()
        # self._get_all_valid_stakers()
        # t1 = time.time()
        # elapsed = t1 - t0
        # print("ELAPSED TIME: ", elapsed)

    def get_stakers_time_series(self):
        """ Staking amounts each day (not a running sum). """
        stakers_df = pandas.read_csv('sherlock_staking_positions.csv')
        stakers_df['timestamp'] = pandas.to_datetime(stakers_df['timestamp']).dt.strftime('%Y-%m-%d')
        output_dict = stakers_df.groupby('timestamp').amountStaked.sum().to_dict()
        # print("OUTPUT DICT:", output_dict)
        # print("SUM:", sum(output_dict.values()))
        return json.dumps(output_dict)

    def get_staking_pool_time_series(self):
        """ Running sum over staking pool. """
        stakers_df = pandas.read_csv('sherlock_staking_positions.csv')
        stakers_df['timestamp'] = pandas.to_datetime(stakers_df['timestamp']).dt.strftime('%Y-%m-%d')
        grouped_df = stakers_df.groupby('timestamp').amountStaked.sum()
        # print("GROUPED_DF:", grouped_df)
        df = grouped_df.cumsum()
        # print("df:", df)
        output_dict = df.to_dict()
        # print("OUTPUT DICT:", output_dict)
        return json.dumps(output_dict)

    def _process_staker_wallets(self):
        """ Caution! On avg takes 290 seconds. """
        sr71 = Sr71Radar()
        t0 = time.time()
        sr71.scan(self.staker_addresses, output_csv_file_path="sherlock_stats.csv")
        t1 = time.time()
        elapsed = t1 - t0
        print("elapsed:", elapsed)

    def get_staker_wallet_stats(self):
        stats = {
            'totalWallets': 337,
            'activeWalletCount': 264,
            'meanEthBalance': 4.07096450293483,
            'meanUsdBalance': 7514.440439197163,
            'mean_nft_count': 36.62611275964392,
            'median_nft_count': 24.0,
            'topThreeNftContracts':
                {'0x0e3a2a1f2146d86a604adc220b4967a898d7fe07': 652,
                 '0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85': 597,
                 '0x629cdec6acc980ebeebea9e5003bcd44db9fc5ce': 596},
            'isActiveWalletPercent': 0.7833827893175074,
            'isActiveNftWalletPercent': 0.5519287833827893,
            'walletsWithNftPercent': 1.0
        }
        return json.dumps(stats)


    ###################################################
    ####### Code below is for batch processing ########
    ###################################################

    def _get_all_valid_stakers(self):
        stakers_first_round = self._get_valid_staker_data_frame(self.STAKERS_FIRST_ROUND_CSV)
        stakers_second_round = self._get_valid_staker_data_frame(self.STAKERS_SECOND_ROUND_CSV)
        all_stakers = stakers_first_round.append(stakers_second_round, ignore_index=True)
        return all_stakers

    def _get_valid_staker_data_frame(self, csv_file_path):
        transactions_data_frame = pandas.read_csv(csv_file_path)
        if "first_round" in csv_file_path:
            query = "Method == 'Execute' and ErrCode != 'Error(0)'"
        else:
            query = "Method == 'Initial Stake' and ErrCode != 'Error(0)'"
        valid_transactions_df = transactions_data_frame.query(query)
        return valid_transactions_df

    def accumulate_stats(self):
        address_to_position = self.get_sherlock_staking_positions()
        stats = pandas.DataFrame(address_to_position["addressAllPositions"], columns=["address", "timestamp", "amountStaked"])
        stats.to_csv("sherlock_staking_positions.csv", mode='a', header=False)

        balances = self.accumulate_staker_balances(address_to_position["addressTotalStaked"])
        staker_total_stats = pandas.DataFrame(balances, columns=["address", "ethBalance", "ethUsdBalance", "totalSherlockStake"])
        staker_total_stats.to_csv("sherlock_staker_balances.csv", mode='a', header=False)

    def get_sherlock_staking_positions(self):
        """ Get staking positions knowing Sherlock's smart contract address.

        Need a way to determine if a transaction is staking.
        Etherscan doesn't contain staking value so need to hit alchemy.
        """
        address_to_total_staked = Counter()
        address_to_all_positions = []
        address_to_position = {}
        for address in self.staker_addresses:
            transactions = self.crypto_client.get_transactions(\
                from_address=address,\
                to_address=self.SHERLOCK_CONTRACT_ADDRESS_FIRST)
            for transaction in transactions:
                if transaction.value:
                    address_to_total_staked.update({address: transaction.value})
                    address_to_all_positions.append((address,
                        transaction.block_timestamp.strftime("%Y-%m-%dT%H:%M:%S"),
                        transaction.value))

        #TODO(): remove 'address' from key.
        address_to_position["addressTotalStaked"] = address_to_total_staked
        address_to_position["addressAllPositions"] = address_to_all_positions
        return address_to_position

    def accumulate_staker_balances(self, address_to_total_staked):
        wallet_balances = self.get_staker_wallet_balances()
        all_wallet_balances = []
        for address in wallet_balances:
            wallet_holding = wallet_balances[address]
            total_sherlock_stake = "N/A"
            if address in address_to_total_staked:
                total_sherlock_stake = address_to_total_staked[address]
            else:
                print(f"Could not find sherlock stake for address: {address}")

            wallet_value = (address, wallet_holding.coin_value, wallet_holding.usd_value, total_sherlock_stake)
            all_wallet_balances.append(wallet_value)

        return all_wallet_balances


    def get_staker_wallet_balances(self):
        address_to_wallet_balance = {}
        for address in self.staker_addresses:
            if address not in address_to_wallet_balance:
                eth_holding = self.crypto_client.get_eth_holding(address)
                address_to_wallet_balance[address] = eth_holding
            else:
                print(f"Found duplicate address: [{address}]")
        return address_to_wallet_balance


    def get_sherlock_transactions(self):
        pass

def main():
    sherlock = Sherlock()
    sherlock.investigate()


if __name__ == "__main__":
    print("staaahting investigation misses hudson")
    main()
