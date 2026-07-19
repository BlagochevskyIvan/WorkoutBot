from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config.states import MENU
from db.fact_workout_crud import get_fact_workouts, get_fact_workout
from db.fact_exercise_crud import get_fact_exercises
from db.fact_set_crud import get_fact_sets

async def workout_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    fact_workouts = await get_fact_workouts(user_id=update.effective_user.id)
    fact_workouts.reverse()
    keyboard = []

    for index, fact_workout in enumerate(fact_workouts):
        keyboard.append([
            InlineKeyboardButton(
                text=f"Тренировка {index + 1} | {fact_workout.created_at.strftime('%d/%m/%y')}",
                callback_data=f"fact_workout_{fact_workout.id}"
            )
        ])
    
    context.user_data["fact_workout_date"] = fact_workouts

    keyboard.append([InlineKeyboardButton(text="В меню", callback_data="menu")])

    text = "История тренировок"
    if not fact_workouts:
        text = "У вас пока нет завершённых тренировок"

    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return MENU

async def fact_workout_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    fact_workout_id = int(query.data.split("_")[-1])
    fact_exercises = await get_fact_exercises(fact_workout_id=fact_workout_id)
    fact_workout = await get_fact_workout(fact_workout_id=fact_workout_id)
    text = f"Тренировка {fact_workout.created_at.strftime('%d/%m/%y')}\n{fact_workout.name}\n\n"
    for index, fact_exercise in enumerate(fact_exercises):
        text += f"{index + 1}. {fact_exercise.name}\n"
        sets = await get_fact_sets(fact_exercise_id=fact_exercise.id)
        for set_index, fact_set in enumerate(sets):
            text += f"   Подход {set_index + 1}: {fact_set.weight} кг x {fact_set.reps}\n"

    keyboard = [[InlineKeyboardButton("Меню", callback_data="menu")], [InlineKeyboardButton("Назад", callback_data="history")]]

    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return MENU
