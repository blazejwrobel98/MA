

import requests
mkt = []
url = "https://api.zonda.exchange/rest/trading/ticker"

headers = {'content-type': 'application/json'}

response = requests.request("GET", url, headers=headers)
for element in response.json()['items'].keys():
    mkt.append(element)

with open('markets.txt', 'w') as f:
    # write mkt list to file with each element on a new line
    for item in mkt:
        if "PLN" in item:
            f.write(item + '\n')

with open('markets.txt', 'r') as f:
    markets = f.read().splitlines()
    print(markets)

