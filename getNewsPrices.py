import requests
import pandas as pd
import time
import json

def init_file (csv_file, col):
    df = pd.read_csv(csv_file)
    df[col] = None
    df.to_csv(csv_file, index=False)
    print('done!')

def get_stock_one(symbol, n=20, lastId=None):
    last = ''
    if lastId:
        last = f'&last={lastId}'
    url = f"https://api.tickertick.com/feed?q=(and tt:{symbol} T:curated)&n={n}{last}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        filtered = [body.get('description', body.get('title')) for body in data['stories']]
        result = {'data':filtered, 'lastId': data['stories'][-1]['id']}
        return json.dumps(result)
    else:
        print("Failed to get news data, status code:", response.status_code)


def add_news_prices(csv_file):
       df = pd.read_csv(csv_file)
    index = index
    #send request to api one by one
    while index <= 505:
        symbol = df.loc[index, 'Symbol']
        print(index, symbol)
        res = get_stock_one(symbol)
        news = res['data']
        daily = get_price(symbol, 'daily', 14)
        df.loc[index, '14days'] = daily
        time.sleep(12)
        weekly = get_price(symbol, 'weely', 7)
        df.loc[index, '7weeks'] = weekly
        # avoid reaching api requests limit
        time.sleep(12)
        while len(news) < 10:
            id = res['lastId']
            temp = get_stock_one(symbol, id)
            # avoid reaching api requests limit
            time.sleep(10)
            news = news.union(temp['data'])
        df.loc[index, 'News'] = str(news)
        df.to_csv(csv_file, index=False)
        print(index, symbol, 'prices and news added!')
        index += 1
    #write to the csv file

    print('done!')
    return 'news done'

def add_prices(csv_file):
    df = pd.read_csv(csv_file)
    index = 0
    #send request to api one by one
    while index <= 505:
        symbol = df.loc[index, 'Symbol']
        print(index, symbol)
        daily = get_price('daily', 14)
        df.loc[index, '14days'] = daily
        time.sleep(12)
        weekly = get_price('weekly', 7)
        df.loc[index, '7weeks'] = weekly
        time.sleep(12)
        df.to_csv(csv_file, index=False)
        index += 1
    print('prices added done!')

init_file('sp500_info.csv', 'News')
add_news_prices('sp500_info.csv')