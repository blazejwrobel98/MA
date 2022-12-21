# get current data from 'https://www.tradingview.com/chart/?symbol=EASYMARKETS%3AOILUSD'
# and save it to 'data.csv'

import requests
import csv
import time
import datetime


def get_data():
    url = 'https://www.tradingview.com/chart/?symbol=EASYMARKETS%3AOILUSD'
    response = requests.get(url)
    data = response.text
    return data


def save_data(data):
    with open('data.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)


def main():
    while True:
        data = get_data()
        save_data(data)
        time.sleep(60)


if __name__ == '__main__':
    main()
