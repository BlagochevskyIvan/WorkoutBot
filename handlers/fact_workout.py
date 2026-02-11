from telegram import Update
from telegram.ext import ContextTypes
from libs.sub_func import date_now
from db.fact_workout_crud import create_fact_workout


async def start_workout(update: Update, context: ContextTypes) -> None:
    query = update.callback_query
    await query.answer()
    created_at = date_now()
    user_id = update.effective_user.id
    workout_id = context.user_data["workout_id"]
    fact_workout = create_fact_workout(created_at=created_at, user_id=user_id, workout_id=workout_id)
    context.user_data["fact_workout_id"] = fact_workout.id


