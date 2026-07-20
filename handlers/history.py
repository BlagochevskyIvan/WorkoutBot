from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config.states import MENU
from db.fact_workout_crud import get_fact_workouts, get_fact_workout
from db.fact_exercise_crud import get_fact_exercises
from db.fact_set_crud import get_fact_sets

HISTORY_PAGE_SIZE = 7

async def workout_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    page = 0
    if query.data.startswith("history_page_"):
        page = int(query.data.split("_")[-1])

    fact_workouts = await get_fact_workouts(user_id=update.effective_user.id)
    fact_workouts.reverse()
    page_count = max(1, (len(fact_workouts) + HISTORY_PAGE_SIZE - 1) // HISTORY_PAGE_SIZE)
    page = min(page, page_count - 1)
    start_index = page * HISTORY_PAGE_SIZE
    page_workouts = fact_workouts[start_index:start_index + HISTORY_PAGE_SIZE]
    keyboard = []

    for index, fact_workout in enumerate(page_workouts, start=start_index + 1):
        keyboard.append([
            InlineKeyboardButton(
                text=f"Тренировка {index} | {fact_workout.created_at.strftime('%d/%m/%y')}",
                callback_data=f"fact_workout_{fact_workout.id}"
            )
        ])

    context.user_data["fact_workout_date"] = fact_workouts
    context.user_data["history_page"] = page

    page_keyboard = []
    if page > 0:
        page_keyboard.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"history_page_{page - 1}"))
    if page < page_count - 1:
        page_keyboard.append(InlineKeyboardButton(text="Вперёд ➡️", callback_data=f"history_page_{page + 1}"))
    if page_keyboard:
        keyboard.append(page_keyboard)

    keyboard.append([InlineKeyboardButton(text="В меню", callback_data="menu")])

    text = f"История тренировок\nСтраница {page + 1} из {page_count}"
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

    history_page = context.user_data.get("history_page", 0)
    keyboard = [[InlineKeyboardButton("Меню", callback_data="menu")], [InlineKeyboardButton("Назад", callback_data=f"history_page_{history_page}")]]

    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return MENU
