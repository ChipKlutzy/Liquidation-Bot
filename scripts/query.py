import requests, json, time

url = "https://api.thegraph.com/subgraphs/name/aave/protocol-v3-polygon"

def USD_GT(amount):
    return 10 ** 8 * amount  

def get_Target_user(no_of_responses, amount):

    users_batch = []

    for i in range(no_of_responses):

        body = """
        {
            users(first: 1000, skip: """ + str(i * 1000) + """, orderBy: id, orderDirection: desc, where: {borrowedReservesCount_gt: 0}) {
                id
                borrowedReservesCount
                collateralReserve:reserves(where: {currentATokenBalance_gt: 0}) {
                currentATokenBalance
                reserve{
                    usageAsCollateralEnabled
                    reserveLiquidationThreshold
                    reserveLiquidationBonus
                    borrowingEnabled
                    utilizationRate
                    symbol
                    underlyingAsset
                    price {
                    priceInEth
                    }
                    decimals
                }
            }
                borrowReserve: reserves(where: {currentTotalDebt_gt: 0}) {
                currentTotalDebt
                reserve{
                    usageAsCollateralEnabled
                    reserveLiquidationThreshold
                    borrowingEnabled
                    utilizationRate
                    symbol
                    underlyingAsset
                    price {
                    priceInEth
                    }
                    decimals
                }
            }
            }
        }
        """

        response = requests.post(url=url, json={'query': body})
        
        if(response.status_code == 200):
            Json_Response = json.loads(response.content)
            Users = Json_Response['data']['users']
            users_batch += Users


    target_users = []
    
    for user in users_batch:

        totalDebt = 0
        for brc in range(len(user['borrowReserve'])):
            priceInETH = int(user['borrowReserve'][brc]['reserve']['price']['priceInEth']) 
            principleBorrowed = int(user['borrowReserve'][brc]['currentTotalDebt']) / (10 ** user['borrowReserve'][brc]['reserve']['decimals'])
            totalDebt += priceInETH * principleBorrowed

        totalCollateral = 0
        totalCollateralThreshold = 0
        for crc in range(len(user['collateralReserve'])):
            priceInETH = int(user['collateralReserve'][crc]['reserve']['price']['priceInEth']) 
            principleAtokenBalance = int(user['collateralReserve'][crc]['currentATokenBalance']) / (10 ** user['collateralReserve'][crc]['reserve']['decimals'])
            totalCollateral += priceInETH * principleAtokenBalance
            totalCollateralThreshold += priceInETH * principleAtokenBalance * (int(user['collateralReserve'][crc]['reserve']['reserveLiquidationThreshold']) / 10000)

        if(totalDebt != 0):
            healthFactor = totalCollateralThreshold / totalDebt
            if(healthFactor >= 1 and healthFactor <=1.50 and totalDebt > USD_GT(amount)):
                target_users.append({
                    'address': user['id'], 
                    'healthFactor': healthFactor, 
                    'totalCollateralUSD': int(totalCollateral/1e8), 
                    'totalDebtUSD': int(totalDebt/1e8), 
                    'CollateralCount': len(user['collateralReserve']), 
                    'DebtCount': len(user['borrowReserve'])})

    return target_users
    
    

def main():

    start_time = time.time()

    t_users = get_Target_user(6, 100000)    

    print(len(t_users))

    for user_info in t_users:
        print("\n")
        print(user_info)

    end_time = time.time()

    print(f"Time taken to get Target Users : {int(end_time - start_time)} s")

    








        



