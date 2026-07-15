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
from server.routers.api_router import router as api_router
from handlers.bot_init import create_bot_app
from telegram.ext import Application
from sqlalchemy import text

from db.database import engine
from db.models import Base


POSITION_TABLES = (
    ("programs", "owner_id"),
    ("workouts", "program_id"),
    ("exercises", "workout_id"),
    ("sets", "exercise_id"),
)


async def init_position_columns(conn):
    for table_name, parent_column in POSITION_TABLES:
        await conn.execute(
            text(
                f"ALTER TABLE {table_name} "
                "ADD COLUMN IF NOT EXISTS position INTEGER NOT NULL DEFAULT 0"
            )
        )
        await conn.execute(
            text(
                f"""
                WITH parents_to_initialize AS (
                    SELECT {parent_column}
                    FROM {table_name}
                    GROUP BY {parent_column}
                    HAVING COUNT(*) > 1
                       AND MIN(position) = 0
                       AND MAX(position) = 0
                ),
                ranked AS (
                    SELECT id,
                           ROW_NUMBER() OVER (
                               PARTITION BY {parent_column}
                               ORDER BY id
                           ) - 1 AS new_position
                    FROM {table_name}
                    WHERE {parent_column} IN (
                        SELECT {parent_column} FROM parents_to_initialize
                    )
                )
                UPDATE {table_name}
                SET position = ranked.new_position
                FROM ranked
                WHERE {table_name}.id = ranked.id
                """
            )
        )


async def init_registration_columns(conn):
    await conn.execute(
        text(
            "ALTER TABLE users "
            "ADD COLUMN IF NOT EXISTS is_registered BOOLEAN NOT NULL DEFAULT FALSE"
        )
    )


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await init_registration_columns(conn)
        await init_position_columns(conn)
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
    try:
        await bot_app.bot.delete_webhook()
    finally:
        await bot_app.stop()
        await bot_app.shutdown()
        logger.info("Webhook deleted and bot stopped")

def init_fastapi_app():
    app = FastAPI(lifespan=lifespan)
    app.include_router(common_router)
    app.include_router(api_router, prefix='/api')
    return app



