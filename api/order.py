import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import requests
from dotenv import load_dotenv


load_dotenv()
access_key = os.getenv('UPBIT_OPEN_API_ACCESS_KEY')
secret_key = os.getenv('UPBIT_OPEN_API_SECRET_KEY')
server_url = os.getenv('UPBIT_OPEN_API_SERVER_URL')


def get_chance(query):
    """[summary]
    Args:
        market_id (string): 마켓 아이디
    """
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get(server_url + "/v1/orders/chance",
                       params=query, headers=headers)

    return res.json()


def order(query):
    """[summary]
    Args:
        market_id (string): 마켓 아이디
        side (string): 주문 종류 (bid/ask : 매수/매도)
        volume (string): 주문량 (매도)
        price (string): 주문 가격 (매수)
        ord_type (string): 주문 타입 (limit/price/market : 지정가 주문/시장가 매수/시장가 매도)
        identifier (string): 조회용 사용자 지정 값
    """
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post(server_url + "/v1/orders",
                        params=query, headers=headers)

    return res.json()
