import datetime
from transaction import Transaction, NftTransfer
from blockchain import Blockchain, NftHolding, TokenType

TOKEN_TYPES = {'erc721', 'erc1155'}

def create_blackbird_transaction(transfer, receipt=None):
    """ Converts alchemy transfer to blackbird transaction.

    See https://docs.alchemy.com/alchemy/enhanced-apis/transfers-api#returns
    """
    # Data from transfer
    block_num = transfer["blockNum"]
    transaction_hash = transfer["hash"]
    from_address = transfer["from"]
    to_address = transfer["to"]
    value = transfer["value"]
    # '2022-01-26T23:01:27.000Z'
    block_timestamp = datetime.datetime.strptime(transfer["metadata"]["blockTimestamp"],"%Y-%m-%dT%H:%M:%S.%fZ")
    asset = transfer["asset"]
    blockchain = Blockchain.ETH # Defaults to ETH. Change in future
    if asset in [e.value for e in Blockchain]:
        blockchain = Blockchain[asset]

    # NFT Data
    # See https://docs.alchemy.com/docs/how-to-get-all-nft-transactions-by-an-address
    erc_721_token = None
    erc_1151_tokens = []
    # print("transfer category:", transfer["category"])
    if transfer["category"] in TOKEN_TYPES:
        contract_address = transfer["rawContract"]["address"]
        token_type = TokenType[transfer["category"].upper()]
        if "erc1155Metadata" in transfer and transfer["erc1155Metadata"]:
            for erc1155 in transfer["erc1155Metadata"]:
                # ERC1155 allows for batch transfers.
                # See https://101blockchains.com/erc-1155-vs-erc-721/
                token_id = erc1155["tokenId"]
                nft_transfer = NftTransfer(contract_address, token_id, token_type)
                erc_1151_tokens.append(nft_transfer)
        else:
            token_id = transfer["tokenId"]
            erc_721_token = NftTransfer(contract_address, token_id, token_type)

    # Data from receipt
    transaction_index = None
    block_hash = None
    gas_used = None
    effective_gas_price = None
    eth_gas_price = None
    total_gas_cost = None
    if receipt:
        block_hash = receipt["blockHash"].hex()
        gas_used = receipt["gasUsed"]
        transaction_index = receipt["transactionIndex"]
        # Set gas price
        if "effectiveGasPrice" in receipt:
            effective_gas_price = receipt["effectiveGasPrice"]
            eth_gas_price = int(effective_gas_price, 16) / 1e9
            total_gas_cost = eth_gas_price * (gas_used / 1e9)


    # cumulative_gas_used = receipt["cumulativeGasUsed"] # not used rn

    transaction = Transaction(\
        transaction_hash=transaction_hash,\
        block_num=block_num,\
        block_hash=block_hash,\
        from_address=from_address,\
        to_address=to_address,\
        value=value,\
        block_timestamp=block_timestamp,\
        effective_gas_price=effective_gas_price,\
        gas_used=gas_used,\
        total_gas_cost=total_gas_cost,
        transaction_index=transaction_index,\
        blockchain=blockchain,\
        erc_721_token = erc_721_token,\
        erc_1151_tokens = erc_1151_tokens
        )

    return transaction

def create_blackbird_nft_holding(owned_nft_json, blockchain=Blockchain.ETH):
    contract_address = owned_nft_json["contract"]["address"]
    token_id = owned_nft_json["id"]["tokenId"]
    token_type = TokenType.UNKNOWN
    token_type_from_json = owned_nft_json["id"]["tokenMetadata"]["tokenType"]
    if token_type_from_json in [type.value for type in TokenType]:
        token_type = TokenType[owned_nft_json["id"]["tokenMetadata"]["tokenType"]]

    balance = owned_nft_json["balance"]

    blackbird_nft = NftHolding(contract_address, token_id, token_type, balance)
    return blackbird_nft

def hex_multiply(x, y):
    return hex(int(x, 16) * int(y, 16))
