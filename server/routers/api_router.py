from fastapi import APIRouter

from fastapi import Request, Response, status
from fastapi.responses import PlainTextResponse, FileResponse, JSONResponse

from db.user_crud import get_user_crud
from db.programs_crud import get_programs, create_program, get_program, delete_program_crud, update_program
from db.workout_crud import get_workouts, create_workout
from server.schemas.user import UserProfileResponse
from server.schemas.program import ProgramResponse, ProgramCreate, ProgramDetailResponse
from server.schemas.workout import WorkoutResponse, WorkoutCreate

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


#url/api/me?telegram_id=1234
@router.get('/me')
async def get_me(telegram_id:int):
    user = await get_user_crud(telegram_id)
    logger.info(user.username)

    return UserProfileResponse.model_validate(user)

@router.get('/programs', response_model=list[ProgramResponse])
async def get_programs_js(telegram_id:int):
    programs = await get_programs(telegram_id)
    return programs

@router.post('/programs', response_model=ProgramResponse)
async def add_program(telegram_id:int, body:ProgramCreate):
    program = await create_program(telegram_id, body.name)
    return program

@router.get('/programs/{program_id}', response_model=ProgramDetailResponse)
async def get_program_js(program_id:int):
    logger.info(f"Получен запрос на получение программы с id {program_id}")
    program = await get_program(program_id)
    return program

@router.get('/programs/{program_id}/workouts', response_model=list[WorkoutResponse])
async def get_workout_js(program_id:int):
    workouts = await get_workouts(program_id)
    return workouts

@router.post('/programs/{program_id}/workouts', response_model=WorkoutResponse)
async def add_workout(program_id:int, body:WorkoutCreate):
    workout = await create_workout(program_id, body.name)
    return workout


@router.delete('/programs/{program_id}')
async def delete_program_js(program_id:int):
    await delete_program_crud(program_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/programs/{program_id}')
async def update_program_js(program_id:int, body:ProgramCreate):
    program = await update_program(program_id, body.name, body.description)
    return program
