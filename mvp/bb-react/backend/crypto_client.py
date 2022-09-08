import cryptocompare
import currency_utils
import os
import json
import requests
import simplejson as json
import utils

from blockchain import Blockchain, WalletHolding
from flask import Flask, jsonify, render_template, request
from forms import DataTriggerForm
from flask_cors import CORS, cross_origin
from web3 import Web3

class CryptoClient:
    """
        Client for interfacing with blockchain APIs. This is the entry point
        for connecting to web3. This CryptoClient should be used when fetching
        chain data, instead of directly creating a web3 client. That way, the
        underlying api can be changed without breaking Blackbird.

        This client is not meant to process or aggregate data, only fetch.
    """

    ALCHEMY_KEY = "7aQpVM5vBiVrz_U2GHCMCltNuIlSGatn"#os.environ.get('KEY')
    CRYPTOCOMPARE_KEY = "a9342d4d312d5fc942eedc405b6c6aa8ba0855002029d5cac7c5a9f81973cb3b"

    ETH_TOKEN_ALLOW_LIST = {"ETH", "MATIC", "BAT", "DAI"}
    # erc20 for matic transfer
    # TODO(): check how to include internal transfers. This fails sometime
    TRANSFER_CATEGORIES = ["external", "erc20", "erc721", "erc1155"]

    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider('https://eth-mainnet.alchemyapi.io/v2/'+self.ALCHEMY_KEY))
        cryptocompare.cryptocompare._set_api_key_parameter(self.CRYPTOCOMPARE_KEY)

    # includes the standard ERC20 ABI info
    ERC20_ABI = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_from","type":"address"},{"indexed":true,"name":"_to","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_owner","type":"address"},{"indexed":true,"name":"_spender","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Approval","type":"event"}]')  # noqa: 501

    AKITA_ADDRESS = '0x3301Ee63Fb29F863f2333Bd4466acb46CD8323E6'

    def to_checksum_address(self, address):
        return self.w3.toChecksumAddress(address)

    def get_nfts_for_wallet(self, address):
        """ Returns a list of nfts for a given wallet address.

        See https://docs.alchemy.com/reference/getnfts
        # TODO(): Can set withMetadata to false if not needed.
        """
        # url = f"https://eth-mainnet.g.alchemy.com/nft/v2/{self.ALCHEMY_KEY}/getNFTs?owner={address}&withMetadata=true"

        url = f"https://eth-mainnet.alchemyapi.io/nft/v2/{self.ALCHEMY_KEY}/getNFTs?owner={address}&withMetadata=true"
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers)
        owned_nfts = response.json()["ownedNfts"]
        return [utils.create_blackbird_nft_holding(nft) for nft in owned_nfts]

    def get_balance_wei(self, address):
        """ Gets balance of address in wei."""
        return self.w3.eth.get_balance(address)

    def get_eth_holding(self, address):
        """ Gets wallet holding of an address. """
        address = self.to_checksum_address(address)
        wei_balance = self.w3.eth.get_balance(address)
        eth_balance = currency_utils.wei_to_eth(wei_balance)
        eth_to_usd_price = self.get_eth_to_usd_price()
        usd_balance = currency_utils.wei_to_usd(wei_balance, eth_to_usd_price)
        wallet_holding = WalletHolding(blockchain=Blockchain.ETH, coin_value=eth_balance, usd_value=usd_balance)
        return wallet_holding

    def get_eth_transaction_count(self, address):
        return self.w3.eth.get_transaction_count(address)

    def get_eth_to_usd_price(self):
        return cryptocompare.get_price('ETH', currency='USD').get('ETH').get('USD')

    def get_token_balances(self, address, contract_addresses):
        """
        See https://docs.alchemy.com/reference/alchemy-gettokenbalances
        """
        pass

    def get_transaction_receipt(self, transaction_hash):
        """ Gets transaction receipt for a given transaction hash.

        Primarily to determine gas usage for transaction."""
        # Query the blockchain (replace example parameters)
        receipt = self.w3.eth.get_transaction_receipt(transaction_hash)
        return receipt

    def get_transaction_history(self, address, with_gas_receipts=False, transaction_limit=24):
        """
        Gets all inbound and outbound transactions for an address.

        Pagination not implemented. One call will get at most 2K transactions.
        TODO(): Either separate calls by token category or paginate.

        This method is expensive: O(n) API calls where n is the number of
        transactions associated with a wallet. We need to find ways to optimize.

        transaction_limit: is the maximum number of transactions to fetch
        receipts for. Default is 24 arbitrarily rip kob.
        """
        transactions = []
        all_transfers = self._get_all_transfers(address) # 2 api calls

        for index,transfer in enumerate(all_transfers):
            if index >= transaction_limit:
                # to cut down on transactions processed for rate-limiting
                # break
                if index == len(all_transfers) - 1:
                    print("transfer count:", len(all_transfers))

            asset_type = transfer["asset"]
            category = transfer["category"]
            # if asset_type in self.ETH_TOKEN_ALLOW_LIST or category in self.TRANSFER_CATEGORIES:
            if category in self.TRANSFER_CATEGORIES:
                if with_gas_receipts:
                    transaction_hash = transfer["hash"]
                    receipt = self.get_transaction_receipt(transaction_hash) # api call * transaction
                else:
                    receipt = None
                bb_transaction = utils.create_blackbird_transaction(transfer, receipt)
                transactions.append(bb_transaction)

        return transactions

    def _get_all_transfers(self, address):
        """ Returns list of dictionaries representing transfers from an account.

        Makes two separate calls to alchemy API to get transactions from and
        to an account. Can probably be cleaned up more.
        """
        transactions_from_params = self.create_asset_transfer_params(from_address=address)
        transactions_from_data = self._get_asset_transfer_json()
        transactions_from_data["params"] = [transactions_from_params]
        transfers_from = self._get_transfers(transactions_from_data)

        transactions_to_params = self.create_asset_transfer_params(to_address=address)
        transactions_to_data = self._get_asset_transfer_json()
        transactions_to_data["params"] = [transactions_to_params]
        transfers_to = self._get_transfers(transactions_to_data)

        return transfers_from + transfers_to

    def _get_transfers(self, data):
        """ TODO: Implement pagination """
        response = requests.post(\
            'https://eth-mainnet.alchemyapi.io/v2/'+self.ALCHEMY_KEY, \
            json=data)
        json_response = response.json()
        if 'error' in json_response:
            error_code = json_response['error']['code']
            error_message = json_response['error']['message']

            print(f"Error code [{error_code}] in request with message: [{error_message}] from address [{from_address}] to address [{to_address}]")
            return []
        return json_response["result"]["transfers"]

    def get_transactions(self, from_address="0x0", to_address="0x0", categories=TRANSFER_CATEGORIES):
        """ Gets transfers between the given addresses.

        Currently no way to get a transaction object for a transaction hash so
        we must provide addresses.
        """
        data = self.create_transfers_payload(from_address=from_address, to_address=to_address, categories=categories)
        response = requests.post(\
            'https://eth-mainnet.alchemyapi.io/v2/'+self.ALCHEMY_KEY, \
            json=data)
        json_response = response.json()
        if 'error' in json_response:
            error_code = json_response['error']['code']
            error_message = json_response['error']['message']
            to_address = data["params"]["toAddress"]
            from_address = data["params"]["fromAddress"]
            print(f"Error code [{error_code}] in request with message: [{error_message}] from address [{from_address}] to address [{to_address}]")
            return []
        transfers = json_response["result"]["transfers"]
        # print("transfers:" transfers)
        return [utils.create_blackbird_transaction(transfer=transfer, receipt=None) for transfer in transfers]

    def create_transfers_payload(self, from_address="0x0", to_address="0x0", categories=TRANSFER_CATEGORIES):
        """ TODO(): Consider making object for address params. """
        asset_transfer_json = self._get_asset_transfer_json()
        transactions_params = []
        if from_address != "0x0" and to_address != "0x0":
            transactions_params = self.create_asset_transfer_params(from_address=from_address, to_address=to_address, categories=categories)
        elif from_address == "0x0":
            transactions_params = self.create_asset_transfer_params(to_address=to_address, categories=categories)
        else:
            transactions_params = self.create_asset_transfer_params(from_address=from_address, categories=categories)
        # TODO(): add exception for failure case

        asset_transfer_json["params"] = [transactions_params]
        return asset_transfer_json

    def _get_asset_transfer_json(self):
        return {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "alchemy_getAssetTransfers"}

    # TODO(): Add internal transactions
    def create_asset_transfer_params(self, from_block="0x0", to_block="latest", from_address="0x0", to_address="0x0", categories=TRANSFER_CATEGORIES):
        """ Sets params for alchemy asset transfer api. By default searches
        transactions from genesis.

        See https://docs.alchemy.com/alchemy/enhanced-apis/transfers-api
        """
        params = {}
        if from_block != "0x0":
            params["fromBlock"] = from_block
        if to_block != "latest":
            params["toBlock"] = to_block
        if from_address != "0x0":
            params["fromAddress"] = from_address
        if to_address != "0x0":
            params["toAddress"] = to_address

        if categories:
            params["category"] = categories
        params["withMetadata"] = True
        return params
