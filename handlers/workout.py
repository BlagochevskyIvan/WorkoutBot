from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from db.programs_crud import get_programs, create_program
from db.workout_crud import get_workouts
from config.states import MENU, GET_PROGRAMM_NAME

async def list_workout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    tg_user = update.effective_user
    workouts = await get_workouts(tg_user.id)
    keyboard = [
        [InlineKeyboardButton(text="Добавить тренировку", callback_data="create_workout")],
        [InlineKeyboardButton(text="К программам", callback_data="menu")]
    ]
    if not workouts:
        await query.edit_message_text(
            text="В этой программе пока нет тренировок",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return MENU

    keyboard.extend(
        [
            [InlineKeyboardButton(text=workout.name, callback_data=f"program_{workout.id}")]
            for workout in workouts
        ]
    )