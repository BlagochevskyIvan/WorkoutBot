from datetime import date
from db.database import get_session
from db.models import Workout, FactWorkout, User
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

async def create_fact_workout(workout_id: int, user_id: int) -> FactWorkout:
    async with get_session() as session:
        stmt = select(User).where(User.telegram_id == user_id)
        result = await session.execute(stmt)
        user = result.scalars().first()

        if not user:
            raise ValueError("User not found")

        stmt = select(Workout).where(Workout.id == workout_id)
        result = await session.execute(stmt)
        workout = result.scalars().first()

        if not workout:
            raise ValueError("Workout not found")

        fact_workout = FactWorkout(user=user, workout=workout)
        session.add(fact_workout)
        await session.commit()
        await session.refresh(fact_workout)

        return fact_workout
    
async def get_fact_workouts(user_id: int) -> list[FactWorkout]:
    async with get_session() as session:
        stmt = select(User).where(User.telegram_id == user_id).options(selectinload(User.fact_workouts))
        result = await session.execute(stmt)
        user = result.scalars().first() 
        if not user:
            raise ValueError("User not found")
        
        return user.fact_workouts
        
async def get_count_workouts(user_tg_id: int) -> int:
    async with get_session() as session:
        stmt = select(func.count(FactWorkout.id)).join(User, User.id == FactWorkout.user_id).where(User.telegram_id==user_tg_id)
        result = await session.execute(stmt)
        count = result.scalar_one()
        return count