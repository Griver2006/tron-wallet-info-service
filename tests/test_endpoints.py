import pytest
from unittest.mock import patch


@pytest.mark.asyncio
@pytest.mark.usefixtures("override_get_session")
async def test_post_wallets(client):
    mock_data = {
        "address": "TMockAddress",
        "balance": 123.45,
        "bandwidth": 1000,
        "energy": 500
    }

    with patch("app.tron_client.get_wallet_info", return_value=mock_data):
        response = await client.post(
            "/wallets", json={"address": mock_data["address"]}
        )
        assert response.status_code == 200
        result = response.json()
        assert result["address"] == mock_data["address"]
        assert result["balance"] == mock_data["balance"]
        assert result["bandwidth"] == mock_data["bandwidth"]
        assert result["energy"] == mock_data["energy"]


@pytest.mark.asyncio
@pytest.mark.usefixtures("override_get_session")
async def test_get_wallets(client):
    response = await client.get("/wallets")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
