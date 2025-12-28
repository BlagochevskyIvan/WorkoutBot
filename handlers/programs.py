from telegram import Update
from telegram.ext import ContextTypes

async def list_programs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    tg_user = update.effective_user
    await query.edit_message_text(
        text="Здесь будут ваши программы тренировок. Эта функция в разработке!"
    )