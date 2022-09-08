
class TransactionService:
    """ !Not Used! Creates, maintains, and processes Blackbird Transactions. """

    def __init__(self, transfer, receipt):
        self._transfer = transfer
        self._receipt = receipt

    def get_block_num(self):
        block_num = transfer["blockNum"]


    # transaction_hash = transfer["hash"]
    # from_address = transfer["from"]
    # to_address = transfer["to"]
    # value = transfer["value"]
    # block_timestamp = transfer["metadata"]["blockTimestamp"]
    #
    # asset = transfer["asset"]
    # blockchain = Blockchain[asset]
    #
    # # Data from receipt
    # block_hash = receipt["blockHash"].hex()
    # gas_used = receipt["gasUsed"]
    # effective_gas_price = receipt["effectiveGasPrice"]
    # cumulative_gas_used = receipt["cumulativeGasUsed"] # not used rn
    # transaction_index = receipt["transactionIndex"]
    # total_gas_cost = int(effective_gas_price, 16) * gas_used
