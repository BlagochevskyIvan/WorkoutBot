from db.database import get_session
from db.models import Exercise, Repetition
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def create_repetition(id: int, name: str) -> Exercise:
    async with get_session() as session:
        stmt = select(Exercise).where(Exercise.id == id)
        result = await session.execute(stmt)
        exercise = result.scalars().first()

        if not exercise:
            raise ValueError("Workout not found")

        repetition = Repetition(exercise=exercise)
        session.add(repetition)
        await session.commit()
        await session.refresh(repetition)

        return repetition
    
async def get_repetitions(id: int) -> list[Repetition]:
    async with get_session() as session:
        stmt = (
            select(Exercise)
            .where(Exercise.id == id)
            .options(selectinload(Exercise.exercises))
        )

        result = await session.execute(stmt)
        exercise = result.scalars().first()

        if not exercise:
            return []

        return exercise.repetitions
        
async def delete_repetition(repetition_id: int) -> None:
    async with get_session() as session:
        repetition = (
            await session.execute(
                select(Repetition).where(Repetition.id == repetition_id)
            )
        ).scalars().first()

        if not repetition:
            return

        await session.delete(repetition)
        await session.commit()