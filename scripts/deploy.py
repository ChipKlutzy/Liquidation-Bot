from brownie import LiquidationBot, network, accounts, config, chain

def get_account():

    LIVE_NETWORKS = ["mainnet", "polygon-main"]

    if(network.show_active() in LIVE_NETWORKS):
        sender = accounts.add(
            config["wallets"][network.show_active()]["private-key"]
        )
    else:
        sender = accounts.load("PolygonAccount1")

    return sender



def main():

    sender = get_account()

    # Contract Polygon Address - 0x4CDaCC243eD5fCeBedB0977d8D8B92440e59BEef

    # LB = LiquidationBot.deploy(
    #     config["networks"][network.show_active()]["address_provider"],
    #     config["networks"][network.show_active()]["router02"],
    #     {'from': sender}
    # )

    # print(LB.address)

    print(LiquidationBot[-1])


