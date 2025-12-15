from contextlib import asynccontextmanager

from fastapi import FastAPI
from telegram import Update
from config.cp_config import (
    WEBHOOK_URL,
    WEBHOOK_PATH,
    DROP_PENDING,
    SECRET_TOKEN,
)
from config.logger import logger
from server.routers.common_router import router as common_router
from handlers.bot_init import create_bot_app
from telegram.ext import Application


from db.database import engine, Base


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
    logger.info('ВСЕ ТАБЛИЦЫ УСПЕШНО СОЗДАНЫ')

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    bot_app: Application = create_bot_app()
    app.state.bot_app = bot_app

    await bot_app.initialize()
    await bot_app.start()
    await bot_app.bot.set_webhook(
        url=WEBHOOK_URL + WEBHOOK_PATH,
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=DROP_PENDING,
        secret_token=SECRET_TOKEN,
    )
   
    logger.info("Webhook set: %s", WEBHOOK_URL)

    yield
    # Clean shutdown
    try:
        await bot_app.bot.delete_webhook()
    finally:
        await bot_app.stop()
        await bot_app.shutdown()
        logger.info("Webhook deleted and bot stopped")

def init_fastapi_app():
    app = FastAPI(lifespan=lifespan)
    app.include_router(common_router)
    # app.include_router(api_router)
    # app.include_router(payment_router)
    return app



