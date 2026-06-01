from decimal import Decimal

from pydantic import BaseModel


class SummaryResponse(BaseModel):
    total_income: Decimal
    total_expense: Decimal
    balance: Decimal


class MonthlyItem(BaseModel):
    year: int
    month: int
    total_income: Decimal
    total_expense: Decimal
    balance: Decimal


class MonthlyResponse(BaseModel):
    items: list[MonthlyItem]


class ByCategoryItem(BaseModel):
    category_id: int
    category_name: str
    type: str
    total: Decimal


class ByCategoryResponse(BaseModel):
    items: list[ByCategoryItem]
