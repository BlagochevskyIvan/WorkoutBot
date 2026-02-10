from db.database import get_session
from db.models import FactExercise, FactWorkout
from sqlalchemy import select

async def create_fact_exercise(fact_workout_id: int, name: str) -> FactExercise:
    async with get_session() as session:
        stmt = select(FactWorkout).where(FactWorkout.id == fact_workout_id)
        result = await session.execute(stmt)
        fact_workout = result.scalars().first()

        if not fact_workout:
            raise ValueError("Fact workout not found")

        fact_exercise = FactExercise(name=name, fact_workout_id=fact_workout_id, fact_workout=fact_workout)
        session.add(fact_exercise)
        await session.commit()
        await session.refresh(fact_exercise)

        return fact_exercise
