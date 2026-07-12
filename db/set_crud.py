from db.database import get_session
from db.models import Exercise, Program, Set, User, Workout
from sqlalchemy import func, select
from typing import Optional
from sqlalchemy.orm import selectinload


async def create_set(
    exercise_id: int,
    weight: float,
    reps: int,
    telegram_id: int = None
) -> Set:
    async with get_session() as session:
        stmt = (
            select(Exercise)
            .where(Exercise.id == exercise_id)
        )

        if telegram_id:
            stmt = (
                stmt.join(Exercise.workout)
                .join(Workout.program)
                .join(Program.owner)
                .where(User.telegram_id == telegram_id)
            )

        result = await session.execute(stmt)
        exercise = result.scalars().first()

        if not exercise:
            raise ValueError("Exercise not found")

        position = await session.scalar(
            select(func.coalesce(func.max(Set.position), -1) + 1)
            .where(Set.exercise_id == exercise_id)
        )
        set_obj = Set(
            weight=weight,
            reps=reps,
            exercise=exercise,
            position=position
        )
        session.add(set_obj)
        await session.commit()
        await session.refresh(set_obj)

        return set_obj


async def get_sets(exercise_id: int, telegram_id: int = None) -> list[Set]:
    async with get_session() as session:
        stmt = (
            select(Exercise)
            .where(Exercise.id == exercise_id)
            .options(selectinload(Exercise.sets))
        )

        if telegram_id:
            stmt = (
                stmt.join(Exercise.workout)
                .join(Workout.program)
                .join(Program.owner)
                .where(User.telegram_id == telegram_id)
            )

        result = await session.execute(stmt)
        exercise = result.scalars().first()

        if not exercise:
            return []

        return exercise.sets


async def reorder_sets(
    exercise_id: int,
    set_ids: list[int],
    telegram_id: int = None
) -> None:
    async with get_session() as session:
        stmt = (
            select(Set)
            .where(Set.exercise_id == exercise_id)
        )
        if telegram_id:
            stmt = (
                stmt.join(Set.exercise)
                .join(Exercise.workout)
                .join(Workout.program)
                .join(Program.owner)
                .where(User.telegram_id == telegram_id)
            )

        sets = list((await session.execute(stmt)).scalars().all())
        if len(set_ids) != len(sets) or set(set_ids) != {set_obj.id for set_obj in sets}:
            raise ValueError("Invalid set order")

        sets_by_id = {set_obj.id: set_obj for set_obj in sets}
        for position, set_id in enumerate(set_ids):
            sets_by_id[set_id].position = position

        await session.commit()


async def delete_set_crud(set_id: int, telegram_id: int = None) -> None:
    async with get_session() as session:
        stmt = (
            select(Set)
            .where(Set.id == set_id)
        )

        if telegram_id:
            stmt = (
                stmt.join(Set.exercise)
                .join(Exercise.workout)
                .join(Workout.program)
                .join(Program.owner)
                .where(User.telegram_id == telegram_id)
            )

        set_obj = (await session.execute(stmt)).scalars().first()

        if not set_obj:
            return

        await session.delete(set_obj)
        await session.commit()


async def get_set(set_id: int, telegram_id: int = None) -> Optional[Set]:
    async with get_session() as session:
        stmt = (
            select(Set)
            .where(Set.id == set_id)
        )

        if telegram_id:
            stmt = (
                stmt.join(Set.exercise)
                .join(Exercise.workout)
                .join(Workout.program)
                .join(Program.owner)
                .where(User.telegram_id == telegram_id)
            )

        return (await session.execute(stmt)).scalars().first()


async def edit_set(
    set_id: int,
    weight: float,
    reps: int,
    telegram_id: int = None
) -> Optional[Set]:
    async with get_session() as session:
        stmt = (
            select(Set)
            .where(Set.id == set_id)
        )

        if telegram_id:
            stmt = (
                stmt.join(Set.exercise)
                .join(Exercise.workout)
                .join(Workout.program)
                .join(Program.owner)
                .where(User.telegram_id == telegram_id)
            )

        set_obj = (await session.execute(stmt)).scalars().first()

        if not set_obj:
            return

        set_obj.weight = weight
        set_obj.reps = reps
        await session.commit()
        await session.refresh(set_obj)
        return set_obj
