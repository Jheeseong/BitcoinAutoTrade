import time
import pybithumb
import datetime
import requests

# """슬랙 메시지 전송"""
def post_message(token, channel, text):
    
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )

# 변경성 돌파 전략으로 매수 목표가 조회
def get_target_price(ticker):
    df = pybithumb.get_ohlcv(ticker)
    yesterday = df.iloc[-2]

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target

# 매수
def buy_crypto_currency(ticker):
    # 원화 잔고 확인
    krw = bithumb.get_balance(ticker)[2]
    print("원화 = ", krw)
    # 매도 호가 내역 조회
    orderbook = pybithumb.get_orderbook(ticker) 
    sell_price = orderbook['asks'][0]['price']   
    # 매수 수량
    unit = krw/float(sell_price)
    # 매수
    order = bithumb.buy_market_order(ticker, unit*0.5)
    post_message(myToken,"#bitcoin","buy the coin =",order)

# 매도
def sell_crypto_currency(ticker):
    unit = bithumb.get_balance(ticker)[0]
    sell = bithumb.sell_market_order(ticker, unit)
    post_message(myToken, "#bitcoin", "sell the coin =",sell)

# MA-15
def get_yesterday_ma15(ticker):
    df = pybithumb.get_ohlcv(ticker)
    close = df['close']
    ma = close.rolling(15).mean()
    return ma[-2]

access = "c15d88ebfd1258f8ce17113a27ae13c5"
secret = "7fe7f2afc7e34433306c84f37c3be737"
bithumb = pybithumb.Bithumb(access, secret)

myToken = "xoxb-3348226843249-3337959274820-CU2f0XUxBQZS6PcMM7pP2B0y"

now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
coin = "SAND"
ma15 = get_yesterday_ma15(coin)
target_price = get_target_price(coin)

post_message(myToken, "#bitcoin", "autotrade start")

while True:
    try:
        now = datetime.datetime.now()
        if mid < now < mid + datetime.delta(seconds=10): 
            target_price = get_target_price(coin)
            print(target_price)
            mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
            print(mid)
            ma15 = get_yesterday_ma15(coin)
            sell_crypto_currency(coin)
    
        current_price = pybithumb.get_current_price(coin)      
        print("current price =", current_price)  
        print("target_price", target_price)
        if (current_price > target_price) and (current_price > ma15):
            buy_crypto_currency(coin)        
    except:
        print("에러 발생")
        post_message(myToken,"#bitcoin","에러 발생")        
    time.sleep(1)