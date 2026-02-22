from db.database import get_session
from db.models import Exercise, Set
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from typing import Optional

async def create_set(exercise_id: int, weight: float, reps: int) -> Exercise:
    async with get_session() as session:
        stmt = select(Exercise).where(Exercise.id == exercise_id)
        result = await session.execute(stmt)
        exercise = result.scalars().first()

        if not exercise:
            raise ValueError("Exercise not found")

        set = Set(weight=weight, reps=reps, exercise=exercise)
        session.add(set)
        await session.commit()
        await session.refresh(set)

        return set
    
async def get_sets(exercise_id: int) -> list[Set]:
    async with get_session() as session:
        stmt = (
            select(Exercise)
            .where(Exercise.id == exercise_id)
            .options(selectinload(Exercise.sets))
        )

        result = await session.execute(stmt)
        exercise = result.scalars().first()

        if not exercise:
            return []

        return exercise.sets
        
async def delete_set_crud(set_id: int) -> None:
    async with get_session() as session:
        set = (
            await session.execute(
                select(Set).where(Set.id == set_id)
            )
        ).scalars().first()

        if not set:
            return

        await session.delete(set)
        await session.commit()

async def get_set(set_id: int) -> Optional[Set]:
    async with get_session() as session:
        set = (
            await session.execute(
                select(Set).where(Set.id == set_id)
            )
        ).scalars().first()
    return set

async def edit_set(set_id: int, weight: float, reps: int):
    async with get_session() as session:
        await session.execute(
            update(Set)
            .values(weight=weight, reps=reps)
            .where(Set.id == set_id)
        )
        await session.commit()