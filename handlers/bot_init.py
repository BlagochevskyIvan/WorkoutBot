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
from config.states import MENU, GET_DATE, PROFILE, GET_PROGRAMM_NAME, GET_WORKOUT_NAME, GET_EXERCISE_NAME
from handlers.common import start, menu, empty_func
from handlers.profile import get_date, get_gender, get_experience, get_place
from handlers.programs import list_programs, get_program_name, create_program_handler
from handlers.workout import list_workouts, get_workout_name, create_workout_handler
from handlers.exercise import list_exercises, get_exercise_name, create_exercise_handler


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
        per_message=False,
        states={
            MENU: [
                CallbackQueryHandler(menu, pattern="^menu$"),
                CallbackQueryHandler(empty_func, pattern="^profile$"),
                CallbackQueryHandler(list_programs, pattern="^programs$"),
                CallbackQueryHandler(get_program_name, pattern="^create_program$"),
                CallbackQueryHandler(list_workouts, pattern="^program_\d+$"),
                CallbackQueryHandler(list_workouts, pattern="^workouts$"),
                CallbackQueryHandler(get_workout_name, pattern="^create_workout$"),
                CallbackQueryHandler(list_exercises, pattern="^workout_\d+$"),
                CallbackQueryHandler(list_exercises, pattern="^exercises$"),
                CallbackQueryHandler(get_exercise_name, pattern="^create_exercise$"),
            ],
            PROFILE: [
                CallbackQueryHandler(get_gender, pattern="^(male|female)$"),
                CallbackQueryHandler(get_experience, pattern="^(beginner|intermediate|advanced)$"),
                CallbackQueryHandler(get_place, pattern="^(flat|gym)$"),
            ],
            GET_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)],
            GET_PROGRAMM_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_program_handler)],
            GET_WORKOUT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_workout_handler)],
            GET_EXERCISE_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_exercise_handler)]

        },
        fallbacks=[CommandHandler("start", start)],
        name="main_conversation",
    )

    application.add_handler(conv_handler)
    
    return application