from db.database import get_session
from db.models import Workout, Exercise
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def create_exercise(id: int, name: str) -> Exercise:
    async with get_session() as session:
        stmt = select(Workout).where(Workout.id == id)
        result = await session.execute(stmt)
        workout = result.scalars().first()
        
        if not workout:
            raise ValueError("Workout not found")

        exercise = Exercise(name=name, workout=workout)
        session.add(exercise)
        await session.commit()
        await session.refresh(exercise)

        return exercise

async def get_exercises(id: int) -> list[Exercise]:
    async with get_session() as session:
        stmt = (
            select(Workout)
            .where(Workout.id == id)
            .options(selectinload(Workout.exercises))
        )

        result = await session.execute(stmt)
        workout = result.scalars().first()

        if not workout:
            return []

        return workout.exercises
            