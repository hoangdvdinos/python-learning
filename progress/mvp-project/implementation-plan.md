# Implementation Plan — Personal Finance Tracker

> **Góc nhìn:** Senior backend developer triển khai từ A → Z
> **Nguyên tắc:** Mỗi bước chạy được, verify được trước khi sang bước tiếp theo
> **Không bao giờ** viết 5 file rồi mới chạy thử — viết 1 layer, chạy thử ngay

---

## Tư Duy Thứ Tự Triển Khai

```
Tại sao không viết Router trước?
→ Router cần Schema → Schema cần biết Model → Model cần Base → Base cần Config

Dependency graph (bottom-up):
Config → Database → Base → Models → Migration
                              ↓
                           Schemas → Exceptions
                              ↓
                          Repositories
                              ↓
                            Routers
                              ↓
                           main.py
```

Dev kinh nghiệm luôn đi **từ dưới lên** — layer dưới không phụ thuộc layer trên,
nên có thể verify từng layer độc lập.

---

## PHASE 1 — Khởi Tạo Project

### Bước 1.1 — Tạo project và cài dependencies

```bash
# Tạo thư mục project
mkdir finance-tracker && cd finance-tracker

# Khởi tạo project với uv
uv init .

# Cài production dependencies
uv add fastapi uvicorn[standard] sqlalchemy[asyncio] aiosqlite alembic pydantic-settings

# Cài dev dependencies
uv add --dev httpx pytest ruff

# Kiểm tra
uv run python -c "import fastapi, sqlalchemy, alembic; print('OK')"
```

**Verify:** Không có lỗi import là xong.

---

### Bước 1.2 — Tạo cấu trúc thư mục trống

```bash
mkdir -p app/core app/models app/schemas app/repositories app/routers

# Tạo __init__.py cho mỗi package
touch app/__init__.py
touch app/core/__init__.py
touch app/models/__init__.py
touch app/schemas/__init__.py
touch app/repositories/__init__.py
touch app/routers/__init__.py
```

**Lý do tạo `__init__.py`:** Python cần file này để nhận ra folder là package,
mới import được `from app.core.config import settings`.

---

### Bước 1.3 — Tạo file `.env` và `.env.example`

```bash
# .env — không commit lên git
DATABASE_URL=sqlite+aiosqlite:///./finance.db
ENV=development
APP_NAME=Finance Tracker API
APP_VERSION=1.0.0
```

```bash
# .env.example — commit lên git để teammate biết cần set gì
DATABASE_URL=sqlite+aiosqlite:///./finance.db
ENV=development
APP_NAME=Finance Tracker API
APP_VERSION=1.0.0
```

```bash
# .gitignore — thêm vào
.env
*.db
__pycache__/
.venv/
```

---

### Bước 1.4 — Viết `app/core/config.py`

**Viết trước tiên** vì mọi file khác đều cần `settings`.

```python
# app/core/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Finance Tracker API"
    APP_VERSION: str = "1.0.0"
    ENV: str = "development"
    DATABASE_URL: str = "sqlite+aiosqlite:///./finance.db"

    model_config = {"env_file": ".env"}


settings = Settings()
```

**Verify:**
```bash
uv run python -c "from app.core.config import settings; print(settings.DATABASE_URL)"
# Expected: sqlite+aiosqlite:///./finance.db
```

---

### Bước 1.5 — Viết `app/core/database.py`

