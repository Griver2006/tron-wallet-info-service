from typing import Annotated

from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, db


async def get_session():
    """
    Функция для открытия и закрытия сессии базы данных.

    Используется как зависимость в FastAPI, чтобы гарантировать, что сессия
    будет закрыта после выполнения запроса.
    """
    async with db.new_session() as session:
        yield session


# Аннотация для использования сессии в маршрутах
SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def create_wallet_request(session: SessionDep, data: dict):
    db_request = models.WalletRequest(**data)
    session.add(db_request)
    await session.commit()

    return db_request


async def get_wallet_requests(session: SessionDep, skip: int = 0, limit: int = 10):
    result = await session.execute(
        select(models.WalletRequest).offset(skip).limit(limit)
    )
    return result.scalars().all()
