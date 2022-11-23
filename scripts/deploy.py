from brownie import LiquidationBot, network, accounts, config, Contract, chain, interface

def Price(oracle, asset):

    return (oracle.getAssetPrice(asset) / 1e8) # Asset prices in USD, So decimal value is 8 

    
def Deploy(addr):

    print(f"Deploying the required contracts on {network.show_active()}..............\n")

    LB = LiquidationBot.deploy(
        config["networks"][network.show_active()]["aave_v3_address_provider"],
        {'from': addr}
    )

    print(f"1. Liquidation Bot contract deployed @ {LB.address}\n")

    return LB

def Interface(addr1, addr2 = None):

    print(f"Fetching contracts from {network.show_active()} \n")

    if(addr2 != None):
        param2 = config["networks"][network.show_active()][addr2]
    else:
        param2 = None

    ReqContract = Contract.from_explorer(
        config["networks"][network.show_active()][addr1],
        param2
    )

    return ReqContract

def TimeStamp(blockNumber):

    currBlock = chain[-1]
    CTime = currBlock['timestamp']

    TargetBlock = chain[blockNumber] 
    TTime = TargetBlock['timestamp']

    timeElapsed = CTime - TTime
    timeElapsed /= (60 * 60 * 24)

    return timeElapsed


def main():
    sender = accounts.add(
        config["wallets"][network.show_active()]["private-key"]
    )

     # LB = Deploy(sender) # This line is an Ethereum Transaction (deploying a contract)

    LendingPool = Interface("lending_pool_proxy", "lending_pool")

    AaveOracle = Interface("aave_oracle")

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    fromblockNumber = chain.height - 1000

    eventName = LendingPool.events.Borrow

    EventLogs = LendingPool.events.get_sequence(fromblockNumber, None, eventName)

    Borrowers_List = []
    for Adict in EventLogs:
        args = Adict["args"]
        user = args["onBehalfOf"]
        Borrowers_List.append(user)

    for borrower in Borrowers_List:
        UserData = LendingPool.getUserAccountData(borrower)
        health_factor = UserData[-1] / 1e18
        print((borrower, health_factor))




