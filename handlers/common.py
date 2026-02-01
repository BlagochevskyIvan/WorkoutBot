from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from telegram.ext import (
    ContextTypes,
)

from config.states import PROFILE, MENU
from db.user_crud import get_user, create_user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    tg_user = update.effective_user
    db_user = await get_user(telegram_id=tg_user.id)
    if not db_user:
        db_user = await create_user(tg_user.id, tg_user.username)
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
    else:
        keyboard = [[InlineKeyboardButton("Программы тренировок", callback_data='programs')], [InlineKeyboardButton("Профиль", callback_data='profile')]]
        await context.bot.send_message(
            chat_id=tg_user.id,
            text="Вы уже зарегистрированы в боте. Используйте меню для навигации.",
            reply_markup=InlineKeyboardMarkup(keyboard)
            )
        return MENU

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    tg_user = update.effective_user
    keyboard = [[InlineKeyboardButton("Программы тренировок", callback_data='programs')], [InlineKeyboardButton("Профиль", callback_data='profile')]]
    await query.edit_message_text(
        text="Главное меню. Выберите действие.",
        reply_markup=InlineKeyboardMarkup(keyboard)
        )
    return MENU
    
async def empty_func(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    tg_user = update.effective_user
    keyboard = [[InlineKeyboardButton("Меню", callback_data='menu')]]
    await query.edit_message_text(
        text="Функция заглушка. Скоро здесь будет что-то полезное!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return MENU