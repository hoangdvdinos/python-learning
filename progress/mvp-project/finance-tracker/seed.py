"""Seed script — tạo dữ liệu mẫu cho finance-tracker."""

import asyncio
import sys

# Windows console mặc định dùng cp1252, không encode được emoji → force UTF-8
sys.stdout.reconfigure(encoding="utf-8")
from datetime import date
from decimal import Decimal

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = "sqlite+aiosqlite:///./finance.db"

engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def seed() -> None:
    async with SessionLocal() as session:
        # Clear existing data
        await session.execute(text("DELETE FROM transactions"))
        await session.execute(text("DELETE FROM categories"))
        await session.commit()

    # Re-import after clear so models are clean
    from app.repositories.category_repo import CategoryRepository
    from app.repositories.transaction_repo import TransactionRepository
    from app.schemas.category import CategoryCreate
    from app.schemas.transaction import TransactionCreate

    async with SessionLocal() as session:
        cat_repo = CategoryRepository(session)
        tx_repo = TransactionRepository(session)

        # --- Categories ---
        categories_data = [
            CategoryCreate(name="Lương", type="income", icon="💰", color="#4CAF50"),
            CategoryCreate(name="Freelance", type="income", icon="💻", color="#2196F3"),
            CategoryCreate(name="Ăn uống", type="expense", icon="🍜", color="#FF5722"),
            CategoryCreate(name="Di chuyển", type="expense", icon="🚗", color="#FF9800"),
            CategoryCreate(name="Giải trí", type="expense", icon="🎮", color="#9C27B0"),
            CategoryCreate(name="Tiết kiệm", type="expense", icon="🏦", color="#607D8B"),
        ]
        cats = []
        for data in categories_data:
            cat = await cat_repo.create(data)
            cats.append(cat)
            print(f"  Created category: [{cat.id}] {cat.name} ({cat.type})")
        await session.commit()

        # --- Transactions ---
        transactions_data = [
            TransactionCreate(amount=Decimal("15000000"), description="Lương tháng 5", transaction_date=date(2026, 5, 1), category_id=cats[0].id),
            TransactionCreate(amount=Decimal("5000000"), description="Dự án web", transaction_date=date(2026, 5, 10), category_id=cats[1].id),
            TransactionCreate(amount=Decimal("1200000"), description="Ăn uống cả tháng", transaction_date=date(2026, 5, 31), category_id=cats[2].id),
            TransactionCreate(amount=Decimal("500000"), description="Grab xe máy", transaction_date=date(2026, 5, 15), category_id=cats[3].id),
            TransactionCreate(amount=Decimal("300000"), description="Netflix + Spotify", transaction_date=date(2026, 5, 5), category_id=cats[4].id),
            TransactionCreate(amount=Decimal("2000000"), description="Tiết kiệm tháng 5", transaction_date=date(2026, 5, 31), category_id=cats[5].id),
            TransactionCreate(amount=Decimal("15000000"), description="Lương tháng 6", transaction_date=date(2026, 6, 1), category_id=cats[0].id),
            TransactionCreate(amount=Decimal("800000"), description="Ăn ngoài", transaction_date=date(2026, 6, 2), category_id=cats[2].id),
        ]
        for data in transactions_data:
            tx = await tx_repo.create(data)
            print(f"  Created transaction: [{tx.id}] {tx.description} — {tx.amount:,} ({tx.type})")
        await session.commit()

    print("\nSeed completed.")


if __name__ == "__main__":
    asyncio.run(seed())
