from telegram import Update
from telegram.ext import ContextTypes

from db.exercise_crud import get_exercises, reorder_exercises
from db.programs_crud import get_programs, reorder_programs
from db.set_crud import get_sets, reorder_sets
from db.workout_crud import get_workouts, reorder_workouts
from handlers.exercise import list_exercises
from handlers.programs import list_programs
from handlers.set import list_sets
from handlers.workout import list_workouts


def move_item_ids(items, item_id: int, direction: str) -> list[int]:
    ids = [item.id for item in items]
    current_index = ids.index(item_id)
    target_index = current_index - 1 if direction == "up" else current_index + 1
    if 0 <= target_index < len(ids):
        ids[current_index], ids[target_index] = ids[target_index], ids[current_index]
    return ids


def parse_move_data(data: str) -> tuple[int, str]:
    parts = data.split("_")
    return int(parts[2]), parts[3]


async def move_program(update: Update, context: ContextTypes.DEFAULT_TYPE):
    item_id, direction = parse_move_data(update.callback_query.data)
    telegram_id = update.effective_user.id
    programs = await get_programs(telegram_id)
    await reorder_programs(move_item_ids(programs, item_id, direction), telegram_id)
    return await list_programs(update, context)


async def move_workout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    item_id, direction = parse_move_data(update.callback_query.data)
    telegram_id = update.effective_user.id
    program_id = context.user_data["program_id"]
    workouts = await get_workouts(program_id, telegram_id)
    await reorder_workouts(
        program_id,
        move_item_ids(workouts, item_id, direction),
        telegram_id
    )
    return await list_workouts(update, context)


async def move_exercise(update: Update, context: ContextTypes.DEFAULT_TYPE):
    item_id, direction = parse_move_data(update.callback_query.data)
    telegram_id = update.effective_user.id
    workout_id = context.user_data["workout_id"]
    exercises = await get_exercises(workout_id, telegram_id)
    await reorder_exercises(
        workout_id,
        move_item_ids(exercises, item_id, direction),
        telegram_id
    )
    return await list_exercises(update, context)


async def move_set(update: Update, context: ContextTypes.DEFAULT_TYPE):
    item_id, direction = parse_move_data(update.callback_query.data)
    telegram_id = update.effective_user.id
    exercise_id = context.user_data["exercise_id"]
    sets = await get_sets(exercise_id, telegram_id)
    await reorder_sets(
        exercise_id,
        move_item_ids(sets, item_id, direction),
        telegram_id
    )
    return await list_sets(update, context)
