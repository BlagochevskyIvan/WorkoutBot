from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config.states import MENU
from db.fact_workout_crud import get_fact_workouts, get_fact_workout, get_fact_workouts_page, get_fact_workout_details
from db.fact_exercise_crud import get_fact_exercises
from db.fact_set_crud import get_fact_sets

HISTORY_PAGE_SIZE = 7
async def workout_history(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    await query.answer()

    page = 1

    if query.data.startswith("history_page_"):
        page = int(query.data.split("_")[-1])

    fact_workouts, total = await get_fact_workouts_page(
        telegram_id=update.effective_user.id,
        page=page,
        page_size=HISTORY_PAGE_SIZE
    )

    page_count = max(
        1,
        (total + HISTORY_PAGE_SIZE - 1) // HISTORY_PAGE_SIZE
    )

    # Защита от некорректной страницы
    page = max(1, min(page, page_count))

    keyboard = []

    start_index = (page - 1) * HISTORY_PAGE_SIZE + 1

    for index, fact_workout in enumerate(
        fact_workouts,
        start=start_index
    ):
        keyboard.append([
            InlineKeyboardButton(
                text=(
                    f"Тренировка {index} | "
                    f"{fact_workout.created_at.strftime('%d/%m/%y')}"
                ),
                callback_data=f"fact_workout_{fact_workout.id}"
            )
        ])

    page_keyboard = []

    if page > 1:
        page_keyboard.append(
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=f"history_page_{page - 1}"
            )
        )

    if page < page_count:
        page_keyboard.append(
            InlineKeyboardButton(
                text="Вперёд ➡️",
                callback_data=f"history_page_{page + 1}"
            )
        )

    if page_keyboard:
        keyboard.append(page_keyboard)

    keyboard.append([
        InlineKeyboardButton(
            text="В меню",
            callback_data="menu"
        )
    ])

    if total == 0:
        text = "У вас пока нет завершённых тренировок"
    else:
        text = (
            "История тренировок\n"
            f"Страница {page} из {page_count}"
        )

    context.user_data["history_page"] = page

    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return MENU

async def fact_workout_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    fact_workout_id = int(query.data.split("_")[-1])
    fact_workout = await get_fact_workout_details(fact_workout_id=fact_workout_id)
    text = f"Тренировка {fact_workout.created_at.strftime('%d/%m/%y')}\n{fact_workout.name}\n\n"
    for index, fact_exercise in enumerate(fact_workout.fact_exercises):
        text += f"{index + 1}. {fact_exercise.name}\n"
        sets = fact_exercise.fact_sets
        for set_index, fact_set in enumerate(sets):
            text += f"   Подход {set_index + 1}: {fact_set.weight} кг x {fact_set.reps}\n"

    history_page = context.user_data.get("history_page", 0)
    keyboard = [[InlineKeyboardButton("Меню", callback_data="menu")], [InlineKeyboardButton("Назад", callback_data=f"history_page_{history_page}")]]

    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return MENU
