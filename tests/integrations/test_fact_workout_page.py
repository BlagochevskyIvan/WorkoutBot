import pytest
import pytest_asyncio

from db.database import engine, AsyncSessionLocal
from db.models import Base
from handlers.history import get_fact_workouts_page
from handlers.history import HISTORY_PAGE_SIZE
from db.models import User, Program, Workout, Exercise, Set, FactWorkout
from sqlalchemy import delete

@pytest_asyncio.fixture
async def session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as db:
        await db.execute(delete(FactWorkout))
        await db.execute(delete(Workout))
        await db.execute(delete(Program))
        await db.execute(delete(User))
        await db.commit()
        yield db
    await engine.dispose() 


async def seed(db, telegram_id, count, name):
    user = User(telegram_id=telegram_id)
    db.add(user)
    await db.flush()
    program = Program(name=name, owner=user)
    db.add(program)
    await db.flush()
    workout = Workout(name=name, program=program)
    db.add(workout)
    await db.flush()
    for i in range(count):
        fact_workout = FactWorkout(user_id=user.id, workout=workout, name=name)
        db.add(fact_workout)
    await db.commit()

async def seed2(db, telegram_id, count, name):
    user = User(telegram_id=telegram_id)
    db.add(user)
    await db.flush()
    program = Program(name=name, owner=user)
    db.add(program)
    await db.flush()
    workout = Workout(name=name, program=program)
    db.add(workout)
    await db.flush()
    fw1 = FactWorkout(user_id=user.id, workout=workout, name=name, created_at="")

@pytest.mark.asyncio
async def test_first_page_is_seven(session):
    await seed(session, telegram_id=123, count=20, name="Test Fact Workout")
    await seed(session, telegram_id=456, count=1, name="Test Fact Workout 2")
    
    items, total = await get_fact_workouts_page(telegram_id=123, page=1, page_size=HISTORY_PAGE_SIZE)

    assert len(items) == HISTORY_PAGE_SIZE
    assert total == 20
    assert all(item.name == "Test Fact Workout" for item in items)

@pytest.mark.asyncio
async def test_last_page_test(session):
    await seed(session, telegram_id=124, count=20, name="Test Fact Workout")
    items, total = await get_fact_workouts_page(telegram_id=124, page=3, page_size=HISTORY_PAGE_SIZE)
    assert len(items) == 6
    assert total == 20

@pytest.mark.asyncio
async def test_user_without_workouts(session):
    await seed(session, telegram_id=25, count=0, name="fw")
    items, total = await get_fact_workouts_page(telegram_id=25, page=1, page_size=HISTORY_PAGE_SIZE)
    assert len(items) == 0
    assert total == 0

