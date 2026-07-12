from db.database import get_session
from db.models import Program, Workout, User
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from typing import Optional

async def create_workout(program_id: int, name: str, telegram_id: int = None) -> Workout:
    async with get_session() as session:
        stmt = select(Program).where(Program.id == program_id)
        if telegram_id:
            stmt = stmt.join(Program.owner).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        program = result.scalars().first()

        if not program:
            raise ValueError("Program not found")

        position = await session.scalar(
            select(func.coalesce(func.max(Workout.position), -1) + 1)
            .where(Workout.program_id == program_id)
        )
        workout = Workout(name=name, program=program, position=position)
        session.add(workout)
        await session.commit()
        await session.refresh(workout)

        return workout


async def reorder_workouts(
    program_id: int,
    workout_ids: list[int],
    telegram_id: int = None
) -> None:
    async with get_session() as session:
        stmt = (
            select(Workout)
            .where(Workout.program_id == program_id)
        )
        if telegram_id:
            stmt = (
                stmt.join(Workout.program)
                .join(Program.owner)
                .where(User.telegram_id == telegram_id)
            )

        workouts = list((await session.execute(stmt)).scalars().all())
        if len(workout_ids) != len(workouts) or set(workout_ids) != {workout.id for workout in workouts}:
            raise ValueError("Invalid workout order")

        workouts_by_id = {workout.id: workout for workout in workouts}
        for position, workout_id in enumerate(workout_ids):
            workouts_by_id[workout_id].position = position

        await session.commit()
    
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
        stmt = select(Workout).where(Workout.id == workout_id)
        if telegram_id:
            stmt = stmt.join(Workout.program).join(Program.owner).where(User.telegram_id == telegram_id)

        workout = (await session.execute(stmt)).scalars().first()
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
) -> Optional[Workout]:
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
