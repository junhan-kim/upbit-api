import pyupbit


def get_moving_average(close, window_size):
    window = close.rolling(window_size)
    ma = window.mean()
    return ma


def is_bull_market():
    # open / high / low / close / volume
    ohlcv = pyupbit.get_ohlcv(
        "KRW-BTC", interval="minute15", count=300)  # 15 분봉
    price = pyupbit.get_current_price("KRW-BTC")

    close = ohlcv['close']

    # ma5 = get_moving_average(close, 5)
    # ma10 = get_moving_average(close, 10)
    ma20 = get_moving_average(close, 20)
    # ma60 = get_moving_average(close, 60)
    # ma120 = get_moving_average(close, 120)

    last_ma = ma20[-2]

    return True if price > last_ma else False
