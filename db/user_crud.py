from db.database import get_session
from db.models import User
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

async def get_user(telegram_id: int) -> Optional[User]:
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
    
