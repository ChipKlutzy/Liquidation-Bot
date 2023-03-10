import requests, json

def main():

    url = "https://api.thegraph.com/subgraphs/name/aave/aave-v2-matic"

    body = """
    {
    users(
        first: 10000,
        skip: 5000, 
        orderBy: id, 
        orderDirection: asc, 
        where: {borrowedReservesCount_gt: 0}) {
        id
    }
    }
    """

    response = requests.post(url=url, json={'query': body})

    if(response.status_code == 200):
        Json_Response = json.loads(response.content)
        Users = Json_Response['data']['users']
        print(len(Users))