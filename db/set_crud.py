from db.database import get_session
from db.models import Exercise, Set
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def create_set(exercise_id: int, name: str) -> Exercise:
    async with get_session() as session:
        stmt = select(Exercise).where(Exercise.id == exercise_id)
        result = await session.execute(stmt)
        exercise = result.scalars().first()

        if not exercise:
            raise ValueError("Exercise not found")

        set = Set(exercise=exercise)
        session.add(set)
        await session.commit()
        await session.refresh(set)

        return set
    
async def get_sets(id: int) -> list[Set]:
    async with get_session() as session:
        stmt = (
            select(Exercise)
            .where(Exercise.id == id)
            .options(selectinload(Exercise.sets))
        )

        result = await session.execute(stmt)
        exercise = result.scalars().first()

        if not exercise:
            return []

        return exercise.sets
        
async def delete_set(set_id: int) -> None:
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