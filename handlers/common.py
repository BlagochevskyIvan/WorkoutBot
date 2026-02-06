from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)

from config.states import PROFILE, MENU
from db.user_crud import get_user, create_user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    context.chat_data.clear()

    tg_user = update.effective_user
    chat_id = update.effective_chat.id

    db_user = await get_user(telegram_id=tg_user.id)

    if not db_user:
        db_user = await create_user(tg_user.id, tg_user.username)
        keyboard = [[
            InlineKeyboardButton("Мужчина", callback_data='male'),
            InlineKeyboardButton("Женщина", callback_data='female')
        ]]
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Привет, {tg_user.first_name}! Добро пожаловать в бота.\n\nКто вы?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return PROFILE
    else:
        keyboard = [
            [InlineKeyboardButton("Программы тренировок", callback_data='programs')],
            [InlineKeyboardButton("Профиль", callback_data='profile')]
        ]
        await context.bot.send_message(
            chat_id=chat_id,
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
    keyboard = [[InlineKeyboardButton("Меню", callback_data='menu')]]
    await query.edit_message_text(
        text="Функция заглушка. Скоро здесь будет что-то полезное!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return MENU

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.delete()

    context.user_data.clear()
    return ConversationHandler.END