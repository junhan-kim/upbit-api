import os
import logging
import time
import datetime
import traceback

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
    balance = upbit.get_balance(ticker) * 0.95
    upbit.sell_market_order(ticker, balance)
    logger.warning(f"sell {ticker}: {balance}")


def buy_crypto_currency(ticker):
    krw_balance = int(upbit.get_balance('KRW') * 0.95)
    upbit.buy_market_order(ticker, krw_balance)
    logger.warning(f"buy {ticker}: {krw_balance}")


if __name__ == "__main__":

    ticker = 'KRW-BTC'

    while True:
        try:
            now = datetime.datetime.now()
            balance = int(upbit.get_balance('KRW'))

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
            # plot_df([df['bb_bbhi'], df['bb_bbli']])

            high_band_price = df['bb_bbh'][-1]
            low_band_price = df['bb_bbl'][-1]
            now_price = pyupbit.get_current_price(ticker)
            is_high = df['bb_bbhi'][-1] == 1.0
            is_low = df['bb_bbli'][-1] == 1.0

            now_status = 'None'
            if is_high:
                logger.warning('high indicated')
                now_status = 'high'
                buy_crypto_currency(ticker)
            elif is_low:
                logger.warning('low indicated')
                now_status = 'low'
                sell_crypto_currency(ticker)
            else:
                pass

            logger.info(
                f"bal: {balance}, cur: {int(now_price)}, high: {int(high_band_price)}, low: {int(low_band_price)}, stat: {now_status}")

        except Exception as err:
            logger.error(err)
            traceback.print_exc()

        time.sleep(1)
