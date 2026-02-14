from db.database import get_session
from db.models import FactExercise, FactSet
from sqlalchemy import select

async def create_fact_set(fact_exercise_id: int, reps: int, weight: float) -> FactSet:
    async with get_session() as session:
        stmt = select(FactExercise).where(FactExercise.id == fact_exercise_id)
        result = await session.execute(stmt)
        fact_exercise = result.scalars().first()

        if not fact_exercise:
            raise ValueError("Fact workout not found")

        fact_set = FactSet(fact_exercise_id=fact_exercise_id, reps=reps, fact_exercise=fact_exercise, weight=weight)
        session.add(fact_set)
        await session.commit()
        await session.refresh(fact_set)

        return fact_set
