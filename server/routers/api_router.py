from fastapi import APIRouter

from fastapi import Request, Response, status
from fastapi.responses import PlainTextResponse, FileResponse, JSONResponse

from db.user_crud import get_user_crud
from db.programs_crud import get_programs
from server.schemas.user import UserProfileResponse
from server.schemas.program import ProgramResponse

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
async def get_program_js(telegram_id:int):
    programs = await get_programs(telegram_id)

    return programs
    