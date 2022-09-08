
def wei_to_eth(wei):
    return wei / (10**18)

def wei_to_usd(wei, eth_to_usd_price):
    eth_balance = wei_to_eth(wei)
    return eth_balance * eth_to_usd_price
