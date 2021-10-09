import logging
import os

import pyupbit

from algo import get_moving_average


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


def get_target_price(ticker):
    df = pyupbit.get_ohlcv(ticker)
    yesterday = df.iloc[-2]

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target


def set_logger():
    os.makedirs('log', exist_ok=True)
    log_path = './log/error.log'

    complex_formatter = logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(complex_formatter)
    console_handler.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(complex_formatter)
    file_handler.setLevel(logging.WARN)

    root_logger = logging.getLogger('root_logger')
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.INFO)
