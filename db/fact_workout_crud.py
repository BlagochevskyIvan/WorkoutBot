from db.database import get_session
from db.models import Workout, FactWorkout, User
from sqlalchemy import select

async def create_fact_workout(workout_id: int, user_id: int, name: str) -> FactWorkout:
    async with get_session() as session:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        user = result.scalars().first()

        if not user:
            raise ValueError("User not found")

        stmt = select(Workout).where(Workout.id == workout_id)
        result = await session.execute(stmt)
        workout = result.scalars().first()

        if not workout:
            raise ValueError("Workout not found")

        fact_workout = FactWorkout(name=name, user=user, workout=workout)
        session.add(fact_workout)
        await session.commit()
        await session.refresh(fact_workout)

        return fact_workout
