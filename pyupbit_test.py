import time
import datetime
import os
import logging

from dotenv import load_dotenv
import pyupbit
from pyupbit.exchange_api import Upbit

from util import get_target_price, set_logger


load_dotenv()
access_key = os.getenv('UPBIT_OPEN_API_ACCESS_KEY')
secret_key = os.getenv('UPBIT_OPEN_API_SECRET_KEY')
server_url = os.getenv('UPBIT_OPEN_API_SERVER_URL')

upbit = Upbit(access_key, secret_key)

TICKER = 'KRW-BTC'

now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
target_price = get_target_price(TICKER)

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


while True:
    try:
        now = datetime.datetime.now()
        logger.info(f"no change")

        if mid < now < mid + datetime.timedelta(seconds=10):
            target_price = get_target_price(TICKER)
            logger.warn(f"target price : {target_price}")
            mid = datetime.datetime(
                now.year, now.month, now.day) + datetime.timedelta(1)
            logger.warn(f"mid time refreshed : {mid}")
            sell_crypto_currency(TICKER)

        current_price = pyupbit.get_current_price(TICKER)
        if current_price > target_price:
            buy_crypto_currency(TICKER)

    except Exception as err:
        logger.error(err)

    time.sleep(1)
