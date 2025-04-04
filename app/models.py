from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class WalletRequest(Base):
    """
    Модель данных для хранения информации о кошельках в базе данных.

    Включает:
    - `address`: Адрес кошелька.
    - `balance`: Баланс кошелька в TRX.
    - `bandwidth`: Ресурсы сети для транзакций.
    - `energy`: Энергия для выполнения смарт-контрактов.
    - `timestamp`: Время создания записи о кошельке.
    """
    __tablename__ = 'wallet_queries'

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str]
    balance: Mapped[float]
    bandwidth: Mapped[int]
    energy: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
