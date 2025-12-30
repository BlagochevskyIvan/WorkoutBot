from db.database import get_session
from db.models import User, Program
from sqlalchemy import select, update
from typing import Optional
from sqlalchemy.orm import selectinload

async def create_program(telegram_id: int, name: str) -> Program:
    async with get_session() as session:
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        user = result.scalars().first()

        if not user:
            raise ValueError("User not found")

        program = Program(name=name, owner=user, is_template=False)
        session.add(program)
        await session.commit()
        await session.refresh(program)
        
        return program
    
async def get_programs(telegram_id: int) -> list[Program]:
    async with get_session() as session:
        stmt = (
            select(User)
            .where(User.telegram_id == telegram_id)
            .options(selectinload(User.programs))
        )

        result = await session.execute(stmt)
        user = result.scalars().first()

        if not user:
            return []

        return user.programs


    
    
