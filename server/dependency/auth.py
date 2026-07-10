from fastapi import Header, HTTPException

from server.auth.telegram import get_telegram_user_id


async def get_current_telegram_id(
    x_telegram_auth: str | None = Header(default=None, alias="X-Telegram-Auth"),
) -> int:
    if not x_telegram_auth:
        raise HTTPException(status_code=401, detail="Нет X-Telegram-Auth")

    return get_telegram_user_id(x_telegram_auth)