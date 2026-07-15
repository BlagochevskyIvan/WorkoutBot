from db.database import get_session
from db.models import User, Params
from sqlalchemy import select, update
from typing import Optional

# Создание пользователя
async def create_user(telegram_id: int, username: str) -> User:
    """Создает нового пользователя"""
    async with get_session() as session:
        user = User(telegram_id=telegram_id, username=username)
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user

async def get_user_crud(telegram_id: int) -> Optional[User]:
    """Получает пользователя по telegram_id"""
    async with get_session() as session:
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        return result.scalars().first()
    
async def add_gender(telegram_id: int, gender) -> None:
    """Добавляет пол пользователя"""
    async with get_session() as session:
        await session.execute(
            update(User)
            .values(gender=gender)
            .where(User.telegram_id == telegram_id)
        )
        await session.commit()

async def add_params(
    telegram_id: int,
    weight: float,
    height: float,
    body_fat_percentage: float,
) -> None:
    """Добавляет параметры и завершает регистрацию пользователя"""
    async with get_session() as session:
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        user = result.scalars().first()

        if not user:
            return

        params = Params(
            user_id=user.id,
            weight=weight,
            height=height,
            body_fat_percentage=body_fat_percentage,
        )
        session.add(params)
        user.is_registered = True
        await session.commit()

async def get_last_params(telegram_id: int) -> Optional[Params]:
    """Получает последние параметры пользователя"""
    async with get_session() as session:
        stmt = (
            select(Params)
            .join(User, Params.user_id == User.id)
            .where(User.telegram_id == telegram_id)
            .order_by(Params.id.desc())
        )
        result = await session.execute(stmt)
        return result.scalars().first()

async def add_expirience(telegram_id: int, experience):
    """добавляет опыт пользователя"""
    async with get_session() as session:
        await session.execute(
            update(User)
            .values(experience = experience)
            .where(User.telegram_id == telegram_id)
        )
        await session.commit()

async def add_birth_date(telegram_id: int, birth_date):
    """Добавляет дату рождения пользователя"""
    async with get_session() as session:
        await session.execute(
            update(User)
            .values(birth_date = birth_date)
            .where(User.telegram_id == telegram_id)
        )
        await session.commit()

async def add_place(telegram_id: int, place):
    """Добавляет место тренировок пользователя"""
    async with get_session() as session:
        await session.execute(
            update(User)
            .values(place = place)
            .where(User.telegram_id == telegram_id)
        )
        await session.commit()

async def get_all_users() -> list[User]:
    """Получает всех пользователей"""
    async with get_session() as session:
        stmt = select(User)
        result = await session.execute(stmt)
        return result.scalars().all()
