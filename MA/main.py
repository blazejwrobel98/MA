import json
import time
import requests

pairs = ['ETH-PLN', 'DOGE-PLN', 'SHIB-PLN', 'KSM-PLN', 'REEF-PLN']
with open('markets.txt', 'r') as f:
    pairs = f.read().splitlines()

mas = ["ma_short", "ma_long"]
wallet = {}
best_ma = {}


def buy_crypto(_i, _pair):
    wallet[_pair][_pair.split("-")[0]] = round((wallet[_pair][_pair.split("-")[1]] / _i) * 0.9957, 8)
    wallet[_pair][_pair.split("-")[1]] = 0.0
    wallet[_pair]['rounded'] = round((wallet[_pair][_pair.split("-")[0]] * _i) * 0.9957, 2)
    wallet_history.append([wallet[_pair][_pair.split("-")[0]], wallet[_pair][_pair.split("-")[1]]])


def sell_crypto(_i, _pair):
    wallet[_pair][_pair.split("-")[1]] = round((wallet[_pair][_pair.split("-")[0]] * _i) * 0.9957, 2)
    wallet[_pair][_pair.split("-")[0]] = 0.0
    wallet[_pair]['rounded'] = 0.0
    wallet_history.append([wallet[_pair][_pair.split("-")[0]], wallet[_pair][_pair.split("-")[1]]])


def get_candles(_pair):
    timestamp = int(time.time() * 1000)
    # from_timestamp = timestamp - 1 month in milliseconds
    from_timestamp = timestamp - 2592000000*5
    url = f"https://api.zonda.exchange/rest/trading/candle/history/{_pair}/3600?from={from_timestamp}&to={timestamp}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers).json()
    closing_price = []
    for element in response['items']:
        closing_price.append(round(float(element[1]['c']), 8))
    return closing_price


if __name__ == '__main__':
    for _pair in pairs:
        wallet[_pair] = {
            _pair.split('-')[0]: 0.00,
            _pair.split('-')[1]: 100.00,
            'rounded': 0.00
        }
    for _pair in pairs:
        best_ma[_pair] = {
        }
        for ma in mas:
            best_ma[_pair][ma] = {
                'length': 0,
                'money': 0.00
            }
    print(f"Starting money: {len(pairs) * 100} PLN")
    for _pair in pairs:
        try:
            closing_prices = get_candles(_pair)
            wallet_history = []
            wallet_history.append([wallet[_pair][_pair.split("-")[0]], wallet[_pair][_pair.split("-")[1]]])
            ongoing_prices = []
            ma_short, ma_long = 0.00, 0.00
            for _ma_long in range(1, 100):
                for _ma_short in range(1, 100):
                    if _ma_short >= _ma_long:
                        continue
                    for _price in closing_prices:
                        ongoing_prices.append(float(_price))
                        if len(ongoing_prices) > _ma_long:
                            ma_short = round(sum(ongoing_prices[-_ma_short:]) / _ma_short, 8)
                            ma_long = round(sum(ongoing_prices[-_ma_long:]) / _ma_long, 8)
                            if ma_long < ma_short and wallet[_pair][_pair.split("-")[1]] > 0 and _price > \
                                    ongoing_prices[-2]:
                                # BUY
                                buy_crypto(_price, _pair)
                                continue
                            if ma_long > ma_short and wallet[_pair][
                                _pair.split("-")[0]] > 0 and round(
                                (wallet[_pair][_pair.split("-")[0]] * _price) * 0.9957, 2) > \
                                    wallet_history[-2][1] and _price < ongoing_prices[-2]:
                                # SELL
                                sell_crypto(_price, _pair)
                                continue
                        if round(wallet[_pair]['rounded'] + wallet[_pair][_pair.split('-')[1]], 2) > \
                                best_ma[_pair]['ma_short']['money']:
                            best_ma[_pair]['ma_short']['length'] = _ma_short
                            best_ma[_pair]['ma_short']['money'] = round(
                                wallet[_pair]['rounded'] + wallet[_pair][_pair.split('-')[1]], 2)
                    if round(wallet[_pair]['rounded'] + wallet[_pair][_pair.split('-')[1]], 2) > \
                            best_ma[_pair]['ma_long']['money']:
                        best_ma[_pair]['ma_long']['length'] = _ma_long
                        best_ma[_pair]['ma_long']['money'] = round(
                            wallet[_pair]['rounded'] + wallet[_pair][_pair.split('-')[1]], 2)
        except:
            print(f"Error with {_pair}")
        print(wallet[_pair])
        time.sleep(1)
print(
    f"Ending money: {round(sum([wallet[pair]['rounded'] for pair in pairs]) + sum([wallet[pair]['PLN'] for pair in pairs]), 2)} PLN")

with open('best_ma.json', 'w') as outfile:
    json.dump(best_ma, outfile)

top_10_pairs = []
for pair in pairs:
    top_10_pairs.append([pair, round(wallet[pair]['rounded'] + wallet[pair]['PLN'], 2)])
top_10_pairs.sort(key=lambda x: x[1], reverse=True)
print(top_10_pairs[:10])


