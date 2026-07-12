import hashlib
import hmac
import json
import time
from urllib.parse import parse_qsl

from fastapi import HTTPException

from config.cp_config import TELEGRAM_TOKEN
from config.logger import logger


# Проверяем подпись initData по доке Telegram
# https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
def _validate_init_data(init_data: str, max_age_seconds: int = 86400) -> dict[str, str]:
    parsed = dict(parse_qsl(init_data, keep_blank_values=True))
    
    received_hash = parsed.pop("hash", None)

    if not received_hash:
        raise HTTPException(status_code=401, detail="Нет hash в initData")

    data_check_string = "\n".join(
        f"{key}={value}" for key, value in sorted(parsed.items())
    )

    secret_key = hmac.new(
        b"WebAppData",
        TELEGRAM_TOKEN.encode(),
        hashlib.sha256,
    ).digest()

    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256,
    ).hexdigest()

    if calculated_hash != received_hash:
        raise HTTPException(status_code=401, detail="Неверная подпись initData")

    auth_date = int(parsed.get("auth_date", "0"))
    if auth_date and time.time() - auth_date > max_age_seconds:
        raise HTTPException(status_code=401, detail="initData устарела")

    return parsed


def get_telegram_user_id(init_data: str) -> int:
    """Из проверенной initData достаём telegram_id юзера."""
    logger.info(init_data)
    parsed = _validate_init_data(init_data)
    user_raw = parsed.get("user")

    if not user_raw:
        raise HTTPException(status_code=401, detail="Нет user в initData")

    user = json.loads(user_raw)
    user_id = user.get("id")
    

    if not user_id:
        raise HTTPException(status_code=401, detail="Нет id в user")

    return int(user_id)