from telegram.ext import (
    Application,
    CommandHandler,
)
from telegram.ext import (
    ConversationHandler,
    CallbackQueryHandler,
    PicklePersistence,
)
from config.cp_config import (
    TELEGRAM_TOKEN,
)
from config.logger import logger
from config.states import MAINMENU
from handlers.common import start


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
            MAINMENU: [
                CallbackQueryHandler(start, pattern="^subscribe$"),
                CallbackQueryHandler(start, pattern="^info$"),
                CallbackQueryHandler(start, pattern="^menu$"),
                CallbackQueryHandler(start, pattern="^rfcard$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
        name="main_conversation",
    )

    application.add_handler(conv_handler)
    
    return application