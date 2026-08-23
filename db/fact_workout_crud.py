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

        fact_workout = FactWorkout(user=user, workout=workout, name=workout.name)
        session.add(fact_workout)
        await session.commit()
        await session.refresh(fact_workout)

        return fact_workout


async def get_fact_workouts(user_id: int) -> list[FactWorkout]:
    async with get_session() as session:
        stmt = (
            select(User)
            .where(User.telegram_id == user_id)
            .options(selectinload(User.fact_workouts))
        )
        result = await session.execute(stmt)
        user = result.scalars().first()
        if not user:
            raise ValueError("User not found")

        return user.fact_workouts


async def get_fact_workouts_page(
    telegram_id: int, page: int, page_size: int
) -> tuple[list[FactWorkout], int]:
    async with get_session() as session:
        stmt_user_id = select(User.id).where(User.telegram_id == telegram_id)
        result_user_id = (await session.execute(stmt_user_id)).scalar_one_or_none()

        total = (
            await session.execute(
                select(func.count(FactWorkout.id)).where(
                    FactWorkout.user_id == result_user_id
                )
            )
        ).scalar_one()

        offset = (page - 1) * page_size
        stmt = (
            select(FactWorkout)
            .where(FactWorkout.user_id == result_user_id)
            .order_by(FactWorkout.created_at.desc(), FactWorkout.id.desc())
            .offset(offset)
            .limit(page_size)
        )
        result = await session.execute(stmt)
        return result.scalars().all(), total


async def get_fact_workout(fact_workout_id: int) -> FactWorkout:
    async with get_session() as session:
        stmt = select(FactWorkout).where(FactWorkout.id == fact_workout_id)
        result = await session.execute(stmt)
        fact_workout = result.scalars().first()

        if not fact_workout:
            raise ValueError("Fact workout not found")

        return fact_workout


async def get_count_workouts(user_tg_id: int) -> int:
    async with get_session() as session:
        stmt = (
            select(func.count(FactWorkout.id))
            .join(User, User.id == FactWorkout.user_id)
            .where(User.telegram_id == user_tg_id)
        )
        result = await session.execute(stmt)
        count = result.scalar_one()
        return count
