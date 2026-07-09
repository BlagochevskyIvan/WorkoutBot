from db.database import get_session
from db.models import Workout, Exercise, User, Program
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Optional

async def create_exercise(workout_id: int, name: str, telegram_id: int = None) -> Exercise:
    async with get_session() as session:
        stmt = select(Workout).where(Workout.id == workout_id)
        result = await session.execute(stmt)
        workout = result.scalars().first()

        if not workout:
            raise ValueError("Workout not found")
        if telegram_id and workout.owner.telegram_id != telegram_id:
            raise ValueError("User does not own this workout")

        exercise = Exercise(name=name, workout=workout)
        session.add(exercise)
        await session.commit()
        await session.refresh(exercise)

        return exercise

async def get_exercises(workout_id: int, telegram_id: int = None) -> list[Exercise]:
    async with get_session() as session:
        stmt = (
            select(Workout)
            .where(Workout.id == workout_id)
            .options(selectinload(Workout.exercises))
        )
        if telegram_id:
            stmt = stmt.join(Workout.owner).where(User.telegram_id == telegram_id)

        result = await session.execute(stmt)
        workout = result.scalar_one_or_none()

        if not workout:
            return []

        return workout.exercises
        
async def delete_exercise_crud(exercise_id: int, telegram_id: int = None) -> None:
    async with get_session() as session:
        exercise = (
            await session.execute(
                select(Exercise).where(Exercise.id == exercise_id)
            )
        ).scalars().first()
        if telegram_id and exercise and exercise.workout.owner.telegram_id != telegram_id:
            raise ValueError("User does not own this exercise")
        if not exercise:
            return

        await session.delete(exercise)
        await session.commit()

async def get_exercise(ex_id: int, telegram_id: int = None) -> Optional[Exercise]:
    async with get_session() as session:
        stmt = select(Exercise).where(Exercise.id == ex_id)
        if telegram_id:
            stmt = stmt.join(Exercise.workout).join(Workout.owner).where(User.telegram_id == telegram_id)
        exercise = (
            await session.execute(stmt)
        ).scalars().first()
    return exercise 