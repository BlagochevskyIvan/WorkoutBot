from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from db.exercise_crud import get_exercises, create_exercise, delete_exercise_crud
from db.workout_crud import get_workout
from config.states import MENU, GET_EXERCISE_NAME


def exercise_button_row(exercise, index: int, total: int):
    row = [
        InlineKeyboardButton(
            text=f"{index + 1}. {exercise.name}",
            callback_data=f"exercise_{exercise.id}"
        )
    ]
    if index > 0:
        row.append(InlineKeyboardButton(text="↑", callback_data=f"move_exercise_{exercise.id}_up"))
    if index < total - 1:
        row.append(InlineKeyboardButton(text="↓", callback_data=f"move_exercise_{exercise.id}_down"))
    return row


async def list_exercises(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if str(query.data).startswith("workout_"):
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
                [InlineKeyboardButton(text="Удалить тренировку", callback_data="delete_workout")],
                [InlineKeyboardButton(text="Назад к тренировкам", callback_data="workouts")],
                [InlineKeyboardButton(text="Меню", callback_data="menu")]
            ]
        )
        await query.edit_message_text(
            text=f"{workout.name}\n\nВ этой тренировке пока пусто\nДобавьте упражнения",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return MENU

    keyboard.extend(
        exercise_button_row(exercise, index, len(exercises))
        for index, exercise in enumerate(exercises)
    )

    keyboard.extend(
        [
            [InlineKeyboardButton(text="Добавить упражнение", callback_data="create_exercise")],
            [InlineKeyboardButton(text="Начать тренировку", callback_data="start_workout")],
            [InlineKeyboardButton(text="Удалить тренировку", callback_data="delete_workout")],
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
        [InlineKeyboardButton(text="Удалить упражнение", callback_data="delete_exercise")],
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

async def delete_exercise(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    exercise_id = context.user_data["exercise_id"]
    await delete_exercise_crud(exercise_id=exercise_id)

    workout_id = context.user_data["workout_id"]
    workout = await get_workout(workout_id)
    exercises = await get_exercises(workout_id)
    keyboard = []
    if not exercises:
        keyboard.extend(
            [
                [InlineKeyboardButton(text="Добавить упражнение", callback_data="create_exercise")],
                [InlineKeyboardButton(text="Удалить тренировку", callback_data="delete_workout")],
                [InlineKeyboardButton(text="Назад к тренировкам", callback_data="workouts")],
                [InlineKeyboardButton(text="Меню", callback_data="menu")]
            ]
        )
        await query.edit_message_text(
            text=f"Упражнение удалено\n{workout.name}\n\nВ этой тренировке пока пусто\nДобавьте упражнения",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return MENU

    keyboard.extend(
        exercise_button_row(exercise, index, len(exercises))
        for index, exercise in enumerate(exercises)
    )

    keyboard.extend(
        [
            [InlineKeyboardButton(text="Добавить упражнение", callback_data="create_exercise")],
            [InlineKeyboardButton(text="Начать тренировку", callback_data="start_workout")],
            [InlineKeyboardButton(text="Удалить тренировку", callback_data="delete_workout")],
            [InlineKeyboardButton(text="Назад к тренировкам", callback_data="workouts")],
            [InlineKeyboardButton(text="Меню", callback_data="menu")]
        ]
    )
    await query.edit_message_text(
        text=f"Упражнение удалено\n{workout.name}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return MENU
