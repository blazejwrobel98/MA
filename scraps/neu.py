
NEU_TAX = 0.003
PLN_TAX = 0.004
neu_buy = 0.200
neu_sell = 0.213
wallet = {
    "pln": 0,
    "neu": 0,
    "on_plus": 0,
    "last_buy": 0,
}


def buy_neu(pln):
    neu = round(pln * (1 - NEU_TAX) / neu_buy, 8)
    wallet["last_buy"] = pln
    wallet["pln"] -= pln
    wallet["neu"] += neu


def sell_neu(neu):
    pln = round(neu * neu_sell * (1 - PLN_TAX), 2)
    wallet["on_plus"] = round(pln - wallet["last_buy"], 2)
    wallet["pln"] += pln
    wallet["neu"] -= neu


if __name__ == '__main__':
    start_pln = input('How much PLN do you want to invest? ')
    wallet["pln"] = float(start_pln)
    i = 0
    w = 1
    while wallet["pln"] < 1000000:
        buy_neu(wallet["pln"])
        sell_neu(wallet["neu"])
        print(f'[TRADE: {i} WEEK: {w}] You have {wallet["pln"]} PLN, profit: {wallet["on_plus"]}')
        i += 1
        if i % 7 == 0:
            w += 1