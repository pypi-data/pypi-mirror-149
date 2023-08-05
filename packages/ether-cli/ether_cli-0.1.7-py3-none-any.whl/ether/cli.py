from ether import wallet, transaction, local, utils
from sys import argv
from getpass import getpass

msg_menu = """▄▄▄ .▄▄▄▄▄ ▄ .▄▄▄▄ .▄▄▄  
▀▄.▀·•██  ██▪▐█▀▄.▀·▀▄ █·
▐▀▀▪▄ ▐█.▪██▀▐█▐▀▀▪▄▐▀▀▄ 
▐█▄▄▌ ▐█▌·██▌▐▀▐█▄▄▌▐█•█▌
 ▀▀▀  ▀▀▀ ▀▀▀ · ▀▀▀ .▀  ▀
v0.1.7"""

msg_commands = """ether account
ether account --testnet
ether convert eth <amount>
ether convert gwei <amount>
ether convert wei <amount>
ether keys
ether price
ether price <amount>
ether gas <total>
ether gas <total> <price>
ether init
ether init account
ether init account --testnet
ether init location
ether init provider
ether init provider --testnet
ether mnemonic
ether send
ether send --testnet"""

def main():
    args = argv[1:]
    if len(args) == 0:
        print(msg_menu)
    try:
        if len(args) == 1:
            arg2 = argv[1]
            if arg2 == "init":
                ext_file_path = input("DRAG AND DROP EXTERNAL DRIVE: ")
                wallet.try_path(path=ext_file_path.strip())
            if arg2 == "account":
                wallet.balance()
            if arg2 == "keys":
                wallet.account(private=True)
            if arg2 == "mnemonic":
                print(f"\n{wallet.seed_phrase()[1]}\n")
            if arg2 == "price":
                ether = utils.eth_price(1)
                print(f"${ether:.2f}")
            if arg2 == "commands":
                print(msg_commands)
            if arg2 == "send":
                transaction.send_transaction()
        elif len(args) == 2:
            arg2 = argv[1]
            arg3 = argv[2]
            if arg2 == "init" and arg3 == "account":
                local.init_account()
            elif arg2 == "init" and arg3 == "provider":
                provider = getpass("PROVIDER: ")
                local.provider_file(provider=provider, chain_id=1)
                print("Mainnet provider has been set.")
            elif arg2 == "init" and arg3 == "location":
                ext_file_path = input("DRAG AND DROP EXTERNAL DRIVE: ")
                local.wallet_path(path=ext_file_path)
                print("Wallet location has been set.")
            if arg2 == "account" and arg3 == "--testnet":
                wallet.balance(testnet=True)
            if arg2 == "price":
                ether = utils.eth_price(arg3)
                print(f"${ether:.2f}")
            if arg2 == "gas":
                estimate = utils.eth_estimate(arg3, 1)
                print(f"${estimate:.2f}")
            if arg2 == "send" and arg3 == "--testnet":
                transaction.send_transaction(testnet=True)
        elif len(args) == 3:
            arg2 = argv[1]
            arg3 = argv[2]
            arg4 = argv[3]
            if arg2 == "init" and arg3 == "provider" and arg4 == "--testnet":
                provider = getpass("PROVIDER: ")
                chain_id = input("CHAIN ID: ")
                local.provider_file(provider=provider, chain_id=chain_id, testnet=True)
                print("Testnet provider has been set.")
            elif arg2 == "init" and arg3 == "account" and arg4 == "--testnet":
                local.init_account(testnet=True)
            if arg2 == "gas":
                estimate = utils.eth_estimate(arg3, arg4)
                print(f"${estimate:.2f}")
            if arg2 == "convert":
                convert = utils.unit_convert(arg3, arg4)
                print(f"{convert[0]:.16f}".rstrip("0").rstrip("."), "ETH")
                print(f"{convert[1]:.16f}".rstrip("0").rstrip("."), "GWEI")
                print(f"{convert[2]:.16f}".rstrip("0").rstrip("."), "WEI")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
