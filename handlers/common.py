from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from telegram.ext import (
    ContextTypes,
)

from config.states import PROFILE

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    tg_user = update.effective_user
    # db_user = await get_user(telegram_id=tg_user.id)
    # if not db_user:
    # db_user = await create_user(tg_user.id, tg_user.username)
    await context.bot.send_message(
        chat_id=tg_user.id,
        text=f"Привет, {tg_user.first_name}! Добро пожаловать в бота для создания тренировок.\n\nДля начала работы необходимо создать профиль.",
        )
    keyboard = [[InlineKeyboardButton("Мужчина", callback_data='male'), InlineKeyboardButton("Женщина", callback_data='female')]]
    await context.bot.send_message(
        chat_id=tg_user.id,
        text="Кто вы?",
        reply_markup=InlineKeyboardMarkup(keyboard)
        # text="Введите свою дату рождения в формате 01.01.2001",
        )
    return PROFILE