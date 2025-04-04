from fastapi import APIRouter, HTTPException

from tronpy.exceptions import BadAddress

from app import crud, schemas, tron_client, db


router = APIRouter()


@router.post(
    '/setup_datebase',
    summary='Создать/Пересоздать бд',
)
async def setup_datebase():
    """
    (Функция только для отладки)

    Удаляет все таблицы в базе данных и создаёт их заново.
    Используется для инициализации базы данных в процессе разработки и тестирования.
    """
    async with db.engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.drop_all)  # Удаляем все таблицы
        await conn.run_sync(db.Base.metadata.create_all)  # Создаём новые таблицы

    return {'ok': True}


@router.post(
    '/wallets',
    tags=['Кошельки'],
    summary='Получить данные с кошелька'
)
async def fetch_wallet_data(wallet: schemas.WalletRequestCreate, session: crud.SessionDep):
    """
    Добавляет информацию о кошельке в базу данных.

    Принимает:
    - `data`: Схема с адресом кошелька.

    Запрашивает информацию о кошельке (баланс, ресурсы и энергия) через Tron API.
    Если адрес некорректен, возвращает ошибку. В случае успешного запроса добавляет
    данные в базу и возвращает их в ответ.
    """
    try:
        data = tron_client.get_wallet_info(wallet.address)
        return await crud.create_wallet_request(session, data)
    except BadAddress:
        raise HTTPException(status_code=400, detail='Некорректный адрес кошелька')


@router.get(
    '/wallets',
    tags=['Кошельки'],
    summary='Получить данные с уже запрошенных кошельков',
    response_model=list[schemas.WalletRequestResponse]
)
async def get_wallets(session: crud.SessionDep, skip: int = 0, limit: int = 10):
    """
    Получает все записи о кошельках из базы данных.

    Использует пагинацию для более эффективного запроса (в случае необходимости,
    можно добавить параметры пагинации).
    """
    return await crud.get_wallet_requests(session, skip, limit)
