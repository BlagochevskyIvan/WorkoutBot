from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)

from config.states import GET_GENDER, MENU
from db.user_crud import get_user_crud, create_user

from config.cp_config import WEBAPP_URL


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    context.chat_data.clear()

    tg_user = update.effective_user
    chat_id = update.effective_chat.id

    db_user = await get_user_crud(telegram_id=tg_user.id)

    if not db_user:
        db_user = await create_user(tg_user.id, tg_user.username)

    if not db_user.is_registered:
        keyboard = [
            [
                InlineKeyboardButton("Мужчина", callback_data="male"),
                InlineKeyboardButton("Женщина", callback_data="female"),
            ]
        ]
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Привет, {tg_user.first_name}! Для регистрации укажите ваш пол.",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        await context.bot.delete_message(
            chat_id=update.effective_chat.id, message_id=update.effective_message.id
        )
        return GET_GENDER

    keyboard = [
        [InlineKeyboardButton("Программы тренировок", callback_data="programs")],
        [InlineKeyboardButton("История тренировок", callback_data="history")],
        [InlineKeyboardButton("Профиль", callback_data="profile")],
        [InlineKeyboardButton(web_app=WebAppInfo(url=WEBAPP_URL+"/programs"), text="Веб-версия")],
    ]
    await context.bot.send_message(
        chat_id=chat_id,
        text="Вы уже зарегистрированы в боте. Используйте меню для навигации.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    await context.bot.delete_message(
        chat_id=update.effective_chat.id, message_id=update.effective_message.id
    )
    return MENU


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Программы тренировок", callback_data="programs")],
        [InlineKeyboardButton("История тренировок", callback_data="history")],
        [InlineKeyboardButton("Профиль", callback_data="profile")],
        [InlineKeyboardButton(web_app=WebAppInfo(url=WEBAPP_URL+"/programs"), text="Веб-версия")],
    ]
    await query.edit_message_text(
        text="Главное меню. Выберите действие.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return MENU


async def empty_func(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton("Меню", callback_data="menu")]]
    await query.edit_message_text(
        text="Функция заглушка. Скоро здесь будет что-то полезное!",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return MENU


async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.delete()

    context.user_data.clear()
    return ConversationHandler.END
