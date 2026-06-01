from decimal import Decimal

from sqlalchemy import case, extract, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import Transaction
from app.schemas.report import (
    ByCategoryItem,
    ByCategoryResponse,
    MonthlyItem,
    MonthlyResponse,
    SummaryResponse,
)


class ReportRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_summary(self) -> SummaryResponse:
        income_col = func.sum(
            case((Transaction.type == "income", Transaction.amount), else_=0)
        )
        expense_col = func.sum(
            case((Transaction.type == "expense", Transaction.amount), else_=0)
        )
        stmt = select(income_col, expense_col).where(
            Transaction.is_deleted == False  # noqa: E712
        )
        result = await self.session.execute(stmt)
        row = result.one()
        total_income = Decimal(row[0] or 0)
        total_expense = Decimal(row[1] or 0)
        return SummaryResponse(
            total_income=total_income,
            total_expense=total_expense,
            balance=total_income - total_expense,
        )

    async def get_monthly(self) -> MonthlyResponse:
        year_col = extract("year", Transaction.transaction_date).label("year")
        month_col = extract("month", Transaction.transaction_date).label("month")
        income_col = func.sum(
            case((Transaction.type == "income", Transaction.amount), else_=0)
        ).label("total_income")
        expense_col = func.sum(
            case((Transaction.type == "expense", Transaction.amount), else_=0)
        ).label("total_expense")

        stmt = (
            select(year_col, month_col, income_col, expense_col)
            .where(Transaction.is_deleted == False)  # noqa: E712
            .group_by(year_col, month_col)
            .order_by(year_col.desc(), month_col.desc())
        )
        result = await self.session.execute(stmt)
        items = [
            MonthlyItem(
                year=int(row.year),
                month=int(row.month),
                total_income=Decimal(row.total_income or 0),
                total_expense=Decimal(row.total_expense or 0),
                balance=Decimal(row.total_income or 0) - Decimal(row.total_expense or 0),
            )
            for row in result
        ]
        return MonthlyResponse(items=items)

    async def get_by_category(self) -> ByCategoryResponse:
        from app.models.category import Category

        stmt = (
            select(
                Transaction.category_id,
                Category.name.label("category_name"),
                Category.type.label("type"),
                func.sum(Transaction.amount).label("total"),
            )
            .join(Category, Transaction.category_id == Category.id)
            .where(Transaction.is_deleted == False)  # noqa: E712
            .group_by(Transaction.category_id, Category.name, Category.type)
            .order_by(func.sum(Transaction.amount).desc())
        )
        result = await self.session.execute(stmt)
        items = [
            ByCategoryItem(
                category_id=row.category_id,
                category_name=row.category_name,
                type=row.type,
                total=Decimal(row.total or 0),
            )
            for row in result
        ]
        return ByCategoryResponse(items=items)
