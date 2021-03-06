
import pybithumb
import numpy as np
import time
import datetime

def get_ror():
    df = pybithumb.get_ohlcv("BTC").tail()
    df['noise'] = 1 - abs(df['open'] - df['close']) / (df['high'] - df['low'])
    df['noise_ma20'] = df['noise'].rolling(window=20, min_periods=1).mean()
    df['ma5'] = df['close'].rolling(window=15).mean().shift(1)
    df['range'] = (df['high'] - df['low']) * 0.5
    df['target'] = df['open'] + df['range'].shift(1) * df['noise_ma20']
    df['bull'] = df['open'] > df['ma5']
    
    fee = 0.0032
    df['ror'] = np.where((df['high'] > df['target']) & df['bull'],
                      df['close'] / df['target'] - fee,
                      1)

    df['hpr'] = df['ror'].cumprod()
    df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
    print("MDD: ", df['dd'].max())
    print("HPR: ", df['hpr'][-2])
    df.to_excel("larry_ma.xlsx")

    ror = df['ror'].cumprod()[-2]
    return ror

get_ror()
# for k in np.arange(0.1, 1.0, 0.1):
#     ror = get_ror(k)
#     print("%.1f %f" % (k, ror))
