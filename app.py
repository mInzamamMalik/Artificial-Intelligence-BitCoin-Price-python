import requests
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from threading import Timer


def price(symbol, comparison_symbols=['USD'], exchange=''):
    url = 'https://min-api.cryptocompare.com/data/price?fsym={}&tsyms={}'.format(
        symbol.upper(), ','.join(comparison_symbols).upper())
    if exchange:
        url += '&e={}'.format(exchange)
    page = requests.get(url)
    data = page.json()
    return data


def daily_price_historical(symbol, comparison_symbol, all_data=True, limit=1, aggregate=1, exchange=''):
    url = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}&limit={}&aggregate={}' \
        .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)
    if exchange:
        url += '&e={}'.format(exchange)
    if all_data:
        url += '&allData=true'
    page = requests.get(url)
    data = page.json()['Data']

    # print("data: ", data)

    df = pd.DataFrame(data)

    # print("df: ", df)

    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    return df


df = daily_price_historical('BTC', 'USD')


def getData():
    df = daily_price_historical('BTC', 'USD')
    print("getting new data: ", datetime.datetime.now())
    # plt.clear()

    plt.title("BitCoin Rate (All time)")
    plt.ylabel("1 Btc Price (USD)")
    plt.xlabel("Over Time")

    plt.plot(df.timestamp, df.close)

    Timer(3.0, getData).start()


getData()

# print(df)
plt.plot(df.timestamp, df.close)
plt.show()
