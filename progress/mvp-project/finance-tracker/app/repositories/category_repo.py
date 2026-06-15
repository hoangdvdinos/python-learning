from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessException, NotFoundException
from app.models.category import Category
from app.models.transaction import Transaction
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self, type: str | None = None) -> list[Category]:
        filters = [Category.is_deleted == False]  # noqa: E712 -> binary expression for better query performance
        if type:
            filters.append(Category.type == type)
        stmt = select(Category).where(*filters)
        result = await self.session.execute(stmt)
        return list(result.scalars().all()) # return as list for easier JSON serialization, example: [Category(id=1, name="Food", type="expense", is_deleted=False), ...]

    async def get_by_id(self, category_id: int) -> Category:
        stmt = select(Category).where(
            Category.id == category_id,
            Category.is_deleted == False,  # noqa: E712
        )
        result = await self.session.execute(stmt)
        category = result.scalar_one_or_none()
        if category is None:
            raise NotFoundException("Category", category_id)
        return category

    async def create(self, data: CategoryCreate) -> Category:
        category = Category(**data.model_dump())
        self.session.add(category)
        await self.session.flush() # create auto-generated ID and other defaults before refresh, not commit yet to allow transaction rollback if needed
        await self.session.refresh(category) # return complete category with all fields populated (e.g. id, created_at)
        return category

    async def update(self, category_id: int, data: CategoryUpdate) -> Category:
        category = await self.get_by_id(category_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(category, field, value) # assign values for object
        await self.session.flush() 
        await self.session.refresh(category)
        return category

    async def delete(self, category_id: int) -> None:
        category = await self.get_by_id(category_id)

        # Soft delete guard: block if active transactions exist
        # Đếm xem bao nhiêu giao dịch chưa bị xóa liên quan đến category này, nếu có thì không cho xóa category
        stmt = select(func.count(Transaction.id)).where(
            Transaction.category_id == category_id,
            Transaction.is_deleted == False,  # noqa: E712
        )
        count = await self.session.scalar(stmt)
        if count and count > 0:
            raise BusinessException(
                f"Cannot delete category with {count} active transaction(s). "
                "Delete or reassign transactions first."
            )

        category.is_deleted = True
        await self.session.flush()
