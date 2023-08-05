from ether import local, wallet
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from getpass import getpass

def provider(network):
    provider = Web3(HTTPProvider(network))
    provider.middleware_onion.inject(geth_poa_middleware, layer=0)
    return provider

def get_balance(provider=None, account_address=None):
    return provider.eth.get_balance(str(account_address)) / 1000000000000000000

def core_transaction(provider=None, to=None, amount=None, gas_price=None, data=None, key_pair=None, chain_id=1):
    if chain_id == 1:
        chain = 1
    elif chain_id == "ropsten":
        chain = 3
    elif chain_id == "kovan":
        chain = 42
    elif chain_id == "rinkeby":
        chain = 4
    else:
        chain = chain_id
    if data == None:
        txn_data = b""
    else:
        note = data.encode()
    signed_tx = provider.eth.account.signTransaction({
        "maxFeePerGas" : gas_price * 1000000000,
        "maxPriorityFeePerGas" : 2000000000,
        "to" : to,
        "from" : key_pair[1],
        "value" : int(amount * 1000000000000000000),
        "nonce" : provider.eth.get_transaction_count(key_pair[1]),
        "gas" : 21000,
        "data" : txn_data,
        "chainId" : chain,
        },
        key_pair[0]
    )
    tx_hash = provider.eth.send_raw_transaction(signed_tx.rawTransaction)
    print("Processing transaction...")
    tx_receipt = provider.eth.wait_for_transaction_receipt(tx_hash)
    print("Transaction completed.")
    return tx_receipt.transactionHash.hex()

def send_transaction(data=None, testnet=False):
    try:
        seed_phrase = None
        ext_file_path = local.wallet_path()
        wallet.derivation(ext_file_path, "0")
    except:
        print("Use command `ether init location` to set wallet path.")
        seed_phrase = getpass("MNEMONIC: ")
        ext_file_path = None
    passphrase = getpass("PASSPHRASE: ")
    account_number = input("INDEX: ")
    if account_number == "":
        account_number = "0"
    if passphrase != "":
        key_pair = wallet.derivation(ext_file_path, account_number, passphrase=passphrase, private=True, mnemonic=seed_phrase)
    else:
        key_pair = wallet.derivation(ext_file_path, account_number, private=True, mnemonic=seed_phrase)
    provider_info = local.provider_file(testnet=testnet)
    provider_data = provider(provider_info.strip())
    balance = get_balance(provider_data, key_pair[1])
    print(f"ACCOUNT: {key_pair[1]}\nBALANCE: {balance} ETH")
    menu = input("CONTINUE? Y/N ")
    if menu.lower() == "y":
        to = input("TO: ")
        amount = input("ETH AMOUNT: ")
        gas = input("GAS PRICE: ")
        if testnet == True:
            txn = core_transaction(provider=provider_data, to=to, amount=float(amount), gas_price=int(gas), data=data, key_pair=key_pair, chain_id=local.testnet_chain_id_file())
        if testnet == False:
            txn = core_transaction(provider=provider_data, to=to, amount=float(amount), gas_price=int(gas), data=data, key_pair=key_pair)
        print(txn)