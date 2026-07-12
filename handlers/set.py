from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from db.set_crud import get_sets, create_set, get_set, delete_set_crud, edit_set
from db.exercise_crud import get_exercise
from libs.sub_func import validate_num, pretty_float
from config.states import MENU, GET_SET_WEIGHT, GET_SET_REPS, EDIT_SET_WEIGHT, EDIT_SET_REPS
from re import match


def set_button_row(set_obj, index: int, total: int):
    row = [
        InlineKeyboardButton(
            text=f"{index + 1}. {pretty_float(set_obj.weight)}кг х {set_obj.reps}",
            callback_data=f"{index + 1}set_{set_obj.id}"
        )
    ]
    if index > 0:
        row.append(InlineKeyboardButton(text="↑", callback_data=f"move_set_{set_obj.id}_up"))
    if index < total - 1:
        row.append(InlineKeyboardButton(text="↓", callback_data=f"move_set_{set_obj.id}_down"))
    return row


async def list_sets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if str(query.data).startswith("exercise_"):
        exercise_id = int(query.data.split("_")[1])
        context.user_data["exercise_id"] = exercise_id
    exercise_id = context.user_data["exercise_id"]
    exercise = await get_exercise(exercise_id)
    sets = await get_sets(exercise_id)
    keyboard = []
    if not sets:
        keyboard.extend(
            [
                [InlineKeyboardButton(text="Добавить подход", callback_data="create_set")],
                [InlineKeyboardButton(text="Удалить упражнение", callback_data="delete_exercise")],
                [InlineKeyboardButton(text="Назад к упражнениям", callback_data="exercises")],
                [InlineKeyboardButton(text="Меню", callback_data="menu")],
            ]
        )
        await query.edit_message_text(
            text=f"{exercise.name}\n\nВ этом упржнении пока нет подходов\nВы можете добавить их",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return MENU

    keyboard.extend(
        set_button_row(set_obj, index, len(sets))
        for index, set_obj in enumerate(sets)
    )

    keyboard.extend(
        [
            [InlineKeyboardButton(text="Добавить подход", callback_data="create_set")],
            [InlineKeyboardButton(text="Удалить упражнение", callback_data="delete_exercise")],
            [InlineKeyboardButton(text="Назад к упражнениям", callback_data="exercises")],
            [InlineKeyboardButton(text="Меню", callback_data="menu")],
        ]
    )
    await query.edit_message_text(
        text=f"{exercise.name}", reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return MENU


async def get_set_weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    message = await query.edit_message_text(
        text="Введите вес подхода:",
    )
    context.user_data["question_message_id"] = message.message_id
    return GET_SET_WEIGHT


async def get_set_reps(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await context.bot.delete_messages(
        chat_id=update.effective_chat.id,
        message_ids=[update.effective_message.id],
    )
    weight = update.message.text.replace(",", ".")
    if validate_num(weight):
        context.user_data["set_weight"] = weight
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=context.user_data["question_message_id"],
            text="Введите количество повторений подхода:",
        )
        return GET_SET_REPS
    else:
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=context.user_data["question_message_id"],
            text="Введите вес должен быть числом\nВведите вес подхода:",
        )
        return GET_SET_WEIGHT


async def create_set_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.delete_messages(
        chat_id=update.effective_chat.id,
        message_ids=[update.effective_message.id],
    )
    tg_user = update.effective_user
    reps = update.message.text.replace(",", ".")
    if validate_num(reps):
        exercise_id = int(context.user_data.get("exercise_id"))
        set_weight = float(context.user_data.get("set_weight"))
        await create_set(exercise_id=exercise_id, weight=set_weight, reps=int(reps))

        exercise = await get_exercise(exercise_id)
        sets = await get_sets(exercise_id)
        keyboard = []
        keyboard.extend(
            set_button_row(set_obj, index, len(sets))
            for index, set_obj in enumerate(sets)
        )

        keyboard.extend(
            [
                [InlineKeyboardButton(text="Добавить подход", callback_data="create_set")],
                [InlineKeyboardButton(text="Удалить упражнение", callback_data="delete_exercise")],
                [InlineKeyboardButton(text="Назад к упражнениям", callback_data="exercises")],
                [InlineKeyboardButton(text="Меню", callback_data="menu")],
            ]
        )

        await context.bot.edit_message_text(
            chat_id=tg_user.id,
            message_id=context.user_data["question_message_id"],
            text=f"подход успешно создан!\n\n{exercise.name}",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return MENU
    
    else:
        await context.bot.edit_message_text(
            chat_id=tg_user.id,
            message_id=context.user_data["question_message_id"],
            text="Повторения должены быть числом\nВведите количество повторений:",
        )
        return GET_SET_REPS


async def get_set_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    num = match(r"\d+", query.data).group()
    set_id = int(query.data.split("_")[1])
    context.user_data["set_id"] = set_id
    set = await get_set(set_id)
    keyboard = [
        [InlineKeyboardButton(text="Редактировать подход", callback_data="edit_set")],
        [InlineKeyboardButton(text="Удалить подход", callback_data="delete_set")],
        [InlineKeyboardButton(text="Назад к упражнению", callback_data="sets")],
        [InlineKeyboardButton(text="Меню", callback_data="menu")],
    ]
    await query.edit_message_text(
        text=f"Подход {num}\nвес {pretty_float(set.weight)} кг\n{set.reps} повторений",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return MENU

async def delete_set(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    set_id = context.user_data["set_id"]
    await delete_set_crud(set_id=set_id)

    exercise_id = context.user_data["exercise_id"]
    exercise = await get_exercise(exercise_id)
    sets = await get_sets(exercise_id)
    keyboard = []
    if not sets:
        keyboard.extend(
            [
                [InlineKeyboardButton(text="Добавить подход", callback_data="create_set")],
                [InlineKeyboardButton(text="Удалить упражнение", callback_data="delete_exercise")],
                [InlineKeyboardButton(text="Назад к упражнениям", callback_data="exercises")],
                [InlineKeyboardButton(text="Меню", callback_data="menu")],
            ]
        )
        await query.edit_message_text(
            text=f"{exercise.name}\n\nВ этом упржнении пока нет подходов\nВы можете добавить их",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return MENU

    keyboard.extend(
        set_button_row(set_obj, index, len(sets))
        for index, set_obj in enumerate(sets)
    )

    keyboard.extend(
        [
            [InlineKeyboardButton(text="Добавить подход", callback_data="create_set")],
            [InlineKeyboardButton(text="Удалить упражнение", callback_data="delete_exercise")],
            [InlineKeyboardButton(text="Назад к упражнениям", callback_data="exercises")],
            [InlineKeyboardButton(text="Меню", callback_data="menu")],
        ]
    )
    await query.edit_message_text(
        text=f"{exercise.name}", reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return MENU

async def edit_set_weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    message = await query.edit_message_text(
        text="Введите вес подхода:",
    )
    context.user_data["question_message_id"] = message.message_id
    return EDIT_SET_WEIGHT

async def edit_set_reps(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await context.bot.delete_messages(
        chat_id=update.effective_chat.id,
        message_ids=[update.effective_message.id],
    )
    weight = update.message.text.replace(",", ".")
    if validate_num(weight):
        context.user_data["set_weight"] = weight
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=context.user_data["question_message_id"],
            text="Введите количество повторений подхода:",
        )
        return EDIT_SET_REPS
    else:
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=context.user_data["question_message_id"],
            text="Введите вес должен быть числом\nВведите вес подхода:",
        )
        return EDIT_SET_WEIGHT
       
async def edit_set_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.delete_messages(
        chat_id=update.effective_chat.id,
        message_ids=[update.effective_message.id],
    )
    tg_user = update.effective_user
    reps = update.message.text.replace(",", ".")
    if validate_num(reps):
        set_id = int(context.user_data.get("set_id"))
        set_weight = float(context.user_data.get("set_weight"))
        await edit_set(set_id=set_id, weight=set_weight, reps=int(reps))
        exercise_id = int(context.user_data.get("exercise_id"))
        exercise = await get_exercise(exercise_id)
        sets = await get_sets(exercise_id)
        keyboard = []
        keyboard.extend(
            set_button_row(set_obj, index, len(sets))
            for index, set_obj in enumerate(sets)
        )

        keyboard.extend(
            [
                [InlineKeyboardButton(text="Добавить подход", callback_data="create_set")],
                [InlineKeyboardButton(text="Удалить упражнение", callback_data="delete_exercise")],
                [InlineKeyboardButton(text="Назад к упражнениям", callback_data="exercises")],
                [InlineKeyboardButton(text="Меню", callback_data="menu")],
            ]
        )

        await context.bot.edit_message_text(
            chat_id=tg_user.id,
            message_id=context.user_data["question_message_id"],
            text=f"подход успешно изменён!\n\n{exercise.name}",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return MENU
    
    else:
        await context.bot.edit_message_text(
            chat_id=tg_user.id,
            message_id=context.user_data["question_message_id"],
            text="Повторения должены быть числом\nВведите количество повторений:",
        )
        return EDIT_SET_REPS
