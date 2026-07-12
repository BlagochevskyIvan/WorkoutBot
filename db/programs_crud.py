from db.database import get_session
from db.models import User, Program
from sqlalchemy import func, select, update
from sqlalchemy.orm import selectinload
from typing import Optional

async def create_program(telegram_id: int, name: str, description: str | None = None) -> Program:
    async with get_session() as session:
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        user = result.scalars().first()

        if not user:
            raise ValueError("User not found")

        position = await session.scalar(
            select(func.coalesce(func.max(Program.position), -1) + 1)
            .where(Program.owner_id == user.id)
        )
        program = Program(
            name=name,
            description=description,
            owner=user,
            is_template=False,
            owner_id=user.id,
            position=position
        )
        session.add(program)
        await session.commit()
        await session.refresh(program)
        
        return program


async def reorder_programs(program_ids: list[int], telegram_id: int) -> None:
    async with get_session() as session:
        stmt = (
            select(Program)
            .join(Program.owner)
            .where(User.telegram_id == telegram_id)
        )
        programs = list((await session.execute(stmt)).scalars().all())

        if len(program_ids) != len(programs) or set(program_ids) != {program.id for program in programs}:
            raise ValueError("Invalid program order")

        programs_by_id = {program.id: program for program in programs}
        for position, program_id in enumerate(program_ids):
            programs_by_id[program_id].position = position

        await session.commit()
    
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
    
async def delete_program_crud(program_id: int, telegram_id: int = None) -> None:
    async with get_session() as session:
        stmt = (
            select(Program)
            .where(Program.id == program_id)
        )
        if telegram_id:
            stmt = stmt.join(Program.owner).where(User.telegram_id == telegram_id)

        program = (await session.execute(stmt)).scalars().first()

        if not program:
            return

        await session.delete(program)
        await session.commit()

async def get_program(program_id: int, telegram_id: int = None) -> Optional[Program]:
    async with get_session() as session:
        stmt = (
            select(Program)
            .where(Program.id == program_id)
            .options(selectinload(Program.workouts))
        )
        if telegram_id:
            stmt = stmt.join(Program.owner).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        program = result.scalars().first()
    return program

async def update_program(
    program_id: int,
    name: str | None = None,
    description: str | None = None,
    telegram_id: int | None = None
):
    async with get_session() as session:
        stmt = (
            select(Program)
            .where(Program.id == program_id)
            .options(selectinload(Program.workouts))
        )
        if telegram_id:
            stmt = stmt.join(Program.owner).where(User.telegram_id == telegram_id)

        result = await session.execute(stmt)
        program = result.scalars().first()

        if name is not None:
            program.name = name

        if description is not None:
            program.description = description

        await session.commit()
        await session.refresh(program)

        return program




    
    
