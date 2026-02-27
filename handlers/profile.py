from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    ContextTypes,
)

from config.states import MENU, GET_DATE, PROFILE
from db.user_crud import add_gender, add_birth_date, add_expirience, add_place, get_user_crud
from libs.sub_func import get_true_date, validate_date
from db.fact_workout_crud import get_count_workouts

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
    message = await query.edit_message_text(
        text="Место тренировок установлено. \nТеперь введите вашу дату рождения в формате ДД.ММ.ГГГГ (например, 01.01.2001)",
    )
    context.user_data["question_mesage_id"] = message.message_id
    return GET_DATE

async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await context.bot.delete_messages(
        chat_id=update.effective_chat.id,
        message_ids=[update.effective_message.id],
    )
    tg_user = update.effective_user
    date_str = update.message.text

    if not validate_date(date_str):
        await context.bot.edit_message_text(
            chat_id=tg_user.id,
            message_id=context.user_data["question_mesage_id"],
            text="Некорректный формат даты. Пожалуйста, введите дату в формате ДД.ММ.ГГГГ (например, 01.01.2001).",
        )
        return GET_DATE
    await add_birth_date(telegram_id=tg_user.id, birth_date=get_true_date(date_str))
    context.user_data["birth_date"] = date_str
    keyboard = [[InlineKeyboardButton("Меню", callback_data='menu')]]
    await context.bot.edit_message_text(
        chat_id=tg_user.id,
        message_id=context.user_data["question_mesage_id"],
        text="Дата сохранена. Ваш профиль успешно создан!\nИспользуйте главное меню для навигации.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return MENU

async def get_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user = update.effective_user
    user_name = user.full_name
    user = await get_user_crud(telegram_id=user.id)
    user_workouts = await get_count_workouts(user_tg_id=user.telegram_id)
    keyboard = [
        [InlineKeyboardButton("Редактировать профиль", callback_data="edit_profile")],
        [InlineKeyboardButton("В меню", callback_data="menu")]
    ]
    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=query.message.message_id,
        text = f"{user_name}\nКоличество тренировок: {user_workouts}\nДата рождения: {user.birth_date.strftime('%d/%m/%y')}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return MENU