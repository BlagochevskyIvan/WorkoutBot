from fastapi import APIRouter

from fastapi import Request, Response, status
from fastapi.responses import PlainTextResponse, FileResponse
from telegram import Update
from config.cp_config import (
    TEMPLATE_PATH,
    WEBHOOK_PATH,
    SECRET_TOKEN,
)
from config.logger import logger

router = APIRouter()

@router.get("/")
async def root() -> Response:
    return PlainTextResponse("ok")


@router.get("/healthz")
async def health() -> Response:
    return PlainTextResponse("ok")


# Webhook endpoint
@router.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request) -> Response:
    # Optional: verify Telegram secret header
    
    if SECRET_TOKEN:
        header_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if header_token != SECRET_TOKEN:
            logger.warning("Forbidden: invalid secret token header")
            return Response(status_code=status.HTTP_403_FORBIDDEN)

    try:
        payload = await request.json()
    except Exception:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    update = Update.de_json(payload, request.app.state.bot_app.bot)
    # Hand off to PTB for processing
    await request.app.state.bot_app.update_queue.put(update)
    return Response(status_code=status.HTTP_200_OK)


@router.get("/app")
async def start_webapp(request: Request) -> Response:
    return FileResponse(path=str(TEMPLATE_PATH / "index.html"))