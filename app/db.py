from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

# Создаём асинхронный движок для работы с базой данных SQLite
engine = create_async_engine('sqlite+aiosqlite:///wallets.db')

# Создаём сессию для работы с базой данных
new_session = async_sessionmaker(engine, expire_on_commit=False)


# Базовый класс для моделей SQLAlchemy
class Base(DeclarativeBase):
    pass
