from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from db.programs_crud import get_programs, create_program
from db.workout_crud import get_workouts
from db.exercise_crud import get_exercises, create_exercise
from config.states import MENU, GET_EXERCISE_NAME
from config.logger import logger

async def list_exercises(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if str(query.data) != "exercises":
        workout_id = int(query.data.split("_")[1])
        context.user_data["workout_id"] = workout_id
    workout_id = context.user_data["workout_id"]
    exercises = await get_exercises(workout_id)
    keyboard = []
    if not exercises:
        keyboard.extend(
            [
                [InlineKeyboardButton(text="Добавить упражнение", callback_data="create_exercise")],
                [InlineKeyboardButton(text="К тренировкам", callback_data="workouts")],
                [InlineKeyboardButton(text="Меню", callback_data="menu")]
            ]
        )
        await query.edit_message_text(
            text="В этой тренировке пока нет упражненеий",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return MENU

    keyboard.extend(
        [
            [InlineKeyboardButton(text=exercise.name, callback_data=f"exercise_{exercise.id}")]
            for exercise in exercises
        ]
    )
    keyboard.extend(
        [
            [InlineKeyboardButton(text="Добавить упражнение", callback_data="create_exercise")],
            [InlineKeyboardButton(text="К тренировкам", callback_data="workouts")],
            [InlineKeyboardButton(text="Меню", callback_data="menu")]
        ]
    )
    await query.edit_message_text(
        text="Тренировки в программе",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return MENU

async def get_exercise_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text="Введите название нового упражнения:",
    )
    return GET_EXERCISE_NAME

async def create_exercise_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tg_user = update.effective_user
    workout_id = context.user_data.get("workout_id")

    exercise_name = update.message.text
    exercise = await create_exercise(workout_id=workout_id, name=exercise_name)
    context.user_data["exercise_id"] = exercise.id
    keyboard = [
        [InlineKeyboardButton(text="Добавить Подход", callback_data="create_exercise")],
        [InlineKeyboardButton(text="К упражнениям", callback_data="exercises")],
        [InlineKeyboardButton(text="Меню", callback_data="menu")]
        ]
    await context.bot.send_message(
        chat_id=tg_user.id,
        text=f"Упражнение '{exercise_name}' успешно создано!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return MENU