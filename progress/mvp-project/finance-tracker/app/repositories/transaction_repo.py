from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException
from app.models.transaction import Transaction
from app.repositories.category_repo import CategoryRepository
from app.schemas.transaction import TransactionCreate, TransactionUpdate


class TransactionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self._category_repo = CategoryRepository(session)

    async def get_all(
        self,
        type: str | None = None,
        category_id: int | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        page: int = 1,
        size: int = 20,
    ) -> list[Transaction]:
        filters = [Transaction.is_deleted == False]  # noqa: E712
        if type:
            filters.append(Transaction.type == type)
        if category_id:
            filters.append(Transaction.category_id == category_id)
        if date_from:
            filters.append(Transaction.transaction_date >= date_from)
        if date_to:
            filters.append(Transaction.transaction_date <= date_to)

        stmt = (
            select(Transaction)
            .where(*filters)
            .options(selectinload(Transaction.category))
            .order_by(Transaction.transaction_date.desc())
            .offset((page - 1) * size)
            .limit(size)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, transaction_id: int) -> Transaction:
        stmt = (
            select(Transaction)
            .where(
                Transaction.id == transaction_id,
                Transaction.is_deleted == False,  # noqa: E712
            )
            .options(selectinload(Transaction.category))
        )
        result = await self.session.execute(stmt)
        transaction = result.scalar_one_or_none()
        if transaction is None:
            raise NotFoundException("Transaction", transaction_id)
        return transaction

    async def create(self, data: TransactionCreate) -> Transaction:
        # Derive type from category — client does not send type directly
        category = await self._category_repo.get_by_id(data.category_id)
        transaction = Transaction(
            **data.model_dump(),
            type=category.type,
        )
        self.session.add(transaction)
        await self.session.flush()
        await self.session.refresh(transaction)
        return transaction

    async def update(self, transaction_id: int, data: TransactionUpdate) -> Transaction:
        transaction = await self.get_by_id(transaction_id)
        updates = data.model_dump(exclude_unset=True)

        # Re-derive type if category changes
        if "category_id" in updates:
            category = await self._category_repo.get_by_id(updates["category_id"])
            updates["type"] = category.type

        for field, value in updates.items():
            setattr(transaction, field, value)

        await self.session.flush()
        await self.session.refresh(transaction)
        return transaction

    async def delete(self, transaction_id: int) -> None:
        transaction = await self.get_by_id(transaction_id)
        transaction.is_deleted = True
        await self.session.flush()
