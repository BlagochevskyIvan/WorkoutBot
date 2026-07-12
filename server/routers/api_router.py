from fastapi import APIRouter, Depends

from fastapi import Request, Response, status
from fastapi.responses import PlainTextResponse, FileResponse, JSONResponse
from fastapi.exceptions import HTTPException

from db.user_crud import get_user_crud
from db.programs_crud import get_programs, create_program, get_program, delete_program_crud, update_program, reorder_programs
from db.workout_crud import get_workouts, create_workout, delete_workout_crud, get_workout, update_workout, reorder_workouts
from db.exercise_crud import get_exercises, create_exercise, delete_exercise_crud, get_exercise, update_exercise, reorder_exercises
from db.set_crud import create_set, delete_set_crud, edit_set, get_set, get_sets, reorder_sets
from server.schemas.user import UserProfileResponse
from server.schemas.program import ProgramResponse, ProgramCreate, ProgramDetailResponse
from server.schemas.workout import WorkoutResponse, WorkoutCreate
from server.schemas.exercise import ExerciseResponse, ExerciseCreate
from server.schemas.set import SetResponse, SetCreate
from server.schemas.order import OrderUpdate
from server.dependency.auth import get_current_telegram_id

from telegram import Update
from config.cp_config import (
    TEMPLATE_PATH,
    WEBHOOK_PATH,
    SECRET_TOKEN,
)
from config.logger import logger

router = APIRouter()

@router.get('/user')
async def get_user():
    logger.info('мы')
    return JSONResponse({'name':'vanya'})

@router.get('/user2')
async def get_user2():
    logger.info('мы')
    return JSONResponse({'name':'vanya2'})

