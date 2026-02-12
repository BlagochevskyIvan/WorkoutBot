from telegram import Update
from telegram.ext import ContextTypes
from config.states import MENU
from libs.sub_func import date_now
from db.fact_workout_crud import create_fact_workout, get_fact_workouts
from db.exercise_crud import get_exercises
from db.set_crud import get_sets


async def start_workout(update: Update, context: ContextTypes) -> None:
    query = update.callback_query
    await query.answer()
    created_at = date_now()
    user_id = update.effective_user.id
    workout_id = context.user_data["workout_id"]
    fact_workout_num = len(await get_fact_workouts(user_id=user_id)) + 1
    fact_workout = await create_fact_workout(created_at=created_at, user_id=user_id, workout_id=workout_id)
    context.user_data["fact_workout_id"] = fact_workout.id

    fact_exercises = await get_exercises(workout_id=workout_id)
    exercise_num = 0
    fact_exercise = fact_exercises[exercise_num]
    fact_sets = await get_sets(exercise_id=fact_exercise.id)
    set_num = 0
    fact_set = fact_sets[set_num]
    
    await query.edit_message_text(
        text=f"Тренировка {fact_workout_num}\n{created_at.strftime('%d/%m/%y')}\nУпражнение {exercise_num+1}\n{fact_exercise.name}\n\nПодход {set_num+1}\n{fact_set.weight}кг х {fact_set.reps}"
    )

    return MENU