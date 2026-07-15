from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    ContextTypes,
)

from config.states import MENU, GET_DATE, PROFILE, GET_HEIGHT, GET_WEIGHT, GET_BODY_FAT_PERCENTAGE
from db.user_crud import add_gender, add_birth_date, add_expirience, add_place, add_params, get_last_params, get_user_crud
from libs.sub_func import get_true_date, pretty_float, validate_date, validate_num
from db.fact_workout_crud import get_count_workouts

async def get_gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    gender = query.data
    await add_gender(telegram_id=update.effective_user.id, gender=gender)
    context.user_data["gender"] = gender
    await query.edit_message_text(
        text="Пол установлен.\nТеперь введите ваш рост в сантиметрах:",
    )
    context.user_data["question_message_id"] = query.message.message_id
    return GET_HEIGHT

async def get_height(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.delete()
    height = update.message.text.replace(",", ".")

    if not validate_num(height) or float(height) == 0:
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=context.user_data["question_message_id"],
            text="Некорректный рост. Введите рост в сантиметрах, например 180:",
        )
        return GET_HEIGHT

    context.user_data["height"] = float(height)
    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=context.user_data["question_message_id"],
        text="Рост сохранён.\nТеперь введите ваш вес в килограммах:",
    )
    return GET_WEIGHT

async def get_weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.delete()
    weight = update.message.text.replace(",", ".")

    if not validate_num(weight) or float(weight) == 0:
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=context.user_data["question_message_id"],
            text="Некорректный вес. Введите вес в килограммах, например 75.5:",
        )
        return GET_WEIGHT

    context.user_data["weight"] = float(weight)
    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=context.user_data["question_message_id"],
        text="Вес сохранён.\nТеперь введите процент жира:",
    )
    return GET_BODY_FAT_PERCENTAGE

async def get_body_fat_percentage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.delete()
    body_fat_percentage = update.message.text.replace(",", ".")

    if not validate_num(body_fat_percentage) or float(body_fat_percentage) > 100:
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=context.user_data["question_message_id"],
            text="Некорректный процент жира. Введите число от 0 до 100:",
        )
        return GET_BODY_FAT_PERCENTAGE

    await add_params(
        telegram_id=update.effective_user.id,
        weight=context.user_data["weight"],
        height=context.user_data["height"],
        body_fat_percentage=float(body_fat_percentage),
    )
    keyboard = [[InlineKeyboardButton("Меню", callback_data="menu")]]
    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=context.user_data["question_message_id"],
        text="Параметры сохранены. Регистрация завершена!",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    context.user_data.clear()
    return MENU

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
    params = await get_last_params(telegram_id=user.telegram_id)
    gender = {"male": "Мужчина", "female": "Женщина"}.get(user.gender, "Не указан")
    height = f"{pretty_float(params.height)} см" if params and params.height is not None else "Не указан"
    weight = f"{pretty_float(params.weight)} кг" if params and params.weight is not None else "Не указан"
    body_fat_percentage = f"{pretty_float(params.body_fat_percentage)}%" if params and params.body_fat_percentage is not None else "Не указан"
    keyboard = [
        [InlineKeyboardButton("Редактировать профиль", callback_data="edit_profile")],
        [InlineKeyboardButton("В меню", callback_data="menu")]
    ]
    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=query.message.message_id,
        text=(
            f"{user_name}\n"
            f"Количество тренировок: {user_workouts}\n"
            f"Пол: {gender}\n"
            f"Рост: {height}\n"
            f"Вес: {weight}\n"
            f"Процент жира: {body_fat_percentage}"
        ),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return MENU
