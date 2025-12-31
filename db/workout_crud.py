from db.database import get_session
from db.models import User, Program, Workout
from sqlalchemy import select, update
from typing import Optional
from sqlalchemy.orm import selectinload

async def create_workout(id: int, name: str) -> Workout:
    async with get_session() as session:
        stmt = select(Program).where(Program.id == id)
        result = await session.execute(stmt)
        program = result.scalars().first()

        if not program:
            raise ValueError("Program not found")

        workout = Workout(name=name, program=program)
        session.add(workout)
        await session.commit()
        await session.refresh(workout)

        return workout
    
async def get_workouts(id: int) -> list[Workout]:
    async with get_session() as session:
        stmt = (
            select(Program)
            .where(Program.id==id)
            .options(selectinload(Program.workouts))
        )

        result = await session.execute(stmt)
        program = result.scalars().first()

        if not program:
            return []

        return program.workouts