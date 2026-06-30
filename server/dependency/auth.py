from fastapi import Header, HTTPException

from server.auth.telegram import get_telegram_user_id


async def get_current_telegram_id(
    authorization: str | None = Header(default=None),
) -> int:
    """
    Клиент шлёт заголовок:
    Authorization: <сырая initData строка от Telegram>
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Нет Authorization")

    return get_telegram_user_id(authorization)