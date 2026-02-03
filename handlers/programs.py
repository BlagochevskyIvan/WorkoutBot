from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from db.programs_crud import get_programs, create_program
from config.states import MENU, GET_PROGRAMM_NAME
from config.logger import logger

async def list_programs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    tg_user = update.effective_user
    keyboard = [
        [InlineKeyboardButton(text="Создать программу", callback_data="create_program")],
    ]
    programs = await get_programs(tg_user.id)
    
    if not programs:
        keyboard.extend(
            [
                [InlineKeyboardButton(text="Меню", callback_data="menu")]
            ]
        )
        await query.edit_message_text(
            text="У вас пока нет программ тренировок.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return MENU

    keyboard.extend(
        [
            [InlineKeyboardButton(text=program.name, callback_data=f"program_{program.id}")]
            for program in programs
        ]
    )
    

    keyboard.extend(
        [
            [InlineKeyboardButton(text="Меню", callback_data="menu")]
        ]
    )

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text="Ваши программы тренировок:",
        reply_markup=reply_markup
    )
    return MENU

async def get_program_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text="Введите название новой программы тренировок:",
    )
    return GET_PROGRAMM_NAME

async def create_program_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    tg_user = update.effective_user
    program_name = update.message.text
    program = await create_program(telegram_id=tg_user.id, name=program_name)
    context.user_data["program_id"] = program.id
    keyboard = [
        [InlineKeyboardButton(text="Добавить тренировку", callback_data="create_workout")],
        [InlineKeyboardButton(text="К программам", callback_data="programs")],
        [InlineKeyboardButton(text="Меню", callback_data="menu")]
        ]
    await context.bot.send_message(
        chat_id=tg_user.id,
        text=f"Программа '{program_name}' успешно создана!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return MENU

# async def open_program(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     query = update.callback_query
#     await query.answer()

#     program_id = int(query.data.split("_")[1])
#     context.user_data["program_id"] = program_id
#     keyboard = [
#         [InlineKeyboardButton(text="Добавить тренировку", callback_data="create_workout")],
#         [InlineKeyboardButton(text="К программам", callback_data="programs")],
#         [InlineKeyboardButton(text="Меню", callback_data="menu")]
#         ]

#     return MENU

