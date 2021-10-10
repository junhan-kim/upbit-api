import os
import logging
import time
import datetime

from ta.volatility import BollingerBands
from dotenv import load_dotenv
import pyupbit
from pyupbit.exchange_api import Upbit

from util import set_logger
from plot import plot_df


load_dotenv()
access_key = os.getenv('UPBIT_OPEN_API_ACCESS_KEY')
secret_key = os.getenv('UPBIT_OPEN_API_SECRET_KEY')
server_url = os.getenv('UPBIT_OPEN_API_SERVER_URL')
upbit = Upbit(access_key, secret_key)

set_logger()
logger = logging.getLogger('root_logger')


def sell_crypto_currency(ticker):
    btc_balance = upbit.get_balance(ticker)
    upbit.sell_market_order(ticker, btc_balance)
    logger.warn(f"sell {ticker}: {btc_balance}")


def buy_crypto_currency(ticker):
    krw_balance = upbit.get_balance('KRW')

    orderbook = pyupbit.get_orderbook(ticker)
    sell_price = orderbook['orderbook_units'][0]['ask_price']
    unit = krw_balance / sell_price

    upbit.buy_market_order(ticker, unit)
    logger.warn(f"buy {ticker}: {unit}")


if __name__ == "__main__":

    ticker = 'KRW-BTC'

    while True:
        try:
            now = datetime.datetime.now()
            # logger.info(f"no change")

            # get bb
            df = pyupbit.get_ohlcv(ticker, interval='minute15', count=500)
            indicator_bb = BollingerBands(
                close=df["close"], window=20, window_dev=2)

            # bb features
            df['bb_bbm'] = indicator_bb.bollinger_mavg()
            df['bb_bbh'] = indicator_bb.bollinger_hband()
            df['bb_bbl'] = indicator_bb.bollinger_lband()

            # high and low indicater
            df['bb_bbhi'] = indicator_bb.bollinger_hband_indicator()
            df['bb_bbli'] = indicator_bb.bollinger_lband_indicator()

            high_band_price = df['bb_bbh'][-1]
            low_band_price = df['bb_bbl'][-1]
            is_high = df['bb_bbhi'][-1]
            is_low = df['bb_bbli'][-1]
            now_price = df['close'][-1]

            logger.info(
                f"cur: {now_price}, high: {high_band_price}, low: {low_band_price}")

            if is_high:
                logger.warn('high indicated')
                buy_crypto_currency(ticker)
            elif is_low:
                logger.warn('low indicated')
                sell_crypto_currency(ticker)
            else:
                pass

        except Exception as err:
            logger.error(err)

        time.sleep(1)
