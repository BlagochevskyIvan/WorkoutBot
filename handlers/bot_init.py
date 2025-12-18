from telegram.ext import (
    Application,
    CommandHandler,
)
from telegram.ext import (
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    PicklePersistence,
)
from config.cp_config import (
    TELEGRAM_TOKEN,
)
from config.logger import logger
from config.states import MAINMENU, GET_DATE, PROFILE
from handlers.common import start
from handlers.profile import get_date, get_gender, get_experience, get_place


def create_bot_app():
    persistence = PicklePersistence("bot_cache")
    application = (
        Application.builder()
        .token(TELEGRAM_TOKEN)
        .persistence(persistence)
        .build()
    )

    logger.info("Запуск тг бота")
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            # Работа основного приложения
            MAINMENU: [
                CallbackQueryHandler(start, pattern="^subscribe$"),
                CallbackQueryHandler(start, pattern="^info$"),
                CallbackQueryHandler(start, pattern="^menu$"),
                CallbackQueryHandler(start, pattern="^rfcard$"),
            ],
            PROFILE: [
                CallbackQueryHandler(get_gender, pattern="^(male|female)$"),
                CallbackQueryHandler(get_experience, pattern="^(beginner|intermediate|advanced)$"),
                CallbackQueryHandler(get_place, pattern="^(flat|gym)$"),
            ],
            # Получение даты рождения
            GET_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)]
        },
        fallbacks=[CommandHandler("start", start)],
        name="main_conversation",
    )

    application.add_handler(conv_handler)
    
    return application