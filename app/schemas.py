from pydantic import BaseModel
from datetime import datetime


class WalletRequestCreate(BaseModel):
    address: str


class WalletRequestResponse(BaseModel):
    id: int
    address: str
    bandwidth: int
    energy: int
    balance: float
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
