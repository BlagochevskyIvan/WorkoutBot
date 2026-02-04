from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from db.workout_crud import get_workouts, create_workout
from db.programs_crud import get_program
from config.states import MENU, GET_WORKOUT_NAME
from config.logger import logger

async def list_workouts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if str(query.data) != "workouts":
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
            [InlineKeyboardButton(text=workout.name, callback_data=f"workout_{workout.id}")]
            for workout in workouts
        ]
    )
    keyboard.extend(
        [
            [InlineKeyboardButton(text="Добавить тренировку", callback_data="create_workout")],
            [InlineKeyboardButton(text="Назад к программам", callback_data="programs")]
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
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text="Введите название новой тренировки:",
    )
    return GET_WORKOUT_NAME

async def create_workout_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tg_user = update.effective_user
    program_id = context.user_data.get("program_id")
    workout_name = update.message.text
    workout = await create_workout(program_id=program_id, name=workout_name)
    context.user_data["workout_id"] = workout.id
    keyboard = [
        [InlineKeyboardButton(text="Добавить упражнение", callback_data="create_exercise")],
        [InlineKeyboardButton(text="Назад к тренировкам", callback_data="workouts")],
        [InlineKeyboardButton(text="Меню", callback_data="menu")]
        ]
    await context.bot.send_message(
        chat_id=tg_user.id,
        text=f"Тренировка '{workout_name}' успешно создана!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return MENU