import os

def account_file(account_address=None, testnet=False):
    if account_address == None:
        if testnet == False:
            with open(os.path.expanduser("~/.ether/mainnet_account.csv"), "r") as file:
                account = file.read()
            return account
        if testnet == True:
            with open(os.path.expanduser("~/.ether/testnet_account.csv"), "r") as file:
                test_account = file.read()
            return test_account
    if account_address != None:
        if testnet == False:
            try:
                with open(os.path.expanduser("~/.ether/mainnet_account.csv"), "w") as file:
                    file.write(account_address)
            except:
                os.mkdir(os.path.expanduser("~/.ether"))
                with open(os.path.expanduser("~/.ether/mainnet_account.csv"), "w") as file:
                    file.write(account_address)
        if testnet == True:
            try:
                with open(os.path.expanduser("~/.ether/testnet_account.csv"), "w") as file:
                    file.write(account_address)
            except:
                os.mkdir(os.path.expanduser("~/.ether"))
                with open(os.path.expanduser("~/.ether/testnet_account.csv"), "w") as file:
                    file.write(account_address)

def init_account(testnet=False):
    account_address = input("ACCOUNT: ")
    if testnet == False:
        account_file(account_address)
        print("Watch only account has been set.")
    if testnet == True:
        account_file(account_address)
        print("Watch only testnet account has been set.")

def provider_file(provider=None, chain_id=None, testnet=False):
    if provider == None:
        if testnet == False:
            with open(os.path.expanduser("~/.ether/mainnet_provider.csv"), "r") as file:
                mainnet = file.read()
            return mainnet
        if testnet == True:
            with open(os.path.expanduser("~/.ether/testnet_provider.csv"), "r") as file:
                test_network = file.read()
            return test_network
    if provider != None:
        if testnet == False:
            try:
                with open(os.path.expanduser("~/.ether/mainnet_provider.csv"), "w") as file:
                    file.write(provider)
            except:
                os.mkdir(os.path.expanduser("~/.ether"))
                with open(os.path.expanduser("~/.ether/mainnet_provider.csv"), "w") as file:
                    file.write(provider)
        if testnet == True:
            try:
                with open(os.path.expanduser("~/.ether/testnet_provider.csv"), "w") as file:
                    file.write(provider)
            except:
                os.mkdir(os.path.expanduser("~/.ether"))
                with open(os.path.expanduser("~/.ether/testnet_provider.csv"), "w") as file:
                    file.write(provider)
            with open(os.path.expanduser("~/.ether/testnet_chain"), "w") as file:
                file.write(chain_id)

def testnet_chain_id_file():
    with open(os.path.expanduser("~/.ether/testnet_chain_id.csv"), "r") as file:
        chain_id = file.read()
    return chain_id

def wallet_path(path=None):
    if path == None:
        with open(os.path.expanduser("~/.ether/path.csv"), "r") as file:
            location = file.read()
        return location
    if path != None:
        with open(os.path.expanduser("~/.ether/path.csv"), "w") as file:
            file.write(path)
