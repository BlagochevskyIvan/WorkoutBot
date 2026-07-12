from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from db.workout_crud import get_workouts, create_workout, delete_workout_crud
from db.programs_crud import get_program
from config.states import MENU, GET_WORKOUT_NAME


def workout_button_row(workout, index: int, total: int):
    row = [InlineKeyboardButton(text=workout.name, callback_data=f"workout_{workout.id}")]
    if index > 0:
        row.append(InlineKeyboardButton(text="↑", callback_data=f"move_workout_{workout.id}_up"))
    if index < total - 1:
        row.append(InlineKeyboardButton(text="↓", callback_data=f"move_workout_{workout.id}_down"))
    return row


async def list_workouts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if str(query.data).startswith("program_"):
        program_id = int(query.data.split("_")[1])
        context.user_data["program_id"] = program_id
    program_id = context.user_data["program_id"]
    program = await get_program(program_id)
    workouts = await get_workouts(program_id)
    keyboard = []
    if not workouts:
        keyboard.extend(
            [
                [InlineKeyboardButton(text="Добавить тренировку", callback_data="create_workout")],
                [InlineKeyboardButton(text="Удалить программу", callback_data="delete_program")],
                [InlineKeyboardButton(text="Назад к программам", callback_data="programs")],
                [InlineKeyboardButton(text="Меню", callback_data="menu")]
            ]
        )
        await query.edit_message_text(
            text=f"{program.name}\n\nВ этой программе пока пусто\nВы можете добавить тренировки",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return MENU

    keyboard.extend(
        [
            workout_button_row(workout, index, len(workouts))
            for index, workout in enumerate(workouts)
        ]
    )
    keyboard.extend(
        [
            [InlineKeyboardButton(text="Добавить тренировку", callback_data="create_workout")],
            [InlineKeyboardButton(text="Удалить программу", callback_data="delete_program")],
            [InlineKeyboardButton(text="Назад к программам", callback_data="programs")],
            [InlineKeyboardButton(text="Меню", callback_data="menu")]
        ]
    )
    await query.edit_message_text(
        text=f"{program.name}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return MENU

async def get_workout_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    message = await query.edit_message_text(
        text="Введите название новой тренировки:",
    )
    context.user_data["question_message_id"] = message.message_id
    return GET_WORKOUT_NAME

async def create_workout_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.delete_messages(
        chat_id=update.effective_chat.id,
        message_ids=[update.effective_message.id],
    )
    tg_user = update.effective_user
    program_id = context.user_data.get("program_id")
    workout_name = update.message.text
    workout = await create_workout(program_id=program_id, name=workout_name)
    context.user_data["workout_id"] = workout.id
    keyboard = [
        [InlineKeyboardButton(text="Добавить упражнение", callback_data="create_exercise")],
        [InlineKeyboardButton(text="Удалить тренировку", callback_data="delete_workout")],
        [InlineKeyboardButton(text="Назад к тренировкам", callback_data="workouts")],
        [InlineKeyboardButton(text="Меню", callback_data="menu")]
        ]
    await context.bot.edit_message_text(
        chat_id=tg_user.id,
        message_id=context.user_data["question_message_id"],
        text=f"Тренировка '{workout_name}' успешно создана!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return MENU

async def delete_workout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    workout_id = context.user_data["workout_id"]
    await delete_workout_crud(workout_id=workout_id)

    program_id = context.user_data["program_id"]
    program = await get_program(program_id)
    workouts = await get_workouts(program_id)
    keyboard = []
    if not workouts:
        keyboard.extend(
            [
                [InlineKeyboardButton(text="Добавить тренировку", callback_data="create_workout")],
                [InlineKeyboardButton(text="Удалить программу", callback_data="delete_program")],
                [InlineKeyboardButton(text="Назад к программам", callback_data="programs")],
                [InlineKeyboardButton(text="Меню", callback_data="menu")]
            ]
        )
        await query.edit_message_text(
            text=f"{program.name}\n\nВ этой программе пока пусто\nДобавьте тренировки",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return MENU

    keyboard.extend(
        [
            workout_button_row(workout, index, len(workouts))
            for index, workout in enumerate(workouts)
        ]
    )
    keyboard.extend(
        [
            [InlineKeyboardButton(text="Добавить тренировку", callback_data="create_workout")],
            [InlineKeyboardButton(text="Удалить программу", callback_data="delete_program")],
            [InlineKeyboardButton(text="Назад к программам", callback_data="programs")],
            [InlineKeyboardButton(text="Меню", callback_data="menu")]
        ]
    )
    await query.edit_message_text(
        text=f"{program.name}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return MENU
