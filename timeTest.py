import pybithumb
import numpy as np
import time
import datetime

def get_target_price(ticker):
    df = pybithumb.get_ohlcv(ticker)
    yesterday = df.iloc[-2]

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target

now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day,9) + datetime.timedelta(1)
target_price = get_target_price("BTC")

while True:
    try:
        now = datetime.datetime.now()
        print(now)
        if mid < now < mid + datetime.delta(seconds=10): 
            target_price = get_target_price("BTC")
            print(target_price)
            mid = datetime.datetime(now.year, now.month, now.day, 9) + datetime.timedelta(days=1)
            print(mid)
            print("sell BTC")
            #sell_crypto_currency("BTC")
    
        current_price = pybithumb.get_current_price("BTC")
        print("current_price: ", current_price)       
        print("mid = ", mid)
        print("target = ", target_price) 
        if current_price > target_price:
            print("buy BTC")
            #buy_crypto_currency("BTC")        
    except:
        print("에러 발생")        
    time.sleep(1)