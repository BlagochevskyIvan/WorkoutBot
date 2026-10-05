import hashlib
import hmac
import json
import time
import os
from server.auth.telegram import _validate_init_data, get_telegram_user_id
from urllib.parse import urlencode
import pytest
from fastapi import HTTPException

TELEGRAM_TOKEN= os.getenv("TELEGRAM_TOKEN")

def make_init_data(telegram_id, token, auth_date, fake_hash=None):
    user = json.dumps({"id": telegram_id, 'first_name': 'Test', 'last_name': 'User', 'username': 'testuser'}, separators=(',', ':'))
    pairs = {
        "user": user,
        "auth_date": str(auth_date)
    }
    data_check_string = "\n".join(
            f"{key}={value}" for key, value in sorted(pairs.items())
        )
    secret_key = hmac.new(
            b"WebAppData",
            token.encode(),
            hashlib.sha256,
        ).digest()
    
    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
            hashlib.sha256,
        ).hexdigest()
    
    if fake_hash is not None:
        calculated_hash = fake_hash

    query = urlencode({**pairs, 'hash': calculated_hash})
    return query

def test_validate_init_data():
    init_data = make_init_data(telegram_id=123456, token=TELEGRAM_TOKEN, auth_date=int(time.time()))
    parsed = _validate_init_data(init_data)
    parsed_user = json.loads(parsed['user'])
    assert parsed_user['id'] == 123456

# негативный тест
def test_validate_init_data_expired():
    init_data = make_init_data(telegram_id=123456, token=TELEGRAM_TOKEN, auth_date=int(time.time()) - 90000)

    with pytest.raises(HTTPException) as excinfo:
        _validate_init_data(init_data)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "initData устарела"

def test_validate_init_data_invalid_hash():
    init_data = make_init_data(telegram_id=123456, token=TELEGRAM_TOKEN, auth_date=int(time.time()), fake_hash="invalidhash")

    with pytest.raises(HTTPException) as excinfo:
        _validate_init_data(init_data)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Неверная подпись initData"

def test_get_telegram_user_id():
    init_data = make_init_data(telegram_id=123456, token=TELEGRAM_TOKEN, auth_date=int(time.time()))
    user_id = get_telegram_user_id(init_data)
    assert user_id == 123456





