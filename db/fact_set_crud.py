from db.database import get_session
from db.models import FactExercise, FactSet
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def create_fact_set(fact_exercise_id: int, reps: int, weight: float, nom_reps: int) -> FactSet:
    async with get_session() as session:
        stmt = select(FactExercise).where(FactExercise.id == fact_exercise_id)
        result = await session.execute(stmt)
        fact_exercise = result.scalars().first()

        if not fact_exercise:
            raise ValueError("Fact workout not found")

        fact_set = FactSet(fact_exercise_id=fact_exercise_id, reps=reps, fact_exercise=fact_exercise, weight=weight, nom_reps=nom_reps)
        session.add(fact_set)
        await session.commit()
        await session.refresh(fact_set)

        return fact_set

async def get_fact_sets(fact_exercise_id: int) -> list[FactSet]:
    async with get_session() as session:
        stmt = select(FactExercise).where(FactExercise.id == fact_exercise_id).options(selectinload(FactExercise.fact_sets))
        result = await session.execute(stmt)
        fact_exercise = result.scalars().first() 
        if not fact_exercise:
            raise ValueError("Fact workout not found")
        
        return fact_exercise.fact_sets