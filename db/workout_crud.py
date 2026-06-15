from db.database import get_session
from db.models import Program, Workout
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Optional

async def create_workout(program_id: int, name: str) -> Workout:
    async with get_session() as session:
        stmt = select(Program).where(Program.id == program_id)
        result = await session.execute(stmt)
        program = result.scalars().first()

        if not program:
            raise ValueError("Program not found")

        workout = Workout(name=name, program=program)
        session.add(workout)
        await session.commit()
        await session.refresh(workout)

        return workout
    
async def get_workouts(program_id: int) -> list[Workout]:
    async with get_session() as session:
        stmt = (
            select(Program)
            .where(Program.id==program_id)
            .options(selectinload(Program.workouts))
        )

        result = await session.execute(stmt)
        program = result.scalars().first()

        if not program:
            return []

        return program.workouts
    
async def delete_workout_crud(workout_id: int) -> None:
    async with get_session() as session:
        workout = (
            await session.execute(
                select(Workout).where(Workout.id == workout_id)
            )
        ).scalars().first()

        if not workout:
            return

        await session.delete(workout)
        await session.commit()

async def get_workout(workout_id: int) -> Optional[Workout]:
    async with get_session() as session:
        workout = (
            await session.execute(
                select(Workout).where(Workout.id == workout_id)
            )
        ).scalars().first()
    return workout


async def update_workout(
    workout_id: int,
    name: str | None = None,
):
    async with get_session() as session:
        stmt = (
            select(Workout)
            .where(Workout.id == workout_id)
            .options(selectinload(Workout.exercises))
        )

        result = await session.execute(stmt)
        workout = result.scalars().first()

        if workout is None:
            return None

        if name is not None:
            workout.name = name

        await session.commit()
        await session.refresh(workout)

        return workout