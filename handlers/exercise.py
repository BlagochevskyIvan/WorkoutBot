from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from db.programs_crud import get_programs, create_program
from db.workout_crud import get_workouts
from db.exercise_crud import get_exercises
from config.states import MENU, GET_PROGRAMM_NAME

async def list_exercises(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    tg_user = update.effective_user
    exercises = await get_exercises(tg_user.id)
    keyboard = [
        [InlineKeyboardButton(text="Добавить упражнение", callback_data="create_workout")],
        [InlineKeyboardButton(text="К тренировкам", callback_data="menu")]
    ]
    if not exercises:
        await query.edit_message_text(
            text="В этой тренировке пока нет упражнений",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return MENU

    keyboard.extend(
        [
            [InlineKeyboardButton(text=exercise.name, callback_data=f"program_{exercise.id}")]
            for exercise in exercises
        ]
    )