import pyupbit

from algo import get_moving_average
from plot import plot_df


# open / high / low / close / volume
ohlcv = pyupbit.get_ohlcv(
    "KRW-BTC", interval="minute15", count=300)  # 15 분봉
close = ohlcv['close']

ma5 = get_moving_average(close, 5)
ma10 = get_moving_average(close, 10)
ma20 = get_moving_average(close, 20)
ma60 = get_moving_average(close, 60)
ma120 = get_moving_average(close, 120)

plot_df([ma5, ma10, ma20, ma60, ma120])
