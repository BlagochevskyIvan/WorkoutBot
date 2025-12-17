from telegram import (
    Update,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes,
)

from db.user_crud import get_user, create_user
from config.states import MAINMENU, GET_DATE

async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    tg_user = update.effective_user
    date_str = update.message.text
    from libs.sub_func import validate_date

    if not validate_date(date_str):
        await context.bot.send_message(
            chat_id=tg_user.id,
            text="Некорректный формат даты. Пожалуйста, введите дату в формате ДД.ММ.ГГГГ (например, 01.01.2001).",
        )
        return GET_DATE

    await context.bot.send_message(
        chat_id=tg_user.id,
        text="Спасибо! Ваш профиль создан успешно.",
    )
    return MAINMENU

    # Возврат к основному меню
    from handlers.common import start
    return await start(update, context)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    tg_user = update.effective_user
    db_user = await get_user(telegram_id=tg_user.id)
    if not db_user:
        db_user = await create_user(tg_user.id, tg_user.username)
        await context.bot.send_message(
            chat_id=tg_user.id,
            text=f"Привет, {tg_user.first_name}! Добро пожаловать в бота для создания тренировок.\n\nДля начала работы необходимо создать профиль.",
            )
        await context.bot.send_message(
            chat_id=tg_user.id,
            text="Введите свою дату рождения в формате 01.01.2001",
            )
        return GET_DATE