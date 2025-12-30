async def get_all_workouts() -> list[Workout]:
    """Получает все тренировки"""
    async with get_session() as session:
        stmt = select(Workout)
        result = await session.execute(stmt)
        return result.scalars().all()