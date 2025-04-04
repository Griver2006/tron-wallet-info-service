from httpx import AsyncClient, ASGITransport

import pytest_asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.db import Base
from app.main import app
from app.crud import get_session as original_get_session


@pytest_asyncio.fixture(scope='session')
async def test_engine():
    """
    Создаём отдельный движок для тестов на базе in-memory SQLite.
    """
    engine = create_async_engine('sqlite+aiosqlite:///:memory:')
    async with engine.begin() as conn:
        # создаём все таблицы в памяти
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    # по завершении тестов (если нужно) удалим таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def session(test_engine):
    """
    Создаём отдельную сессию для каждого теста (автоматически откатываем транзакции).
    """
    test_session = async_sessionmaker(test_engine, expire_on_commit=False)
    async with test_session() as s:
        yield s


@pytest_asyncio.fixture
def override_get_session(session):
    """
    Переопределяем зависимость get_session так, чтобы она возвращала нашу тестовую сессию.
    """
    async def _get_session_override():
        yield session
    app.dependency_overrides[original_get_session] = _get_session_override
    yield
    # После тестов снимаем нашу переопределённую зависимость
    app.dependency_overrides.pop(original_get_session, None)


# Фикстура клиента FastAPI
@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as ac:
        yield ac
