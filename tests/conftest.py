import pytest_asyncio

from httpx import AsyncClient, ASGITransport

from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.db import new_session, engine, Base


# Поднимаем и очищаем базу перед сессией
@pytest_asyncio.fixture(scope='session', autouse=True)
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# Фикстура для сессии
@pytest_asyncio.fixture
async def session() -> AsyncSession:
    async with new_session() as s:
        yield s


# Фикстура клиента FastAPI
@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as ac:
        yield ac
