from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config.states import GET_FACT_REPS, MENU
from db.fact_workout_crud import create_fact_workout, get_fact_workouts
from db.exercise_crud import get_exercises
from db.set_crud import get_sets
from db.fact_exercise_crud import create_fact_exercise
from db.fact_set_crud import create_fact_set


async def start_workout(update: Update, context: ContextTypes) -> None:
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    workout_id = context.user_data["workout_id"]
    fact_workout_num = len(await get_fact_workouts(user_id=user_id)) + 1
    fact_workout = await create_fact_workout(user_id=user_id, workout_id=workout_id)
    context.user_data["fact_workout_id"] = fact_workout.id

    exercises = await get_exercises(workout_id=workout_id)
    fact_exercise_num = 0
    exercise = exercises[fact_exercise_num]
    fact_exercise = await create_fact_exercise(fact_workout_id=context.user_data["fact_workout_id"], name=exercise.name)
    sets = await get_sets(exercise_id=exercise.id)
    fact_set_num = 0
    fact_set = sets[fact_set_num]
    context.user_data["weight_sum"] = 0
    context.user_data["fact_exercise"] = fact_exercise
    context.user_data["exercises"] = exercises
    context.user_data["fact_exercise_num"] = fact_exercise_num
    context.user_data["sets"] = sets
    context.user_data["fact_set_num"] = fact_set_num

    
    message = await query.edit_message_text(
        text=f"Тренировка {fact_workout_num}\n{fact_workout.created_at.strftime('%d/%m/%y')}\nУпражнение {fact_exercise_num+1}\n{fact_exercise.name}\n\nПодход {fact_set_num+1}\n{fact_set.weight}кг х {fact_set.reps}\n\nВведите количество сделанных повторений:"
    )
    context.user_data["question_message_id"] = message.id
    return GET_FACT_REPS

async def workout_way(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reps = update.effective_message.text

    await context.bot.delete_messages(
        chat_id=update.effective_chat.id,
        message_ids=[update.effective_message.id]
    )

    sets = context.user_data["sets"]
    fact_set_num = context.user_data["fact_set_num"]
    fact_exercise = context.user_data["fact_exercise"]
    exercises = context.user_data["exercises"]
    fact_exercise_num = context.user_data["fact_exercise_num"]

    fact_set = sets[fact_set_num]

    await create_fact_set(
        fact_exercise_id=fact_exercise.id,
        reps=int(reps),
        weight=fact_set.weight
    )

    context.user_data["weight_sum"] += fact_set.weight * int(reps)

    fact_set_num += 1
    if fact_set_num >= len(sets):
        fact_exercise_num += 1
        if fact_exercise_num >= len(exercises):
            workout_id = context.user_data["workout_id"]
            keyboard = [
                [InlineKeyboardButton(text="К тренировке", callback_data=f"workout_{workout_id}")],
                [InlineKeyboardButton(text="В меню", callback_data="menu")]
            ]
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=context.user_data["question_message_id"],
                text=f"Тренировка завершена!\nВсего поднято: {context.user_data['weight_sum']}кг",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return MENU

        exercise = exercises[fact_exercise_num]
        fact_exercise = await create_fact_exercise(
            fact_workout_id=context.user_data["fact_workout_id"],
            name=exercise.name
        )

        sets = await get_sets(exercise_id=exercise.id)
        fact_set_num = 0
        fact_set = sets[fact_set_num]

        context.user_data["fact_exercise"] = fact_exercise
        context.user_data["fact_exercise_num"] = fact_exercise_num
        context.user_data["sets"] = sets
        context.user_data["fact_set_num"] = fact_set_num

    else:
        context.user_data["fact_set_num"] = fact_set_num
        fact_set = sets[fact_set_num]

    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=context.user_data["question_message_id"],
        text=(
            f"Упражнение {context.user_data['fact_exercise_num']+1}\n"
            f"{context.user_data['fact_exercise'].name}\n\n"
            f"Подход {fact_set_num+1}\n"
            f"{fact_set.weight}кг х {fact_set.reps}\n\n"
            f"Введите количество сделанных повторений:"
        )
    )

    return GET_FACT_REPS

