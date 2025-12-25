from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    ContextTypes,
)

from config.states import MENU, GET_DATE, PROFILE
from db.user_crud import add_gender, add_birth_date, add_expirience, add_place

async def get_gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    gender = query.data
    await add_gender(telegram_id=update.effective_user.id, gender=gender)
    context.user_data["gender"] = gender
    keyboard = [[InlineKeyboardButton("Менее года", callback_data='beginner'),
                 InlineKeyboardButton("1-3 года", callback_data='intermediate')],
                [InlineKeyboardButton("Более 3 лет", callback_data='advanced')]]
    await query.edit_message_text(
        text="Пол установлен. \nТеперь укажите стаж тренировок",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return PROFILE

async def get_experience(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    experience = query.data
    await add_expirience(telegram_id=update.effective_user.id, experience=experience)
    context.user_data["experience"] = experience
    keyboard = [[InlineKeyboardButton("Квартира", callback_data='flat'),
                 InlineKeyboardButton("Тренажёрный зал", callback_data='gym')]]
    await query.edit_message_text(
        text="Стаж тренировок установлен. \nТеперь укажите, где планируете тренироваться",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return PROFILE

async def get_place(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    place = query.data
    await add_place(telegram_id=update.effective_user.id, place=place)
    context.user_data["place"] = place
    await query.edit_message_text(
        text="Место тренировок установлено. \nТеперь введите вашу дату рождения в формате ДД.ММ.ГГГГ (например, 01.01.2001)",
    )
    return GET_DATE

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
    await add_birth_date(telegram_id=tg_user.id, birth_date=date_str)
    context.user_data["birth_date"] = date_str
    await context.bot.send_message(
        chat_id=tg_user.id,
        text="Дата сохранена. Ваш профиль успешно создан!\nИспользуйте главное меню для навигации.",
        keyboard = [[InlineKeyboardButton("Меню", callback_data='menu')]]
    )
    return MENU