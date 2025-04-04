import pytest
from app import crud


@pytest.mark.asyncio
@pytest.mark.usefixtures("override_get_session")
async def test_create_wallet_request(session):
    data = {
        "address": "TXYZ1234567890",
        "balance": 100.0,
        "bandwidth": 500,
        "energy": 2000
    }

    record = await crud.create_wallet_request(session, data)

    assert record.id is not None
    assert record.address == data["address"]
    assert record.balance == data["balance"]
    assert record.bandwidth == data["bandwidth"]
    assert record.energy == data["energy"]
