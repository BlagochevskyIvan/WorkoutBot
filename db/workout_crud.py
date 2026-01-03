from db.database import get_session
from db.models import Program, Workout
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def create_workout(id: int, name: str) -> Workout:
    async with get_session() as session:
        stmt = select(Program).where(Program.id == id)
        result = await session.execute(stmt)
        program = result.scalars().first()

        if not program:
            raise ValueError("Program not found")

        workout = Workout(name=name, program=program)
        session.add(workout)
        await session.commit()
        await session.refresh(workout)

        return workout
    
async def get_workouts(id: int) -> list[Workout]:
    async with get_session() as session:
        stmt = (
            select(Program)
            .where(Program.id==id)
            .options(selectinload(Program.workouts))
        )

        result = await session.execute(stmt)
        program = result.scalars().first()

        if not program:
            return []

        return program.workouts
    
async def delete_workout(workout_id: int) -> None:
    async with get_session() as session:
        workout = (
            await session.execute(
                select(Workout).where(Workout.id == workout_id)
            )
        ).scalars().first()

        if not workout:
            return

        await session.delete(workout)
        await session.commit()