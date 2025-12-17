from telegram import (
    Update,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes,
)

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