```python
# app/core/database.py
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.ENV == "development",
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

**Verify:**
```bash
uv run python -c "from app.core.database import engine; print(engine.url)"
# Expected: sqlite+aiosqlite:///./finance.db
```

---

## PHASE 2 — Models & Migration

### Bước 2.1 — Viết `app/models/base.py`

**Viết trước Models** vì Category và Transaction đều kế thừa từ đây.

```python
# app/models/base.py
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, MappedColumn, mapped_column


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: MappedColumn[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: MappedColumn[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
```

---

### Bước 2.2 — Viết `app/models/category.py`

```python
# app/models/category.py
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Category(Base, TimestampMixin):
    __tablename__ = "categories"

    id:        Mapped[int]       = mapped_column(primary_key=True, autoincrement=True)
    name:      Mapped[str]       = mapped_column(String(100), nullable=False, unique=True)
    type:      Mapped[str]       = mapped_column(String(10), nullable=False)   # "income" | "expense"
    icon:      Mapped[str | None] = mapped_column(String(50), nullable=True)
    color:     Mapped[str | None] = mapped_column(String(7), nullable=True)
    is_active: Mapped[bool]      = mapped_column(Boolean, default=True, nullable=False)

    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="category"
    )

    def __repr__(self) -> str:
        return f"<Category id={self.id} name={self.name!r} type={self.type}>"
```

---

### Bước 2.3 — Viết `app/models/transaction.py`

```python
# app/models/transaction.py
from datetime import date, datetime

from sqlalchemy import Boolean, Date, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Transaction(Base, TimestampMixin):
    __tablename__ = "transactions"

    id:               Mapped[int]       = mapped_column(primary_key=True, autoincrement=True)
    category_id:      Mapped[int]       = mapped_column(ForeignKey("categories.id"), nullable=False)
    amount:           Mapped[float]     = mapped_column(Numeric(12, 2), nullable=False)
    type:             Mapped[str]       = mapped_column(String(10), nullable=False)
    note:             Mapped[str | None] = mapped_column(Text, nullable=True)
    transaction_date: Mapped[date]      = mapped_column(Date, nullable=False)
    is_deleted:       Mapped[bool]      = mapped_column(Boolean, default=False, nullable=False)

    category: Mapped["Category"] = relationship("Category", back_populates="transactions")

    def __repr__(self) -> str:
        return f"<Transaction id={self.id} amount={self.amount} type={self.type}>"
```

**Verify cả 2 models:**
```bash
uv run python -c "
from app.models.category import Category
from app.models.transaction import Transaction
print('Models OK:', Category.__tablename__, Transaction.__tablename__)
"
```

---

### Bước 2.4 — Cập nhật `app/models/__init__.py`

**Tại sao cần bước này?** Alembic cần import models để detect schema.
Import tập trung vào 1 chỗ — tránh quên khi thêm model mới.

```python
# app/models/__init__.py
from app.models.base import Base
from app.models.category import Category
from app.models.transaction import Transaction

__all__ = ["Base", "Category", "Transaction"]
```

---

### Bước 2.5 — Setup Alembic

```bash
# Khởi tạo alembic (chạy 1 lần)
uv run alembic init alembic
```

Chỉnh `alembic/env.py` — phần quan trọng nhất:

```python
# alembic/env.py — chỉ thay đổi các phần này, giữ nguyên phần còn lại

import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

# === THÊM 2 DÒNG NÀY ===
from app.models import Base          # import Base để lấy metadata
from app.core.config import settings  # import settings để lấy DATABASE_URL
# =======================

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata   # ← thay None thành Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,   # ← cần cho SQLite
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=True,   # ← cần cho SQLite
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = create_async_engine(settings.DATABASE_URL, poolclass=pool.NullPool)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

---

### Bước 2.6 — Tạo và chạy migration

```bash
# Tạo migration đầu tiên
uv run alembic revision --autogenerate -m "init categories and transactions"

# Xem file được tạo trong alembic/versions/ — đọc để verify đúng
# Phải thấy create_table("categories") và create_table("transactions")

# Chạy migration
uv run alembic upgrade head

# Verify DB đã có bảng
uv run python -c "
import asyncio
from sqlalchemy import text
from app.core.database import AsyncSessionLocal

async def check():
    async with AsyncSessionLocal() as db:
        result = await db.execute(text(\"SELECT name FROM sqlite_master WHERE type='table'\"))
        print('Tables:', [r[0] for r in result.fetchall()])

asyncio.run(check())
"
# Expected: Tables: ['alembic_version', 'categories', 'transactions']
```

---

## PHASE 3 — Schemas & Exceptions

### Bước 3.1 — Viết `app/core/exceptions.py`

**Viết exceptions trước schemas** vì repositories sẽ raise exceptions,
và repositories cần schemas — nên exceptions phải có trước.

```python
# app/core/exceptions.py
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class AppException(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code


class NotFoundException(AppException):
    def __init__(self, resource: str, resource_id: int | str):
        super().__init__(
            code="NOT_FOUND",
            message=f"{resource} với id={resource_id} không tồn tại",
            status_code=404,
        )


class BusinessException(AppException):
    def __init__(self, message: str):
        super().__init__(code="BUSINESS_ERROR", message=message, status_code=409)


# Handler functions — đăng ký vào app ở main.py
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "code": exc.code, "message": exc.message},
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors = [
        {
            "field": ".".join(str(x) for x in e["loc"][1:]),
            "message": e["msg"],
        }
        for e in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={"success": False, "code": "VALIDATION_ERROR", "errors": errors},
    )
```

---

### Bước 3.2 — Viết `app/schemas/category.py`

```python
# app/schemas/category.py
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    name:  str                           = Field(min_length=1, max_length=100)
    type:  Literal["income", "expense"]
    icon:  str | None                    = Field(default=None, max_length=50)
    color: str | None                    = Field(default=None, pattern=r"^#[0-9A-Fa-f]{6}$")


class CategoryUpdate(BaseModel):
    name:      str | None                        = Field(default=None, min_length=1, max_length=100)
    icon:      str | None                        = Field(default=None, max_length=50)
    color:     str | None                        = Field(default=None, pattern=r"^#[0-9A-Fa-f]{6}$")
    is_active: bool | None                       = None


class CategoryResponse(BaseModel):
    id:         int
    name:       str
    type:       str
    icon:       str | None
    color:      str | None
    is_active:  bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
```

---

### Bước 3.3 — Viết `app/schemas/transaction.py`

```python
# app/schemas/transaction.py
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class TransactionCreate(BaseModel):
    category_id:      int     = Field(gt=0)
    amount:           Decimal = Field(gt=0, decimal_places=2)
    note:             str | None = Field(default=None, max_length=500)
    transaction_date: date


class TransactionUpdate(BaseModel):
    category_id:      int | None     = Field(default=None, gt=0)
    amount:           Decimal | None = Field(default=None, gt=0)
    note:             str | None     = None
    transaction_date: date | None    = None


class TransactionResponse(BaseModel):
    id:               int
    category_id:      int
    category_name:    str
    amount:           Decimal
    type:             str
    note:             str | None
    transaction_date: date
    created_at:       datetime
    updated_at:       datetime

    model_config = {"from_attributes": True}


class TransactionListResponse(BaseModel):
    data:  list[TransactionResponse]
    total: int
    page:  int
    limit: int
```

---

### Bước 3.4 — Viết `app/schemas/report.py`

```python
# app/schemas/report.py
from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class SummaryResponse(BaseModel):
    from_date:     date
    to_date:       date
    total_income:  Decimal
    total_expense: Decimal
    balance:       Decimal


class MonthlyItem(BaseModel):
    year:    int
    month:   int
    income:  Decimal
    expense: Decimal
    balance: Decimal


class MonthlyResponse(BaseModel):
    data: list[MonthlyItem]


class ByCategoryItem(BaseModel):
    category_id:   int
    category_name: str
    type:          str
    total:         Decimal
    count:         int


class ByCategoryResponse(BaseModel):
    from_date: date
    to_date:   date
    data:      list[ByCategoryItem]
```

**Verify tất cả schemas:**
```bash
uv run python -c "
from app.schemas.category import CategoryCreate, CategoryResponse
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.schemas.report import SummaryResponse
print('Schemas OK')
"
```

---

## PHASE 4 — Repositories

> **Nguyên tắc:** Repository chỉ biết ORM và SQLAlchemy.
> Không biết FastAPI, không biết HTTP status code.
> Raise AppException — không raise HTTPException.

### Bước 4.1 — Viết `app/repositories/category_repo.py`

```python
# app/repositories/category_repo.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessException, NotFoundException
from app.models.category import Category
from app.models.transaction import Transaction
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, category_id: int) -> Category:
        category = await self.db.get(Category, category_id)
        if category is None or not category.is_active:
            raise NotFoundException("Category", category_id)
        return category

    async def list(
        self,
        type: str | None = None,
        is_active: bool = True,
    ) -> list[Category]:
        conditions = [Category.is_active == is_active]
        if type is not None:
            conditions.append(Category.type == type)

        from sqlalchemy import and_
        query = select(Category).where(and_(*conditions)).order_by(Category.name)
        rows = (await self.db.execute(query)).scalars().all()
        return list(rows)

    async def create(self, data: CategoryCreate) -> Category:
        category = Category(**data.model_dump())
        self.db.add(category)
        await self.db.flush()
        await self.db.refresh(category)
        return category

    async def update(self, category_id: int, data: CategoryUpdate) -> Category:
        category = await self.get_by_id(category_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(category, field, value)
        await self.db.flush()
        await self.db.refresh(category)
        return category

    async def soft_delete(self, category_id: int) -> None:
        # Không cho xóa nếu còn transaction active
        query = select(Transaction).where(
            Transaction.category_id == category_id,
            Transaction.is_deleted == False,
        ).limit(1)
        has_transactions = (await self.db.execute(query)).scalar_one_or_none()
        if has_transactions:
            raise BusinessException(
                f"Không thể xóa category đang có transaction. "
                f"Hãy xóa hoặc chuyển các transaction trước."
            )

        category = await self.get_by_id(category_id)
        category.is_active = False
```

---

### Bước 4.2 — Viết `app/repositories/transaction_repo.py`

```python
# app/repositories/transaction_repo.py
from datetime import date

from sqlalchemy import and_, func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException
from app.models.category import Category
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate


class TransactionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, transaction_id: int) -> Transaction:
        query = (
            select(Transaction)
            .options(selectinload(Transaction.category))
            .where(
                Transaction.id == transaction_id,
                Transaction.is_deleted == False,
            )
        )
        transaction = (await self.db.execute(query)).scalar_one_or_none()
        if transaction is None:
            raise NotFoundException("Transaction", transaction_id)
        return transaction

    async def list(
        self,
        page: int = 1,
        limit: int = 20,
        type: str | None = None,
        category_id: int | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> tuple[list[Transaction], int]:
        conditions = [Transaction.is_deleted == False]
        if type is not None:
            conditions.append(Transaction.type == type)
        if category_id is not None:
            conditions.append(Transaction.category_id == category_id)
        if from_date is not None:
            conditions.append(Transaction.transaction_date >= from_date)
        if to_date is not None:
            conditions.append(Transaction.transaction_date <= to_date)

        base_query = (
            select(Transaction)
            .options(selectinload(Transaction.category))
            .where(and_(*conditions))
        )

        total = (
            await self.db.execute(
                select(func.count()).select_from(
                    select(Transaction).where(and_(*conditions)).subquery()
                )
            )
        ).scalar_one()

        rows = (
            await self.db.execute(
                base_query
                .order_by(Transaction.transaction_date.desc(), Transaction.id.desc())
                .offset((page - 1) * limit)
                .limit(limit)
            )
        ).scalars().all()

        return list(rows), total

    async def create(self, data: TransactionCreate) -> Transaction:
        # Lấy type từ category
        category = await self.db.get(Category, data.category_id)
        if category is None or not category.is_active:
            raise NotFoundException("Category", data.category_id)

        transaction = Transaction(
            **data.model_dump(),
            type=category.type,
        )
        self.db.add(transaction)
        await self.db.flush()

        # Reload với category (để trả về category_name)
        return await self.get_by_id(transaction.id)

    async def update(self, transaction_id: int, data: TransactionUpdate) -> Transaction:
        transaction = await self.get_by_id(transaction_id)
        update_data = data.model_dump(exclude_unset=True)

        # Nếu đổi category → cập nhật lại type
        if "category_id" in update_data:
            category = await self.db.get(Category, update_data["category_id"])
            if category is None or not category.is_active:
                raise NotFoundException("Category", update_data["category_id"])
            update_data["type"] = category.type

        for field, value in update_data.items():
            setattr(transaction, field, value)

        await self.db.flush()
        return await self.get_by_id(transaction_id)

    async def soft_delete(self, transaction_id: int) -> None:
        transaction = await self.get_by_id(transaction_id)
        transaction.is_deleted = True
```

---

### Bước 4.3 — Viết `app/repositories/report_repo.py`

```python
# app/repositories/report_repo.py
from datetime import date
from decimal import Decimal

from sqlalchemy import and_, case, extract, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.models.transaction import Transaction
from app.schemas.report import (
    ByCategoryItem,
    ByCategoryResponse,
    MonthlyItem,
    MonthlyResponse,
    SummaryResponse,
)


class ReportRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_summary(self, from_date: date, to_date: date) -> SummaryResponse:
        query = (
            select(
                Transaction.type,
                func.coalesce(func.sum(Transaction.amount), 0).label("total"),
            )
            .where(
                and_(
                    Transaction.is_deleted == False,
                    Transaction.transaction_date >= from_date,
                    Transaction.transaction_date <= to_date,
                )
            )
            .group_by(Transaction.type)
        )
        rows = (await self.db.execute(query)).all()

        income  = Decimal("0")
        expense = Decimal("0")
        for row in rows:
            if row.type == "income":
                income = Decimal(str(row.total))
            elif row.type == "expense":
                expense = Decimal(str(row.total))

        return SummaryResponse(
            from_date=from_date,
            to_date=to_date,
            total_income=income,
            total_expense=expense,
            balance=income - expense,
        )

    async def get_monthly(self) -> MonthlyResponse:
        # 12 tháng gần nhất
        query = (
            select(
                extract("year",  Transaction.transaction_date).label("year"),
                extract("month", Transaction.transaction_date).label("month"),
                func.sum(
                    case((Transaction.type == "income", Transaction.amount), else_=0)
                ).label("income"),
                func.sum(
                    case((Transaction.type == "expense", Transaction.amount), else_=0)
                ).label("expense"),
            )
            .where(Transaction.is_deleted == False)
            .group_by("year", "month")
            .order_by("year", "month")
        )
        rows = (await self.db.execute(query)).all()

        items = [
            MonthlyItem(
                year=int(row.year),
                month=int(row.month),
                income=Decimal(str(row.income or 0)),
                expense=Decimal(str(row.expense or 0)),
                balance=Decimal(str(row.income or 0)) - Decimal(str(row.expense or 0)),
            )
            for row in rows
        ]
        return MonthlyResponse(data=items)

    async def get_by_category(
        self, from_date: date, to_date: date
    ) -> ByCategoryResponse:
        query = (
            select(
                Category.id.label("category_id"),
                Category.name.label("category_name"),
                Category.type,
                func.sum(Transaction.amount).label("total"),
                func.count(Transaction.id).label("count"),
            )
            .join(Transaction, Transaction.category_id == Category.id)
            .where(
                and_(
                    Transaction.is_deleted == False,
                    Transaction.transaction_date >= from_date,
                    Transaction.transaction_date <= to_date,
                )
            )
            .group_by(Category.id, Category.name, Category.type)
            .order_by(func.sum(Transaction.amount).desc())
        )
        rows = (await self.db.execute(query)).all()

        items = [
            ByCategoryItem(
                category_id=row.category_id,
                category_name=row.category_name,
                type=row.type,
                total=Decimal(str(row.total)),
                count=row.count,
            )
            for row in rows
        ]
        return ByCategoryResponse(from_date=from_date, to_date=to_date, data=items)
```

**Verify repositories (không cần DB thật):**
```bash
uv run python -c "
from app.repositories.category_repo import CategoryRepository
from app.repositories.transaction_repo import TransactionRepository
from app.repositories.report_repo import ReportRepository
print('Repositories OK')
"
```

---

## PHASE 5 — Routers

> **Nguyên tắc:** Router chỉ biết Schema và Repository.
> Không có SQL, không có business logic phức tạp.
> Mỗi endpoint = 1 action: validate → gọi repo → trả response.

### Bước 5.1 — Viết `app/routers/categories.py`

```python
# app/routers/categories.py
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.category_repo import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["Categories"])

DB   = Annotated[AsyncSession, Depends(get_db)]
Repo = Annotated[CategoryRepository, Depends(lambda db: CategoryRepository(db))]


@router.get("/", response_model=list[CategoryResponse])
async def list_categories(
    repo:      Repo,
    type:      str | None = Query(default=None, pattern="^(income|expense)$"),
    is_active: bool       = Query(default=True),
):
    return await repo.list(type=type, is_active=is_active)


@router.post("/", response_model=CategoryResponse, status_code=201)
async def create_category(data: CategoryCreate, repo: Repo):
    return await repo.create(data)


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, repo: Repo):
    return await repo.get_by_id(category_id)


@router.patch("/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: int, data: CategoryUpdate, repo: Repo):
    return await repo.update(category_id, data)


@router.delete("/{category_id}", status_code=204)
async def delete_category(category_id: int, repo: Repo):
    await repo.soft_delete(category_id)
```

---

### Bước 5.2 — Viết `app/routers/transactions.py`

```python
# app/routers/transactions.py
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.transaction_repo import TransactionRepository
from app.schemas.transaction import (
    TransactionCreate,
    TransactionListResponse,
    TransactionResponse,
    TransactionUpdate,
)

router = APIRouter(prefix="/transactions", tags=["Transactions"])

Repo = Annotated[TransactionRepository, Depends(lambda db: TransactionRepository(db))]

# Dependency dùng lại cho pagination
def get_db() -> AsyncSession:   # sẽ bị override bởi Depends ở dưới
    pass

from app.core.database import get_db as _get_db  # noqa: E402
DB = Annotated[AsyncSession, Depends(_get_db)]


def get_repo(db: DB) -> TransactionRepository:
    return TransactionRepository(db)

Repo = Annotated[TransactionRepository, Depends(get_repo)]


@router.get("/", response_model=TransactionListResponse)
async def list_transactions(
    repo:        Repo,
    page:        int          = Query(default=1, ge=1),
    limit:       int          = Query(default=20, ge=1, le=100),
    type:        str | None   = Query(default=None, pattern="^(income|expense)$"),
    category_id: int | None   = Query(default=None),
    from_date:   date | None  = Query(default=None),
    to_date:     date | None  = Query(default=None),
):
    transactions, total = await repo.list(
        page=page,
        limit=limit,
        type=type,
        category_id=category_id,
        from_date=from_date,
        to_date=to_date,
    )
    return TransactionListResponse(
        data=[
            TransactionResponse(
                **{
                    **t.__dict__,
                    "category_name": t.category.name,
                }
            )
            for t in transactions
        ],
        total=total,
        page=page,
        limit=limit,
    )


@router.post("/", response_model=TransactionResponse, status_code=201)
async def create_transaction(data: TransactionCreate, repo: Repo):
    transaction = await repo.create(data)
    return TransactionResponse(
        **{**transaction.__dict__, "category_name": transaction.category.name}
    )


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: int, repo: Repo):
    transaction = await repo.get_by_id(transaction_id)
    return TransactionResponse(
        **{**transaction.__dict__, "category_name": transaction.category.name}
    )


@router.patch("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(transaction_id: int, data: TransactionUpdate, repo: Repo):
    transaction = await repo.update(transaction_id, data)
    return TransactionResponse(
        **{**transaction.__dict__, "category_name": transaction.category.name}
    )


@router.delete("/{transaction_id}", status_code=204)
async def delete_transaction(transaction_id: int, repo: Repo):
    await repo.soft_delete(transaction_id)
```

---

### Bước 5.3 — Viết `app/routers/reports.py`

```python
# app/routers/reports.py
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.report_repo import ReportRepository
from app.schemas.report import ByCategoryResponse, MonthlyResponse, SummaryResponse

router = APIRouter(prefix="/reports", tags=["Reports"])

DB   = Annotated[AsyncSession, Depends(get_db)]
Repo = Annotated[ReportRepository, Depends(lambda db: ReportRepository(db))]


def get_repo(db: DB) -> ReportRepository:
    return ReportRepository(db)

Repo = Annotated[ReportRepository, Depends(get_repo)]


@router.get("/summary", response_model=SummaryResponse)
async def get_summary(
    repo:      Repo,
    from_date: date = Query(..., description="YYYY-MM-DD"),
    to_date:   date = Query(..., description="YYYY-MM-DD"),
):
    return await repo.get_summary(from_date, to_date)


@router.get("/monthly", response_model=MonthlyResponse)
async def get_monthly(repo: Repo):
    return await repo.get_monthly()


@router.get("/by-category", response_model=ByCategoryResponse)
async def get_by_category(
    repo:      Repo,
    from_date: date = Query(..., description="YYYY-MM-DD"),
    to_date:   date = Query(..., description="YYYY-MM-DD"),
):
    return await repo.get_by_category(from_date, to_date)
```

---

## PHASE 6 — main.py & Chạy Server

### Bước 6.1 — Viết `main.py`

**File cuối cùng** — wire tất cả lại với nhau.

```python
# main.py
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine
from app.core.exceptions import (
    AppException,
    app_exception_handler,
    validation_exception_handler,
)
from app.routers import categories, reports, transactions


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# --- Middleware ---
@app.middleware("http")
async def log_requests(request: Request, call_next):
    rid   = str(uuid.uuid4())[:8]
    start = time.time()
    response = await call_next(request)
    ms = (time.time() - start) * 1000
    response.headers["X-Request-Id"]   = rid
    response.headers["X-Process-Time"] = f"{ms:.1f}ms"
    if settings.ENV == "development":
        print(f"[{rid}] {request.method} {request.url.path} → {response.status_code} ({ms:.0f}ms)")
    return response

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Exception Handlers ---
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# --- Routers ---
app.include_router(categories.router)
app.include_router(transactions.router)
app.include_router(reports.router)


@app.get("/health", tags=["System"])
async def health():
    return {"status": "ok", "version": settings.APP_VERSION}
```

---

### Bước 6.2 — Cập nhật `app/routers/__init__.py`

```python
# app/routers/__init__.py
from app.routers import categories, reports, transactions

__all__ = ["categories", "transactions", "reports"]
```

---

### Bước 6.3 — Chạy và verify

```bash
# Chạy server
uv run uvicorn main:app --reload

# Mở browser: http://localhost:8000/docs
# Swagger UI hiện đầy đủ 13 endpoint là thành công
```

---

## PHASE 7 — Seed Data & Smoke Test

### Bước 7.1 — Viết `seed.py`

```python
# seed.py — chạy 1 lần để có data test
import asyncio
from app.core.database import AsyncSessionLocal
from app.models.category import Category
from app.models.transaction import Transaction
from datetime import date

CATEGORIES = [
    {"name": "Lương",     "type": "income",  "icon": "💼", "color": "#4CAF50"},
    {"name": "Thưởng",    "type": "income",  "icon": "🎁", "color": "#8BC34A"},
    {"name": "Ăn uống",   "type": "expense", "icon": "🍜", "color": "#FF5722"},
    {"name": "Di chuyển", "type": "expense", "icon": "🚗", "color": "#FF9800"},
    {"name": "Mua sắm",   "type": "expense", "icon": "🛍️", "color": "#E91E63"},
    {"name": "Nhà ở",     "type": "expense", "icon": "🏠", "color": "#795548"},
]

async def seed():
    async with AsyncSessionLocal() as db:
        # Insert categories
        categories = []
        for data in CATEGORIES:
            cat = Category(**data)
            db.add(cat)
            categories.append(cat)
        await db.flush()

        # Insert sample transactions
        transactions = [
            Transaction(category_id=categories[0].id, amount=15_000_000, type="income",
                       note="Lương tháng 5", transaction_date=date(2026, 5, 1)),
            Transaction(category_id=categories[2].id, amount=85_000,     type="expense",
                       note="Bún bò buổi trưa", transaction_date=date(2026, 5, 31)),
            Transaction(category_id=categories[2].id, amount=120_000,    type="expense",
                       note="Cà phê + bánh mì", transaction_date=date(2026, 5, 30)),
            Transaction(category_id=categories[3].id, amount=200_000,    type="expense",
                       note="Xăng xe tuần này", transaction_date=date(2026, 5, 29)),
            Transaction(category_id=categories[4].id, amount=850_000,    type="expense",
                       note="Áo mới",  transaction_date=date(2026, 5, 28)),
        ]
        for t in transactions:
            db.add(t)

        await db.commit()
        print(f"Seeded {len(CATEGORIES)} categories + {len(transactions)} transactions")

asyncio.run(seed())
```

```bash
uv run python seed.py
```

---

### Bước 7.2 — Smoke test thủ công trên Swagger

Thứ tự test theo dependency:

```
1. GET  /health                          → {"status": "ok"}
2. GET  /categories                      → danh sách categories
3. POST /categories                      → tạo category mới
4. GET  /categories/{id}                 → xem chi tiết
5. PATCH /categories/{id}               → cập nhật icon
6. POST /transactions                    → tạo transaction
7. GET  /transactions                    → có filter + pagination
8. GET  /transactions?type=expense       → chỉ expense
9. GET  /transactions?from_date=2026-05-01&to_date=2026-05-31
10. PATCH /transactions/{id}            → đổi amount
11. DELETE /transactions/{id}           → soft delete
12. GET  /reports/summary?from_date=2026-05-01&to_date=2026-05-31
13. GET  /reports/monthly
14. GET  /reports/by-category?from_date=2026-05-01&to_date=2026-05-31
15. DELETE /categories/{id có transaction} → phải báo lỗi 409
16. POST /transactions với category_id=999 → phải báo lỗi 404
```

---

## Tóm Tắt Thứ Tự Tệp Cần Tạo

```
01  .env, .env.example, .gitignore
02  app/core/config.py
03  app/core/database.py
04  app/models/base.py
05  app/models/category.py
06  app/models/transaction.py
07  app/models/__init__.py
08  alembic/env.py  (chỉnh sửa)
09  [chạy: alembic revision --autogenerate + upgrade head]
10  app/core/exceptions.py
11  app/schemas/category.py
12  app/schemas/transaction.py
13  app/schemas/report.py
14  app/repositories/category_repo.py
15  app/repositories/transaction_repo.py
16  app/repositories/report_repo.py
17  app/routers/categories.py
18  app/routers/transactions.py
19  app/routers/reports.py
20  app/routers/__init__.py
21  main.py
22  [chạy server, verify /docs]
23  seed.py
24  [smoke test 16 cases]
```

> **Quy tắc vàng:** Mỗi file xong → chạy `uv run python -c "from ... import ..."` verify import được.
> Không để lỗi import tích lũy — phát hiện sớm, fix ngay.
