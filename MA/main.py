import time
import requests

pairs = ['BTC-PLN', 'ETH-PLN', 'XRP-PLN', 'LSK-PLN', 'DOGE-PLN']
wallet = {}
for pair in pairs:
    wallet[pair] = {
        pair.split('-')[0]: 0.00,
        pair.split('-')[1]: 100.00,
        'rounded': 0.00
    }

best_ma = {}
mas = ["ma8", "ma13", "ma21", "ma55"]
for pair in pairs:
    best_ma[pair] = {
    }
    for ma in mas:
        best_ma[pair][ma] = {
            'length': 0,
            'money': 0.00
        }

print(best_ma)


def get_candles(pair):
    timestamp = int(time.time() * 1000)
    # from_timestamp = timestamp - 1 month in milliseconds
    from_timestamp = timestamp - 2592000000
    url = f"https://api.zonda.exchange/rest/trading/candle/history/{pair}/3600?from={from_timestamp}&to={timestamp}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers).json()
    closing_price = []
    for element in response['items']:
        closing_price.append(round(float(element[1]['c']), 8))
    return closing_price


if __name__ == '__main__':
    print(f"Starting money: {len(pairs) * 100} PLN")
    for pair in pairs:
        try:
            closing_prices = get_candles(pair)
            wallet_history = []
            wallet_history.append([wallet[pair][pair.split("-")[0]], wallet[pair][pair.split("-")[1]]])
            ongoing_prices = []
            ma8, ma13, ma21, ma55 = 0.00, 0.00, 0.00, 0.00
            for i in closing_prices:
                ongoing_prices.append(float(i))
                for _ma55 in range(50, 100):
                    for _ma21 in range(20, 49):
                        if len(ongoing_prices) > _ma55:
                            ma8 = round(sum(ongoing_prices[-8:]) / 8, 8)
                            ma13 = round(sum(ongoing_prices[-13:]) / 13, 8)
                            ma21 = round(sum(ongoing_prices[-_ma21:]) / _ma21, 8)
                            ma55 = round(sum(ongoing_prices[-_ma55:]) / _ma55, 8)
                            if ma55 < ma21 and ma55 < ma13 and ma55 < ma8 and wallet[pair][
                                pair.split("-")[1]] > 0 and i > \
                                    ongoing_prices[-2]:
                                # BUY
                                wallet[pair][pair.split("-")[0]] = round(
                                    (wallet[pair][pair.split("-")[1]] / i) * 0.9957, 8)
                                wallet[pair][pair.split("-")[1]] = 0.0
                                wallet[pair]['rounded'] = round((wallet[pair][pair.split("-")[0]] * i) * 0.9957, 2)
                                wallet_history.append(
                                    [wallet[pair][pair.split("-")[0]], wallet[pair][pair.split("-")[1]]])
                            elif ma55 > ma21 and ma55 > ma13 and ma55 > ma8 and wallet[pair][
                                pair.split("-")[0]] > 0 and round(
                                (wallet[pair][pair.split("-")[0]] * i) * 0.9957,
                                2) > wallet_history[-2][
                                1] and i < ongoing_prices[-2]:
                                # SELL
                                wallet[pair][pair.split("-")[1]] = round(
                                    (wallet[pair][pair.split("-")[0]] * i) * 0.9957, 2)
                                wallet[pair][pair.split("-")[0]] = 0.0
                                wallet[pair]['rounded'] = 0.0
                                wallet_history.append(
                                    [wallet[pair][pair.split("-")[0]], wallet[pair][pair.split("-")[1]]])
                        if round(wallet[pair]['rounded'] + wallet[pair][pair.split('-')[1]], 2) > best_ma[pair]['ma21'][
                            'money']:
                            best_ma[pair]['ma21']['length'] = _ma55
                            best_ma[pair]['ma21']['money'] = round(
                                wallet[pair]['rounded'] + wallet[pair][pair.split('-')[1]], 2)
                    if round(wallet[pair]['rounded'] + wallet[pair][pair.split('-')[1]], 2) > best_ma[pair]['ma55'][
                        'money']:
                        best_ma[pair]['ma55']['length'] = _ma55
                        best_ma[pair]['ma55']['money'] = round(
                            wallet[pair]['rounded'] + wallet[pair][pair.split('-')[1]], 2)
            print(f"Best MA21 for {pair}: {best_ma[pair]['ma21']['length']}, money: {best_ma[pair]['ma21']['money']}")
            print(f"Best MA55 for {pair}: {best_ma[pair]['ma55']['length']}, money: {best_ma[pair]['ma55']['money']}")
        except:
            print(f"Error with {pair}")
        print(wallet[pair])
        time.sleep(1)
print(
    f"Ending money: {round(sum([wallet[pair]['rounded'] for pair in pairs]) + sum([wallet[pair]['PLN'] for pair in pairs]), 2)} PLN")
