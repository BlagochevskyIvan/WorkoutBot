from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from db.programs_crud import get_programs, create_program
from config.states import MENU, GET_PROGRAMM_NAME

async def list_programs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    tg_user = update.effective_user
    programs = await get_programs(tg_user.id)
    keyboard = [
        [InlineKeyboardButton(text="Создать программу", callback_data="create_program")],
        [InlineKeyboardButton(text="Меню", callback_data="menu")]
    ]
    if not programs:
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
    await create_program(telegram_id=tg_user.id, name=program_name)
    await context.bot.send_message(
        chat_id=tg_user.id,
        text=f"Программа '{program_name}' успешно создана!",
    )
    return 
