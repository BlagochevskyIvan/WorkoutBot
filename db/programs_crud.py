from db.database import get_session
from db.models import User, Program
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

async def create_program(telegram_id: int, name: str) -> Program:
    async with get_session() as session:
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        user = result.scalars().first()

        if not user:
            raise ValueError("User not found")

        program = Program(name=name, owner=user, is_template=False, owner_id=user.id)
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
    
async def delete_program(program_id: int) -> None:
    async with get_session() as session:
        program = (
            await session.execute(
                select(Program).where(Program.id == program_id)
            )
        ).scalars().first()

        if not program:
            return

        await session.delete(program)
        await session.commit()





    
    
