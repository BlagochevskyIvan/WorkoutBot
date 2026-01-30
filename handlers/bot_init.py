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
from config.states import MENU, GET_DATE, PROFILE, GET_PROGRAMM_NAME, PROGRAMM
from handlers.common import start, menu, empty_func
from handlers.profile import get_date, get_gender, get_experience, get_place
from handlers.programs import list_programs, get_program_name, create_program_handler


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
            MENU: [
                CallbackQueryHandler(menu, pattern="^menu$"),
                CallbackQueryHandler(list_programs, pattern="^programs$"),
                CallbackQueryHandler(empty_func, pattern="^profile$"),
                CallbackQueryHandler(get_program_name, pattern="^create_program$"),
            ],
            PROFILE: [
                CallbackQueryHandler(get_gender, pattern="^(male|female)$"),
                CallbackQueryHandler(get_experience, pattern="^(beginner|intermediate|advanced)$"),
                CallbackQueryHandler(get_place, pattern="^(flat|gym)$"),
            ],
            PROGRAMM: [
                CallbackQueryHandler(list_programs, pattern="^programs$"),
            ],
            # Получение даты рождения
            GET_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)],
            GET_PROGRAMM_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_program_handler)],

        },
        fallbacks=[CommandHandler("start", start)],
        name="main_conversation",
    )

    application.add_handler(conv_handler)
    
    return application