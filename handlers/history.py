from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config.states import MENU
from db.fact_workout_crud import get_fact_workouts


async def workout_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    fact_workouts = await get_fact_workouts(user_id=update.effective_user.id)
    keyboard = []

    for index, fact_workout in enumerate(fact_workouts):
        keyboard.append([
            InlineKeyboardButton(
                text=f"Тренировка {index + 1} | {fact_workout.created_at.strftime('%d/%m/%y')}",
                callback_data=f"fact_workout_{fact_workout.id}"
            )
        ])

    keyboard.append([InlineKeyboardButton(text="В меню", callback_data="menu")])

    text = "История тренировок"
    if not fact_workouts:
        text = "У вас пока нет завершённых тренировок"

    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return MENU
