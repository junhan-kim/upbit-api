import os
import requests
from dotenv import load_dotenv


load_dotenv()
server_url = os.getenv('UPBIT_OPEN_API_SERVER_URL')


def get_candle(market_id, unit, count, min_unit=None):
    querystring = {"market": market_id, "count": count}

    headers = {"Accept": "application/json"}

    if unit == 'minutes':
        response = requests.request(
            "GET", f"{server_url}/v1/candles/{unit}/{min_unit}", headers=headers, params=querystring)
    else:
        response = requests.request(
            "GET", f"{server_url}/v1/candles/{unit}", headers=headers, params=querystring)

    return response.json()


# 체결량 조회
def get_tick(market_id, count):
    querystring = {
        "market": market_id,
        "count": count
    }

    headers = {"Accept": "application/json"}

    response = requests.request(
        "GET", f"{server_url}/v1/trades/ticks", headers=headers, params=querystring)

    return response.json()
