from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from db.programs_crud import get_programs, create_program
from config.states import MENU, GET_PROGRAMM_NAME

async def list_workout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    tg_user = update.effective_user
    programs = await get_programs(tg_user.id)
    keyboard = [
        [InlineKeyboardButton(text="Добавить тренировку", callback_data="create_workout")],
        [InlineKeyboardButton(text="")],
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