@router.get('/me')
async def get_me(telegram_id:int = Depends(get_current_telegram_id)):
    user = await get_user_crud(telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return UserProfileResponse.model_validate(user)

@router.get('/programs', response_model=list[ProgramResponse])
async def get_programs_js(telegram_id:int = Depends(get_current_telegram_id)):
    programs = await get_programs(telegram_id)
    if not programs:
        raise HTTPException(status_code=404, detail='Programs not found')
    return programs

@router.post('/programs', response_model=ProgramResponse)
async def add_program(body:ProgramCreate, telegram_id:int = Depends(get_current_telegram_id)):
    program = await create_program(telegram_id, body.name, body.description)
    return program

@router.get('/programs/{program_id}', response_model=ProgramDetailResponse)
async def get_program_js(program_id:int, telegram_id:int = Depends(get_current_telegram_id)):
    logger.info(f"Получен запрос на получение программы с id {program_id}")
    program = await get_program(program_id, telegram_id)
    if not program:
        raise HTTPException(status_code=404, detail='Program not found')
    return program

@router.get('/programs/{program_id}/workouts', response_model=list[WorkoutResponse])
async def get_workout_js(program_id:int, telegram_id:int = Depends(get_current_telegram_id)):
    workouts = await get_workouts(program_id, telegram_id)
    return workouts

@router.post('/programs/{program_id}/workouts', response_model=WorkoutResponse)
async def add_workout(program_id:int, body:WorkoutCreate, telegram_id:int = Depends(get_current_telegram_id)):
    workout = await create_workout(program_id, body.name, telegram_id)
    return workout


@router.delete('/programs/{program_id}')
async def delete_program_js(program_id:int, telegram_id:int = Depends(get_current_telegram_id)):
    await delete_program_crud(program_id, telegram_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/programs/{program_id}')
async def update_program_js(program_id:int, body:ProgramCreate, telegram_id:int = Depends(get_current_telegram_id)):
    program = await update_program(program_id, body.name, body.description, telegram_id)
    return program

@router.delete('/workouts/{workout_id}')
async def delete_workout_js(workout_id: int, telegram_id:int = Depends(get_current_telegram_id)):
    await delete_workout_crud(workout_id, telegram_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get('/workouts/{workout_id}', response_model=WorkoutResponse)
async def get_workout_detail_js(workout_id: int, telegram_id:int = Depends(get_current_telegram_id)):
    workout = await get_workout(workout_id, telegram_id)
    return workout


@router.get('/workouts/{workout_id}/exercises',
            response_model=list[ExerciseResponse])
async def get_workout_exercises_js(workout_id: int, telegram_id:int = Depends(get_current_telegram_id)):
    exercises = await get_exercises(workout_id, telegram_id)
    return exercises


@router.put('/workouts/{workout_id}',
            response_model=WorkoutResponse)
async def update_workout_js(
    workout_id: int,
    body: WorkoutCreate,
    telegram_id:int = Depends(get_current_telegram_id)
):
    workout = await update_workout(
        workout_id,
        body.name,
        telegram_id
    )
    return workout

@router.post('/workouts/{workout_id}/exercises', response_model=ExerciseResponse)
async def add_exercise(workout_id:int, body:ExerciseCreate, telegram_id:int = Depends(get_current_telegram_id)):
    exercise = await create_exercise(workout_id, body.name, telegram_id)
    return exercise


@router.get('/exercises/{exercise_id}', response_model=ExerciseResponse)
async def get_exercise_js(exercise_id:int, telegram_id:int = Depends(get_current_telegram_id)):
    exercise = await get_exercise(exercise_id, telegram_id)
    return exercise


@router.delete('/exercises/{exercise_id}')
async def delete_exercise_js(exercise_id:int, telegram_id:int = Depends(get_current_telegram_id)):
    await delete_exercise_crud(exercise_id, telegram_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/exercises/{exercise_id}', response_model=ExerciseResponse)
async def update_exercise_js(exercise_id:int, body:ExerciseCreate, telegram_id:int = Depends(get_current_telegram_id)):
    exercise = await update_exercise(exercise_id, body.name, telegram_id)
    return exercise


@router.get('/exercises/{exercise_id}/sets', response_model=list[SetResponse])
async def get_exercise_sets_js(exercise_id:int, telegram_id:int = Depends(get_current_telegram_id)):
    sets = await get_sets(exercise_id, telegram_id)
    return sets


@router.post('/exercises/{exercise_id}/sets', response_model=SetResponse)
async def add_set(exercise_id:int, body:SetCreate, telegram_id:int = Depends(get_current_telegram_id)):
    set = await create_set(exercise_id, body.weight, body.reps, telegram_id)
    return set


@router.get('/sets/{set_id}', response_model=SetResponse)
async def get_set_js(set_id:int, telegram_id:int = Depends(get_current_telegram_id)):
    set = await get_set(set_id, telegram_id)
    return set


@router.put('/sets/{set_id}', response_model=SetResponse)
async def update_set_js(set_id:int, body:SetCreate, telegram_id:int = Depends(get_current_telegram_id)):
    set = await edit_set(set_id, body.weight, body.reps, telegram_id)
    return set


@router.delete('/sets/{set_id}')
async def delete_set_js(set_id:int, telegram_id:int = Depends(get_current_telegram_id)):
    await delete_set_crud(set_id, telegram_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/order/programs')
async def reorder_programs_js(body:OrderUpdate, telegram_id:int = Depends(get_current_telegram_id)):
    try:
        await reorder_programs(body.ids, telegram_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/order/programs/{program_id}/workouts')
async def reorder_workouts_js(program_id:int, body:OrderUpdate, telegram_id:int = Depends(get_current_telegram_id)):
    try:
        await reorder_workouts(program_id, body.ids, telegram_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/order/workouts/{workout_id}/exercises')
async def reorder_exercises_js(workout_id:int, body:OrderUpdate, telegram_id:int = Depends(get_current_telegram_id)):
    try:
        await reorder_exercises(workout_id, body.ids, telegram_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/order/exercises/{exercise_id}/sets')
async def reorder_sets_js(exercise_id:int, body:OrderUpdate, telegram_id:int = Depends(get_current_telegram_id)):
    try:
        await reorder_sets(exercise_id, body.ids, telegram_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)
