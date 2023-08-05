from requests import get

def eth_price(multiplier):
    ethereum = get("https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD").json()
    usd_eth = ethereum["USD"]
    multiplied_eth = usd_eth * float(multiplier)
    return multiplied_eth

def eth_estimate(total, unit=1):
    gwei_gas = int(total) * int(unit)
    eth_gas = gwei_gas * 0.000000001
    cost = eth_price(1) * eth_gas
    return cost

def unit_convert(type=None, amount=None):
    if type == "eth":
        eth = 1 * float(amount)
        gwei = 1000000000 * float(amount)
        wei = 1000000000000000000 * float(amount)
        return eth, gwei, wei
    elif type == "gwei":
        eth = 0.000000001 * float(amount)
        gwei = 1 * float(amount)
        wei = 1000000000 * float(amount)
        return eth, gwei, wei
    elif type == "wei":
        eth = 0.000000000000000001 * float(amount)
        gwei = 0.000000001 * float(amount)
        wei = 1 * float(amount)
        return eth, gwei, wei
