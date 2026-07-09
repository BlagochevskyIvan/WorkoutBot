from db.database import get_session
from db.models import Program, Workout, User
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Optional

async def create_workout(program_id: int, name: str, telegram_id: int = None) -> Workout:
    async with get_session() as session:
        stmt = select(Program).where(Program.id == program_id)
        result = await session.execute(stmt)
        program = result.scalars().first()

        if not program:
            raise ValueError("Program not found")
        if telegram_id and program.owner.telegram_id != telegram_id:
            raise ValueError("User does not own this program")
        workout = Workout(name=name, program=program)
        session.add(workout)
        await session.commit()
        await session.refresh(workout)

        return workout
    
async def get_workouts(program_id: int, telegram_id: int = None) -> list[Workout]:
    async with get_session() as session:
        stmt = (
            select(Program)
            .where(Program.id==program_id)
            .options(selectinload(Program.workouts))
        )

        if telegram_id:
            stmt = stmt.join(Program.owner).where(User.telegram_id == telegram_id)

        result = await session.execute(stmt)
        program = result.scalars().first()

        if not program:
            return []

        return program.workouts
    
async def delete_workout_crud(workout_id: int, telegram_id: int = None) -> None:
    async with get_session() as session:
        workout = (
            await session.execute(
                select(Workout).where(Workout.id == workout_id)
            )
        ).scalars().first()
        if telegram_id and workout and workout.program.owner.telegram_id != telegram_id:
            raise ValueError("User does not own this workout")
        if not workout:
            return

        await session.delete(workout)
        await session.commit()

async def get_workout(workout_id: int, telegram_id: int = None) -> Optional[Workout]:
    async with get_session() as session:
        stmt = select(Workout).where(Workout.id == workout_id)
        if telegram_id:
            stmt = stmt.join(Workout.program).join(Program.owner).where(User.telegram_id == telegram_id)
        workout = (
            await session.execute(stmt)
            ).scalars().first()
    return workout


async def update_workout(
    workout_id: int,
    name: str | None = None,
    telegram_id: int = None
):
    async with get_session() as session:
        stmt = (
            select(Workout)
            .where(Workout.id == workout_id)
            .options(selectinload(Workout.exercises))
        )
        if telegram_id:
            stmt = stmt.join(Workout.program).join(Program.owner).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        workout = result.scalars().first()

        if workout is None:
            return None

        if name is not None:
            workout.name = name

        await session.commit()
        await session.refresh(workout)

        return workout