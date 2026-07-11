from db.database import get_session
from db.models import Workout, Exercise, User, Program
from sqlalchemy import select
from typing import Optional


async def create_exercise(
    workout_id: int, name: str, telegram_id: int = None
) -> Exercise:
    async with get_session() as session:
        stmt = (
            select(Workout)
            .join(Workout.program)
            .join(Program.owner)
            .where(Workout.id == workout_id)
        )
        if telegram_id is not None:
            stmt = stmt.where(User.telegram_id == telegram_id)

        result = await session.execute(stmt)
        workout = result.scalars().first()

        if not workout:
            raise ValueError("Workout not found")

        exercise = Exercise(name=name, workout=workout)
        session.add(exercise)
        await session.commit()
        await session.refresh(exercise)

        return exercise


async def get_exercises(workout_id: int, telegram_id: int = None) -> list[Exercise]:
    async with get_session() as session:
        stmt = (
            select(Exercise)
            .join(Exercise.workout)
            .join(Workout.program)
            .join(Program.owner)
            .where(Exercise.workout_id == workout_id)
        )
        if telegram_id is not None:
            stmt = stmt.where(User.telegram_id == telegram_id)

        result = await session.execute(stmt)
        return list(result.scalars().all())


async def delete_exercise_crud(exercise_id: int, telegram_id: int = None) -> None:
    async with get_session() as session:
        stmt = (
            select(Exercise, User.telegram_id)
            .join(Exercise.workout)
            .join(Workout.program)
            .join(Program.owner)
            .where(Exercise.id == exercise_id)
        )

        row = (await session.execute(stmt)).first()
        if not row:
            return

        exercise, owner_telegram_id = row
        if telegram_id is not None and owner_telegram_id != telegram_id:
            raise ValueError("User does not own this exercise")

        await session.delete(exercise)
        await session.commit()


async def get_exercise(ex_id: int, telegram_id: int = None) -> Optional[Exercise]:
    async with get_session() as session:
        stmt = (
            select(Exercise)
            .join(Exercise.workout)
            .join(Workout.program)
            .join(Program.owner)
            .where(Exercise.id == ex_id)
        )
        if telegram_id is not None:
            stmt = stmt.where(User.telegram_id == telegram_id)

        return (await session.execute(stmt)).scalars().first()
