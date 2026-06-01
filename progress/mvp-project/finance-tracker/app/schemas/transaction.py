from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.category import CategoryResponse


class TransactionCreate(BaseModel):
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    description: str | None = Field(default=None)
    transaction_date: date
    category_id: int


class TransactionUpdate(BaseModel):
    amount: Decimal | None = Field(default=None, gt=0, decimal_places=2)
    description: str | None = None
    transaction_date: date | None = None
    category_id: int | None = None


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    amount: Decimal
    type: str
    description: str | None
    transaction_date: date
    category_id: int
    category: CategoryResponse
