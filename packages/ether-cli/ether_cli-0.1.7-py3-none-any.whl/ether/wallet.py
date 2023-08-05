from ether import transaction, local, utils
from cryptography.fernet import Fernet
from mnemonic import Mnemonic
from hdwallet import HDWallet
from hdwallet.symbols import ETH
from getpass import getpass
import os

def seed_phrase():
    lang = Mnemonic("english")
    mnemonic = lang.generate(strength=256)
    return lang, mnemonic

def try_path(path):
    mnemonic = seed_phrase()[1]
    try:
        create_file_pair(path, mnemonic)
    except:
        print("Error has occured.")

def create_file_pair(path, mnemonic):
    key_file(path)
    mnemonic_file(path, mnemonic)
    try:
        with open(os.path.expanduser("~/.wallet/path.csv"), "w") as file:
            file.write(path.strip())
    except:
        os.mkdir(os.path.expanduser("~/.wallet"))
        with open(os.path.expanduser("~/.wallet/path.csv"), "w") as file:
            file.write(path.strip())
    print(f"\nSeed phrase and encryption key have been generated in the external drive\n\n{mnemonic}\n\nWrite backup mnemonic and store drive in secure location")

def key_file(path):
    Key = Fernet.generate_key()
    with open(f"{path}/encryption.key", "wb") as key:
        key.write(Key)

def mnemonic_file(path, mnemonic):
    with open(f"{path}/encryption.key", "rb") as key:
        Key = key.read()
    fernet = Fernet(Key)
    encrypted_mnemonic = fernet.encrypt(mnemonic.encode("utf-8"))
    with open(f"{path}/key.csv", "wb") as file:
        file.write(encrypted_mnemonic)

def decrypt_mnemonic(path):
    with open(f"{path}/encryption.key", "rb") as key:
        Key = key.read()
    fernet = Fernet(Key)
    with open(f"{path}/key.csv", "rb") as file:
        encrypted_mnemonic = file.read()
    decrypted_mnemonic = fernet.decrypt(encrypted_mnemonic)
    return decrypted_mnemonic

def derive_wallet(mnemonic, index, passphrase=None, private=False):
    wallet = HDWallet(ETH)
    lang = seed_phrase()[0]
    if passphrase != None:
        seed = lang.to_seed(mnemonic, passphrase=passphrase)
    else:
        seed = lang.to_seed(mnemonic)
    wallet.from_seed(seed=seed.hex())
    wallet.from_path(path=f"m/44'/60'/0'/0/{index}")
    if private == True:
        private_key = wallet.private_key()
        account_address = wallet.p2pkh_address()
        return private_key, account_address
    if private == False:
        account_address = wallet.p2pkh_address()
        return account_address

def derivation(path, index, passphrase=None, private=False, mnemonic=None, printer=False):
    if passphrase == "":
        passphrase = None
    if mnemonic != None:
        wallet = HDWallet(ETH)
        check_mnemonic = wallet.from_mnemonic(mnemonic=mnemonic)
        check_mnemonic.mnemonic()
        if private == True:
            key_pair = derive_wallet(mnemonic, index, passphrase, private)
            if printer == True:
                print(f"ACCOUNT: {key_pair[1]}")
                print(f"PRIVATE: {key_pair[0]}")
            return key_pair[0], key_pair[1]
        if private == False:
            account_address = derive_wallet(mnemonic, index, passphrase, private)
            if printer == True:
                print(f"ACCOUNT: {account_address}")
            return account_address
    else:
        if private == True:
            decrypted_mnemonic = decrypt_mnemonic(path.strip())
            key_pair = derive_wallet(decrypted_mnemonic, index, passphrase, private)
            if printer == True:
                print(f"ACCOUNT: {key_pair[1]}")
                print(f"PRIVATE: {key_pair[0]}")
            return key_pair[0], key_pair[1]
        if private == False:
            decrypted_mnemonic = decrypt_mnemonic(path.strip())
            account_address = derive_wallet(decrypted_mnemonic, index, passphrase, private)
            if printer == True:
                print(f"ACCOUNT: {account_address}")
            return account_address

def account(private=False):
    try:
        seed_phrase = None
        ext_file_path = local.wallet_path()
        derivation(ext_file_path, "0")
        mnemonic = False
    except:
        print("Use command `ether init location` to set wallet path.")
        seed_phrase = getpass("MNEMONIC: ")
        ext_file_path = None
        mnemonic = True
    passphrase = getpass("PASSPHRASE: ")
    account_number = input("INDEX: ")
    if account_number == "":
        account_number = "0"
    if mnemonic == True:
        if private == True:
            derivation(ext_file_path, account_number, passphrase=passphrase, private=True, mnemonic=seed_phrase, printer=True)
        if private == False:
            derivation(ext_file_path, account_number, passphrase=passphrase, mnemonic=seed_phrase, printer=True)
    if mnemonic == False:
        if private == True:
            derivation(ext_file_path, account_number, passphrase=passphrase, private=True, printer=True)
        if private == False:
            derivation(ext_file_path, account_number, passphrase=passphrase, printer=True)

def balance(testnet=False):
    try:
        status = True
        if testnet == False:
            account = local.account_file()
            try:
                provider_data = local.provider_file()
            except:
                status = False
                if testnet == False:
                    print("Use command `ether init provider` to set provider.")
                if testnet == True:
                    print("Use command `ether init provider --testnet` to set provider.")
        if testnet == True:
            account = local.account_file(testnet=True)
            try:
                provider_data = local.provider_file(testnet=True)
            except:
                status = False
                if testnet == False:
                    print("Use command `ether init provider` to set provider.")
                if testnet == True:
                    print("Use command `ether init provider --testnet` to set provider.")
        if status == True:
            provider_info = transaction.provider(provider_data)
            balance = transaction.get_balance(provider_info, account)
            print(f"{account}\n{balance} ETH")
            if testnet == False:
                try:
                    print(f"${utils.eth_price(balance):.2f}")
                except:
                    pass
    except:
        if testnet == False:
            print("Use command `ether init account` to set watch only account.")
        if testnet == True:
            print("Use command `ether init account --testnet` to set watch only account.")
