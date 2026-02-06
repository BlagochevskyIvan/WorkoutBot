from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from db.exercise_crud import get_exercises, create_exercise
from db.workout_crud import get_workout
from config.states import MENU, GET_EXERCISE_NAME

async def list_exercises(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if str(query.data) != "exercises":
        workout_id = int(query.data.split("_")[1])
        context.user_data["workout_id"] = workout_id
    workout_id = context.user_data["workout_id"]
    workout = await get_workout(workout_id)
    exercises = await get_exercises(workout_id)
    keyboard = []
    if not exercises:
        keyboard.extend(
            [
                [InlineKeyboardButton(text="Добавить упражнение", callback_data="create_exercise")],
                [InlineKeyboardButton(text="Назад к тренировкам", callback_data="workouts")],
                [InlineKeyboardButton(text="Меню", callback_data="menu")]
            ]
        )
        await query.edit_message_text(
            text=f"{workout.name}\n\nВ этой тренировке пока пусто\nДобавьте упражнения",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return MENU

    num = 0
    for exercise in exercises:
        num += 1
        keyboard.extend(
            [
                [InlineKeyboardButton(text=f"{num}. {exercise.name}", callback_data=f"exercise_{exercise.id}")]
            ]
        )

    keyboard.extend(
        [
            [InlineKeyboardButton(text="Добавить упражнение", callback_data="create_exercise")],
            [InlineKeyboardButton(text="Назад к тренировкам", callback_data="workouts")],
            [InlineKeyboardButton(text="Меню", callback_data="menu")]
        ]
    )
    await query.edit_message_text(
        text=f"{workout.name}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return MENU

async def get_exercise_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    message = await query.edit_message_text(
        text="Введите название нового упражнения:",
    )
    context.user_data["question_message_id"] = message.message_id
    return GET_EXERCISE_NAME

async def create_exercise_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.delete_messages(
        chat_id=update.effective_chat.id,
        message_ids=[update.effective_message.id],
    )
    tg_user = update.effective_user
    workout_id = context.user_data.get("workout_id")

    exercise_name = update.message.text
    exercise = await create_exercise(workout_id=workout_id, name=exercise_name)
    context.user_data["exercise_id"] = exercise.id
    keyboard = [
        [InlineKeyboardButton(text="Добавить подход", callback_data="create_set")],
        [InlineKeyboardButton(text="Назад к упражнениям", callback_data="exercises")],
        [InlineKeyboardButton(text="Меню", callback_data="menu")]
        ]
    await context.bot.edit_message_text(
        chat_id=tg_user.id,
        message_id=context.user_data["question_message_id"],
        text=f"Упражнение '{exercise_name}' успешно создано!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return MENU