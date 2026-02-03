from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from db.set_crud import get_sets, create_set
from libs.sub_func import validate_num
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
                [InlineKeyboardButton(text="Назад к упражнениям", callback_data="exercises")],
                [InlineKeyboardButton(text="Меню", callback_data="menu")]
            ]
        )
        await query.edit_message_text(
            text="В этом упржнении пока нет подходов\nВы можете добавить их",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return MENU
    
    num = 0
    for set in sets:
        num += 1
        keyboard.extend(
            [
                [InlineKeyboardButton(text=f"{num}. {set.weight}кг х {set.reps}", callback_data=f"set_{set.id}")]
            ]
        )

    keyboard.extend(
        [
            [InlineKeyboardButton(text="Добавить подход", callback_data="create_set")],
            [InlineKeyboardButton(text="Назад к упражнениям", callback_data="exercises")],
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
    weight = update.message.text
    if validate_num(weight):
        context.user_data["set_weight"] = weight
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Введите количество повторений подхода:",
        )
        return GET_SET_REPS
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Введите вес должен быть числом\nВведите вес подхода:",
        )
        return GET_SET_WEIGHT

async def create_set_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tg_user = update.effective_user
    reps = update.message.text
    if validate_num(reps):
        exercise_id = context.user_data.get("exercise_id")
        set_weight = context.user_data.get("set_weight")
        # set_reps = update.message.text
        set = await create_set(exercise_id=exercise_id, weight=set_weight, reps=reps)
        context.user_data["set_id"] = set.id
        keyboard = [
            [InlineKeyboardButton(text="Изменить Подход", callback_data="create_exercise")],
            [InlineKeyboardButton(text="Назад к подходам", callback_data="sets")],
            [InlineKeyboardButton(text="Меню", callback_data="menu")]
            ]
        await context.bot.send_message(
            chat_id=tg_user.id,
            text=f"подход успешно создан!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return MENU
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Повторения должены быть числом\nВведите количество повторений:",
        )
        return GET_SET_REPS