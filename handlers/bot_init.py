from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    PicklePersistence,
    filters,
)

from config.cp_config import (
    TELEGRAM_TOKEN,
)
from config.logger import logger
from config.states import (
    EDIT_SET_REPS,
    EDIT_SET_WEIGHT,
    GET_BODY_FAT_PERCENTAGE,
    GET_DATE,
    GET_EXERCISE_NAME,
    GET_FACT_REPS,
    GET_GENDER,
    GET_HEIGHT,
    GET_PROGRAMM_NAME,
    GET_SET_REPS,
    GET_SET_WEIGHT,
    GET_WEIGHT,
    GET_WORKOUT_NAME,
    MENU,
    PROFILE,
)
from handlers.common import menu, start
from handlers.exercise import (
    create_exercise_handler,
    delete_exercise,
    get_exercise_name,
    list_exercises,
)
from handlers.history import fact_workout_details, workout_history
from handlers.order import move_exercise, move_program, move_set, move_workout
from handlers.profile import (
    get_body_fat_percentage,
    get_date,
    get_experience,
    get_gender,
    get_height,
    get_place,
    get_user,
    get_weight,
)
from handlers.programs import (
    create_program_handler,
    delete_program,
    get_program_name,
    list_programs,
)
from handlers.set import (
    create_set_handler,
    delete_set,
    edit_set_handler,
    edit_set_reps,
    edit_set_weight,
    get_set_info,
    get_set_reps,
    get_set_weight,
    list_sets,
)
from handlers.workout import (
    create_workout_handler,
    delete_workout,
    get_workout_name,
    list_workouts,
)
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
                CallbackQueryHandler(get_user, pattern="^profile$"),
                CallbackQueryHandler(list_programs, pattern="^programs$"),
                CallbackQueryHandler(get_program_name, pattern="^create_program$"),
                CallbackQueryHandler(list_workouts, pattern=r"^program_\d+$"),
                CallbackQueryHandler(list_workouts, pattern="^workouts$"),
                CallbackQueryHandler(get_workout_name, pattern="^create_workout$"),
                CallbackQueryHandler(list_exercises, pattern=r"^workout_\d+$"),
                CallbackQueryHandler(list_exercises, pattern="^exercises$"),
                CallbackQueryHandler(get_exercise_name, pattern="^create_exercise$"),
                CallbackQueryHandler(list_sets, pattern=r"^exercise_\d+$"),
                CallbackQueryHandler(list_sets, pattern="^sets$"),
                CallbackQueryHandler(get_set_weight, pattern="^create_set$"),
                CallbackQueryHandler(get_set_info, pattern=r"^\d+set_\d+$"),
                CallbackQueryHandler(start_workout, pattern="^start_workout$"),
                CallbackQueryHandler(delete_set, pattern="^delete_set$"),
                CallbackQueryHandler(delete_exercise, pattern="^delete_exercise$"),
                CallbackQueryHandler(delete_workout, pattern="^delete_workout$"),
                CallbackQueryHandler(delete_program, pattern="^delete_program$"),
                CallbackQueryHandler(edit_set_weight, pattern="^edit_set$"),
                CallbackQueryHandler(move_program, pattern=r"^move_program_\d+_(up|down)$"),
                CallbackQueryHandler(move_workout, pattern=r"^move_workout_\d+_(up|down)$"),
                CallbackQueryHandler(move_exercise, pattern=r"^move_exercise_\d+_(up|down)$"),
                CallbackQueryHandler(move_set, pattern=r"^move_set_\d+_(up|down)$"),
                CallbackQueryHandler(workout_history, pattern="^history$"),
                CallbackQueryHandler(workout_history, pattern=r"^history_page_\d+$"),
                CallbackQueryHandler(fact_workout_details, pattern=r"^fact_workout_\d+$"),
            ],
            GET_GENDER: [
                CallbackQueryHandler(get_gender, pattern="^(male|female)$"),
            ],
            PROFILE: [
                CallbackQueryHandler(get_experience, pattern="^(beginner|intermediate|advanced)$"),
                CallbackQueryHandler(get_place, pattern="^(flat|gym)$"),
            ],
            GET_HEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_height)],
            GET_WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_weight)],
            GET_BODY_FAT_PERCENTAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_body_fat_percentage)],
            GET_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)],
            GET_PROGRAMM_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_program_handler)],
            GET_WORKOUT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_workout_handler)],
            GET_EXERCISE_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_exercise_handler)],
            GET_SET_WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_set_reps)],
            GET_SET_REPS: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_set_handler)],
            GET_FACT_REPS: [MessageHandler(filters.TEXT & ~filters.COMMAND, workout_way)],
            EDIT_SET_WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_set_reps)],
            EDIT_SET_REPS: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_set_handler)],
        },
        fallbacks=[CommandHandler("start", start)],
        name="main_conversation",
    )

    application.add_handler(conv_handler)
    
    return application
