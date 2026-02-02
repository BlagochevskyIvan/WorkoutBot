from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from db.programs_crud import get_programs, create_program
from db.workout_crud import get_workouts
from db.exercise_crud import get_exercises, create_exercise
from db.set_crud import get_sets, create_set
from config.states import MENU, GET_SET_WEIGHT, GET_SET_REPS
from config.logger import logger

async def list_sets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if str(query.data) != "sets":
        exercise_id = int(query.data.split("_")[1])
        context.user_data["exercise_id"] = exercise_id
    exercise_id = context.user_data["exercise_id"]
    sets = await get_sets(exercise_id)
    keyboard = []
    if not sets:
        keyboard.extend(
            [
                [InlineKeyboardButton(text="Добавить подход", callback_data="create_set")],
                [InlineKeyboardButton(text="К упражнениям", callback_data="exercises")],
                [InlineKeyboardButton(text="Меню", callback_data="menu")]
            ]
        )
        await query.edit_message_text(
            text="В этом упржнении пока нет подходов",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return MENU
    
    set_num = 0
    for set in sets:
        set_num += 1
        keyboard.extend(
            [
                [InlineKeyboardButton(text=f"{set_num}. {set.weight}кг х {set.reps}", callback_data=f"set_{set.id}")]
            ]
        )

    keyboard.extend(
        [
            [InlineKeyboardButton(text="Добавить подход", callback_data="create_set")],
            [InlineKeyboardButton(text="К упражнениям", callback_data="exercises")],
            [InlineKeyboardButton(text="Меню", callback_data="menu")]
        ]
    )
    await query.edit_message_text(
        text="Подходы в упражнении",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return MENU

async def get_set_weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text="Введите вес подхода:",
    )
    return GET_SET_WEIGHT

async def get_set_reps(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["set_weight"] = int(update.message.text)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Введите количество повторений подхода:",
    )
    return GET_SET_REPS

async def create_set_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tg_user = update.effective_user
    exercise_id = context.user_data.get("exercise_id")

    set_weight = context.user_data.get("set_weight")
    set_reps = int(update.message.text)
    set = await create_set(exercise_id=exercise_id, weight=set_weight, reps=set_reps)
    context.user_data["set_id"] = set.id
    keyboard = [
        [InlineKeyboardButton(text="Изменить Подход", callback_data="create_exercise")],
        [InlineKeyboardButton(text="К подходам", callback_data="sets")],
        [InlineKeyboardButton(text="Меню", callback_data="menu")]
        ]
    await context.bot.send_message(
        chat_id=tg_user.id,
        text=f"подход успешно создан!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return MENU