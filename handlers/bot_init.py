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
from config.states import MENU, GET_DATE, PROFILE, GET_PROGRAMM_NAME, GET_WORKOUT_NAME, GET_EXERCISE_NAME, GET_SET_WEIGHT, GET_SET_REPS, GET_FACT_REPS, EDIT_SET_WEIGHT, EDIT_SET_REPS
from handlers.common import start, menu, empty_func
from handlers.profile import get_date, get_gender, get_experience, get_place
from handlers.programs import list_programs, get_program_name, create_program_handler, delete_program
from handlers.workout import list_workouts, get_workout_name, create_workout_handler, delete_workout
from handlers.exercise import list_exercises, get_exercise_name, create_exercise_handler, delete_exercise
from handlers.set import list_sets, get_set_weight, get_set_reps, create_set_handler, get_set_info, delete_set, edit_set_weight, edit_set_reps, edit_set_handler
from handlers.workout_way import start_workout, workout_way


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
                CallbackQueryHandler(list_sets, pattern="^exercise_\d+$"),
                CallbackQueryHandler(list_sets, pattern="^sets$"),
                CallbackQueryHandler(get_set_weight, pattern="^create_set$"),
                CallbackQueryHandler(get_set_info, pattern="^\d+set_\d+$"),
                CallbackQueryHandler(start_workout, pattern="^start_workout$"),
                CallbackQueryHandler(delete_set, pattern="^delete_set$"),
                CallbackQueryHandler(delete_exercise, pattern="^delete_exercise$"),
                CallbackQueryHandler(delete_workout, pattern="^delete_workout$"),
                CallbackQueryHandler(delete_program, pattern="^delete_program$"),
                CallbackQueryHandler(edit_set_weight, pattern="^edit_set$")
            ],
            PROFILE: [
                CallbackQueryHandler(get_gender, pattern="^(male|female)$"),
                CallbackQueryHandler(get_experience, pattern="^(beginner|intermediate|advanced)$"),
                CallbackQueryHandler(get_place, pattern="^(flat|gym)$"),
            ],
            GET_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)],
            GET_PROGRAMM_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_program_handler)],
            GET_WORKOUT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_workout_handler)],
            GET_EXERCISE_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_exercise_handler)],
            GET_SET_WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_set_reps)],
            GET_SET_REPS: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_set_handler)],
            GET_FACT_REPS: [MessageHandler(filters.TEXT & ~filters.COMMAND, workout_way)],
            EDIT_SET_WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_set_reps)],
            EDIT_SET_REPS: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_set_handler)]
        },
        fallbacks=[CommandHandler("start", start)],
        name="main_conversation",
    )

    application.add_handler(conv_handler)
    
    return application