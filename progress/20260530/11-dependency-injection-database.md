# 11 — Dependency Injection & Database

> **Khối 11 — Dependency Injection & Database**
> Dành cho Java developer — tập trung vào điểm khác biệt so với Spring Boot.

---

## A — Dependency Injection trong FastAPI

### A.1 WHAT — DI là gì?

- **Dependency Injection** = cơ chế FastAPI tự động "tiêm" dependency vào endpoint/function khi request đến
- Dùng `Depends()` để khai báo — FastAPI lo việc khởi tạo, truyền vào, và cleanup
- Dependency có thể là: validate token, lấy DB session, đọc config, parse query params tái sử dụng...

### A.2 WHY — Tại sao cần DI?

- Tránh lặp code: logic auth, DB session không cần viết lại ở mỗi endpoint
- Testable: thay thế dependency bằng mock khi test dễ dàng
- Tự cleanup: dependency dùng `yield` tự động cleanup (đóng DB session, release resource)
- Composable: dependency gọi dependency khác (nested)

### A.3 ⚠️ Java vs FastAPI

| Spring Boot | FastAPI |
|-------------|---------|
| `@Autowired` field injection | `param: Type = Depends(get_dep)` |
| `@Bean` trong `@Configuration` | Hàm Python thường, decorate với `Depends()` |
| `@Component`, `@Service` | Hàm trả về value — không cần annotation |
| `ApplicationContext` quản lý scope | FastAPI tự quản lý: per-request hoặc singleton |
| `@Scope("prototype")` | Mặc định của `Depends()` — tạo mới mỗi request |
| `@Scope("singleton")` | `Depends(func, use_cache=True)` (mặc định) hoặc module-level singleton |

---

## B — Depends() — Dependency Đơn Giản

### B.1 Cú pháp cơ bản

```python
from fastapi import FastAPI, Depends

app = FastAPI()

# Dependency function — hàm Python thường
def get_query_params(
    page:  int = 1,
    limit: int = 20,
    sort:  str = "id",
) -> dict:
    return {"page": page, "limit": limit, "sort": sort, "offset": (page - 1) * limit}

# Inject vào endpoint
@app.get("/products")
async def list_products(params: dict = Depends(get_query_params)):
    return {
        "page":     params["page"],
        "limit":    params["limit"],
        "offset":   params["offset"],
        "sort":     params["sort"],
        "products": [],
    }

# GET /products?page=2&limit=10&sort=name
# → params = {"page": 2, "limit": 10, "sort": "name", "offset": 10}
```

> **Điểm mấu chốt:** `get_query_params` nhận query params như endpoint bình thường.
> FastAPI tự parse và inject — không cần gọi hàm thủ công.

### B.2 Dependency dùng yield — tự cleanup

```python
# Dependency có cleanup (dùng cho DB session, file handle, lock...)
def get_db_connection():
    conn = create_connection()   # mở kết nối
    try:
        yield conn               # ← trả về cho endpoint dùng
    finally:
        conn.close()             # ← tự động cleanup dù có exception hay không

@app.get("/users/{id}")
async def get_user(id: int, conn = Depends(get_db_connection)):
    return conn.fetch_one("SELECT * FROM users WHERE id = ?", id)
```

> Giống `try-with-resources` (Java) / `using` (C#) — cleanup đảm bảo xảy ra.

### B.3 Dependency xác thực — Không trả giá trị

```python
from fastapi import Header, HTTPException

API_KEY = "my-secret-key"

# Dependency chỉ để validate — không cần return value
async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="API Key không hợp lệ")
    # Không return gì → FastAPI inject None, nhưng endpoint không dùng

@app.get("/admin/stats", dependencies=[Depends(verify_api_key)])
async def admin_stats():
    return {"users": 100, "products": 500}

# Hoặc dùng trực tiếp trong param nếu cần giá trị
@app.get("/admin/logs")
async def admin_logs(key: None = Depends(verify_api_key)):
    return {"logs": []}
```

### B.4 Dependency dùng class — có state

```python
from fastapi import Query

class PaginationParams:
    def __init__(
        self,
        page:  int = Query(default=1, ge=1),
        limit: int = Query(default=20, ge=1, le=100),
    ):
        self.page   = page
        self.limit  = limit
        self.offset = (page - 1) * limit

@app.get("/orders")
async def list_orders(pagination: PaginationParams = Depends(PaginationParams)):
    return {
        "page":   pagination.page,
        "limit":  pagination.limit,
        "offset": pagination.offset,
    }

# Dùng class trực tiếp trong Depends() — FastAPI tự gọi __init__
# Tương đương: Depends(lambda page, limit: PaginationParams(page, limit))
```

---

## C — Nested Dependencies — Dependency Lồng Nhau

### C.1 Dependency gọi Dependency

```python
from fastapi import Depends, Header, HTTPException
from typing import Annotated

# Tầng 1: Đọc và validate token
async def get_token(authorization: str = Header(...)) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Token format: Bearer <token>")
    return authorization.removeprefix("Bearer ").strip()

# Tầng 2: Decode token → lấy user info
async def get_current_user(token: str = Depends(get_token)) -> dict:
    # Thực tế: decode JWT, query DB...
    if token == "invalid":
        raise HTTPException(401, "Token không hợp lệ")
    return {"id": 1, "name": "Alice", "role": "admin"}

# Tầng 3: Kiểm tra quyền admin
async def require_admin(user: dict = Depends(get_current_user)) -> dict:
    if user["role"] != "admin":
        raise HTTPException(403, "Chỉ admin mới được phép")
    return user

# Endpoint dùng dependency sâu nhất — FastAPI tự giải chain
@app.get("/admin/users")
async def admin_list_users(admin: dict = Depends(require_admin)):
    return {"admin": admin["name"], "users": []}

# Chain: request → get_token → get_current_user → require_admin → endpoint
```

### C.2 Dùng Annotated để code gọn hơn (Python 3.9+)

```python
from typing import Annotated

# Khai báo type alias với dependency
Token       = Annotated[str,  Depends(get_token)]
CurrentUser = Annotated[dict, Depends(get_current_user)]
AdminUser   = Annotated[dict, Depends(require_admin)]

# Endpoint gọn hơn — không cần viết Depends() lặp lại
@app.get("/me")
async def get_me(user: CurrentUser):
    return user

@app.delete("/users/{id}")
async def delete_user(id: int, admin: AdminUser):
    return {"deleted": id, "by": admin["name"]}
```

> ✅ **Khuyến nghị:** Dùng `Annotated` cho dependency tái sử dụng nhiều. Cú pháp ngắn hơn và type checker hiểu đúng kiểu trả về.

### C.3 Cache dependency trong một request

```python
# Mặc định: Depends() cache result trong 1 request
# Nếu cùng dependency xuất hiện nhiều lần → chỉ gọi 1 lần

async def get_settings() -> dict:
    print("get_settings called")   # chỉ in 1 lần dù inject nhiều chỗ
    return {"debug": True, "env": "dev"}

async def dep_a(settings: dict = Depends(get_settings)) -> str:
    return f"A:{settings['env']}"

async def dep_b(settings: dict = Depends(get_settings)) -> str:
    return f"B:{settings['env']}"

@app.get("/test-cache")
async def test_cache(a: str = Depends(dep_a), b: str = Depends(dep_b)):
    return {"a": a, "b": b}
# get_settings() chỉ được gọi 1 lần cho cả dep_a và dep_b

# Tắt cache nếu cần gọi lại mỗi lần:
# b: str = Depends(dep_b, use_cache=False)
```

---

## D — Singleton Pattern trong DI

### D.1 Module-level singleton (cách đơn giản nhất)

```python
# config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:pass@localhost/db"
    SECRET_KEY:   str = "change-me"
    ENV:          str = "development"

    class Config:
        env_file = ".env"

# Singleton: tạo 1 lần khi import module
settings = Settings()

# Dùng làm dependency
def get_settings() -> Settings:
    return settings
```

```python
# Inject settings vào endpoint
from app.core.config import get_settings, Settings

@app.get("/config-info")
async def config_info(cfg: Settings = Depends(get_settings)):
    return {"env": cfg.ENV}
```

### D.2 Connection Pool — Singleton cho DB

```python
# database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

_engine: AsyncEngine | None = None

def get_engine() -> AsyncEngine:
    global _engine
    if _engine is None:
        _engine = create_async_engine(
            settings.DATABASE_URL,
            pool_size=10,           # số connection tối đa trong pool
            max_overflow=20,
            echo=settings.ENV == "development",
        )
    return _engine

# Engine là singleton — tạo 1 lần, dùng lại toàn bộ app
```

### D.3 Startup / Shutdown lifecycle

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: khởi tạo resources
    print("App starting — connecting to DB...")
    engine = get_engine()          # warm up connection pool

    yield                          # ← App đang chạy

    # Shutdown: cleanup resources
    print("App stopping — closing DB connections...")
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
```

> Thay thế cho `@app.on_event("startup")` / `@app.on_event("shutdown")` (đã deprecated).
> Tương đương `@PostConstruct` / `@PreDestroy` trong Spring Boot.

---

## E — SQLAlchemy 2.0 — Giới Thiệu

### E.1 WHAT — SQLAlchemy là gì?

- ORM Python phổ biến nhất — tương tự **Hibernate** (Java) / **Eloquent** (Laravel)
- SQLAlchemy 2.0 (2023+) thay đổi lớn: unified API, native async support
- Hai tầng:
  - **Core**: SQL Expression Language — gần SQL hơn, linh hoạt
  - **ORM**: Mapped class → table — giống JPA Entity

### E.2 Cài đặt

```bash
# PostgreSQL (production)
uv add sqlalchemy[asyncio] asyncpg alembic

# MySQL (alternative)
uv add sqlalchemy[asyncio] aiomysql alembic

# SQLite (dev/test)
uv add sqlalchemy[asyncio] aiosqlite alembic
```

| Driver | Database | URL prefix |
|--------|----------|------------|
| `asyncpg` | PostgreSQL | `postgresql+asyncpg://` |
| `aiomysql` | MySQL | `mysql+aiomysql://` |
| `aiosqlite` | SQLite | `sqlite+aiosqlite:///./app.db` |

### E.3 ⚠️ Java vs SQLAlchemy

| Java / JPA | SQLAlchemy 2.0 |
|------------|----------------|
| `@Entity` class | `class User(Base)` |
| `@Table(name="users")` | `__tablename__ = "users"` |
| `@Id @GeneratedValue` | `id: Mapped[int] = mapped_column(primary_key=True)` |
| `@Column(nullable=false)` | `name: Mapped[str]` (non-nullable by default khi không Optional) |
| `@OneToMany` | `relationship("Order", back_populates="user")` |
| `EntityManager` | `AsyncSession` |
| `em.persist(entity)` | `session.add(obj)` |
| `em.find(User.class, id)` | `await session.get(User, id)` |
| JPQL | SQLAlchemy `select()` expression |

---

## F — Kết Nối Database

### F.1 Cấu hình engine — PostgreSQL

```python
# app/core/database.py

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)
from app.core.config import settings

# Engine: connection pool, 1 instance toàn app
engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,          # "postgresql+asyncpg://user:pass@host/db"
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,             # kiểm tra connection còn sống trước khi dùng
    echo=settings.ENV == "development",
)

# SessionLocal factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,         # không reload object sau commit
)
```

### F.2 DATABASE_URL trong .env

```bash
# .env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/myapp_db

# .env.example (commit file này, không commit .env)
DATABASE_URL=postgresql+asyncpg://USER:PASSWORD@localhost:5432/DB_NAME
```

```python
# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    ENV: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()
```

### F.3 Kiểm tra kết nối

```python
from sqlalchemy import text

async def check_db_connection() -> bool:
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT 1"))
        return result.scalar() == 1

# Health check endpoint
@app.get("/health")
async def health():
    db_ok = await check_db_connection()
    return {
        "status": "ok" if db_ok else "degraded",
        "database": "connected" if db_ok else "disconnected",
    }
```

---

## G — Định Nghĩa Model ORM

### G.1 DeclarativeBase — Base class cho mọi model

```python
# app/models/base.py

from sqlalchemy.orm import DeclarativeBase, MappedColumn
from sqlalchemy import DateTime, func
from datetime import datetime

class Base(DeclarativeBase):
    pass

# Mixin cho timestamp tự động — tái sử dụng
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

### G.2 Khai báo Model — Mapped[T] style (SQLAlchemy 2.0)

```python
# app/models/product.py

from sqlalchemy import String, Numeric, Boolean, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, 


from decimal import Decimal

class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id:          Mapped[int]          = mapped_column(Integer, primary_key=True, autoincrement=True)
    name:        Mapped[str]          = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None]   = mapped_column(Text, nullable=True)
    price:       Mapped[Decimal]      = mapped_column(Numeric(10, 2), nullable=False)
    stock:       Mapped[int]          = mapped_column(Integer, default=0, nullable=False)
    is_active:   Mapped[bool]         = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<Product id={self.id} name={self.name!r}>"
```

### G.3 Model có quan hệ

```python
# app/models/user.py

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id:       Mapped[int]       = mapped_column(Integer, primary_key=True, autoincrement=True)
    email:    Mapped[str]       = mapped_column(String(255), unique=True, nullable=False, index=True)
    name:     Mapped[str]       = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool]     = mapped_column(default=True)

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user", lazy="selectin")

# app/models/order.py
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id:      Mapped[int]  = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int]  = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    total:   Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="orders")
```

> **`Mapped[str]`** = NOT NULL column.
> **`Mapped[str | None]`** = NULLable column.
> SQLAlchemy 2.0 suy ra `nullable` từ type hint — không cần khai báo thừa.

---

## H — Session Management với Depends()

### H.1 Dependency cung cấp DB session

```python
# app/core/database.py

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session               # ← endpoint nhận session
            await session.commit()      # ← commit nếu không có exception
        except Exception:
            await session.rollback()    # ← rollback nếu có exception
            raise
```

### H.2 Inject session vào endpoint

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from typing import Annotated

# Type alias tiện dụng
DB = Annotated[AsyncSession, Depends(get_db)]

@app.get("/products/{id}")
async def get_product(id: int, db: DB):
    product = await db.get(Product, id)
    if product is None:
        raise HTTPException(404, f"Product {id} không tồn tại")
    return product
```

### H.3 Transaction scope

```python
# get_db() tự động:
# - BEGIN transaction khi yield
# - COMMIT sau khi endpoint return thành công
# - ROLLBACK nếu endpoint raise exception
# - Đóng session sau khi done (dù thành công hay lỗi)

@app.post("/products", status_code=201)
async def create_product(data: ProductCreate, db: DB):
    product = Product(**data.model_dump())
    db.add(product)
    # COMMIT tự động sau khi hàm return (trong get_db)
    await db.flush()        # gửi SQL lên DB nhưng chưa commit — để lấy id
    await db.refresh(product)   # reload từ DB (lấy id, default values...)
    return product
```

---

## I — CRUD Cơ Bản với SQLAlchemy

### I.1 Schemas Pydantic

```python
# app/schemas/product.py

from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime

class ProductCreate(BaseModel):
    name:        str            = Field(min_length=1, max_length=255)
    description: str | None     = None
    price:       Decimal        = Field(gt=0, decimal_places=2)
    stock:       int            = Field(ge=0, default=0)

class ProductUpdate(BaseModel):
    name:        str | None     = Field(default=None, min_length=1, max_length=255)
    description: str | None     = None
    price:       Decimal | None = Field(default=None, gt=0)
    stock:       int | None     = Field(default=None, ge=0)
    is_active:   bool | None    = None

class ProductResponse(BaseModel):
    id:          int
    name:        str
    description: str | None
    price:       Decimal
    stock:       int
    is_active:   bool
    created_at:  datetime
    updated_at:  datetime

    model_config = {"from_attributes": True}   # cho phép đọc từ ORM object
```

### I.2 Create

```python
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product
from app.schemas.product import ProductCreate

async def create_product(db: AsyncSession, data: ProductCreate) -> Product:
    product = Product(**data.model_dump())
    db.add(product)
    await db.flush()
    await db.refresh(product)
    return product
```

### I.3 Read — một và nhiều

```python
from sqlalchemy import select, func

async def get_product_by_id(db: AsyncSession, product_id: int) -> Product | None:
    return await db.get(Product, product_id)

async def list_products(
    db:        AsyncSession,
    page:      int = 1,
    limit:     int = 20,
    is_active: bool | None = None,
) -> tuple[list[Product], int]:
    query = select(Product)

    if is_active is not None:
        query = query.where(Product.is_active == is_active)

    # Đếm tổng
    count_query = select(func.count()).select_from(query.subquery())
    total       = (await db.execute(count_query)).scalar_one()

    # Phân trang
    query = query.offset((page - 1) * limit).limit(limit).order_by(Product.id)
    rows  = (await db.execute(query)).scalars().all()

    return list(rows), total
```

### I.4 Update

```python
from app.schemas.product import ProductUpdate

async def update_product(
    db:         AsyncSession,
    product_id: int,
    data:       ProductUpdate,
) -> Product | None:
    product = await db.get(Product, product_id)
    if product is None:
        return None

    # Chỉ cập nhật các field được truyền vào (exclude_unset)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)

    await db.flush()
    await db.refresh(product)
    return product
```

### I.5 Delete

```python
async def delete_product(db: AsyncSession, product_id: int) -> bool:
    product = await db.get(Product, product_id)
    if product is None:
        return False
    await db.delete(product)
    return True

# Soft delete (khuyến khích hơn hard delete)
async def soft_delete_product(db: AsyncSession, product_id: int) -> bool:
    product = await db.get(Product, product_id)
    if product is None:
        return False
    product.is_active = False
    return True
```

### I.6 Query nâng cao — filter, join, order

```python
from sqlalchemy import select, and_, or_

# Filter nhiều điều kiện
async def search_products(
    db:      AsyncSession,
    keyword: str,
    min_price: Decimal | None = None,
    max_price: Decimal | None = None,
) -> list[Product]:
    conditions = [
        Product.is_active == True,
        Product.name.ilike(f"%{keyword}%"),  # ILIKE = case-insensitive LIKE
    ]

    if min_price is not None:
        conditions.append(Product.price >= min_price)
    if max_price is not None:
        conditions.append(Product.price <= max_price)

    query = select(Product).where(and_(*conditions)).order_by(Product.price)
    rows  = (await db.execute(query)).scalars().all()
    return list(rows)
```

---

## J — Async SQLAlchemy

### J.1 asyncpg + async session

```python
# Đã cấu hình từ phần F — không cần thêm gì
# create_async_engine + async_sessionmaker + AsyncSession là bộ đầy đủ

# Tất cả query đều phải await:
result = await db.execute(select(Product))
rows   = result.scalars().all()

product = await db.get(Product, 1)
await db.commit()
await db.rollback()
await db.refresh(product)
```

### J.2 Eager loading quan hệ — selectin load

```python
from sqlalchemy.orm import selectinload

# Lấy user kèm orders (N+1 problem được giải bằng selectin)
async def get_user_with_orders(db: AsyncSession, user_id: int):
    query = (
        select(User)
        .options(selectinload(User.orders))   # load orders trong 1 query riêng
        .where(User.id == user_id)
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()
```

> `selectinload` phát 2 query: 1 cho user, 1 cho orders.
> Tốt hơn `joinedload` khi load list vì tránh row duplication.
> Tốt hơn `lazy` (N+1) vì không load lần lượt từng record.

### J.3 Bulk insert

```python
from sqlalchemy.dialects.postgresql import insert as pg_insert

async def bulk_create_products(db: AsyncSession, items: list[ProductCreate]) -> int:
    data = [item.model_dump() for item in items]
    stmt = pg_insert(Product).values(data).on_conflict_do_nothing()
    result = await db.execute(stmt)
    return result.rowcount
```

---

## K — Alembic — Database Migration

### K.1 Khởi tạo Alembic

```bash
# Cài
uv add alembic

# Khởi tạo thư mục migration (chạy 1 lần)
alembic init alembic

# Cấu trúc tạo ra:
# alembic/
# ├── env.py          ← cấu hình chính
# ├── script.py.mako  ← template cho migration file
# └── versions/       ← các file migration
# alembic.ini         ← config file
```

### K.2 Cấu hình alembic/env.py

```python
# alembic/env.py — phần quan trọng cần chỉnh

from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from alembic import context

# Import Base và tất cả models (để Alembic biết schema)
from app.models.base import Base
from app.models.product import Product    # noqa: F401 — import để đăng ký metadata
from app.models.user import User          # noqa: F401
from app.core.config import settings

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    connectable = create_async_engine(settings.DATABASE_URL, poolclass=pool.NullPool)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def run_migrations_online() -> None:
    import asyncio
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### K.3 Workflow Migration thường ngày

```bash
# 1. Tạo migration tự động từ model thay đổi
alembic revision --autogenerate -m "add products table"
# → tạo alembic/versions/xxxx_add_products_table.py

# 2. Review file migration vừa tạo (quan trọng — autogenerate có thể sai)
# alembic/versions/xxxx_add_products_table.py

# 3. Chạy migration lên DB
alembic upgrade head

# 4. Rollback 1 bước
alembic downgrade -1

# 5. Xem lịch sử
alembic history --verbose

# 6. Xem trạng thái hiện tại
alembic current
```

### K.4 File migration được tạo ra

```python
# alembic/versions/2024_01_15_001_add_products_table.py

"""add products table

Revision ID: a1b2c3d4e5f6
Revises:
Create Date: 2024-01-15 10:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = "a1b2c3d4e5f6"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("id",          sa.Integer(),     nullable=False),
        sa.Column("name",        sa.String(255),   nullable=False),
        sa.Column("description", sa.Text(),        nullable=True),
        sa.Column("price",       sa.Numeric(10,2), nullable=False),
        sa.Column("stock",       sa.Integer(),     nullable=False, server_default="0"),
        sa.Column("is_active",   sa.Boolean(),     nullable=False, server_default="true"),
        sa.Column("created_at",  sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at",  sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_products_name", "products", ["name"])

def downgrade() -> None:
    op.drop_index("ix_products_name", table_name="products")
    op.drop_table("products")
```

### K.5 ⚠️ Java vs Alembic

| Flyway / Liquibase (Java) | Alembic (Python) |
|--------------------------|------------------|
| `V1__init.sql` SQL file | `alembic revision --autogenerate` → Python file |
| `flyway migrate` | `alembic upgrade head` |
| `flyway undo` | `alembic downgrade -1` |
| Schema tracking trong `flyway_schema_history` | Schema tracking trong `alembic_version` table |
| Tự phát hiện file mới khi deploy | Phải gọi `alembic upgrade head` explicit |

---

## L — API CRUD Hoàn Chỉnh — Product API

### L.1 Cấu trúc thư mục

```
my-api/
├── main.py
├── .env
├── alembic/
│   ├── env.py
│   └── versions/
├── app/
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   │   ├── base.py
│   │   └── product.py
│   ├── schemas/
│   │   └── product.py
│   ├── repositories/           ← tầng truy cập DB
│   │   └── product_repo.py
│   └── routers/
│       └── products.py
```

### L.2 Repository pattern

```python
# app/repositories/product_repo.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from decimal import Decimal

class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, product_id: int) -> Product | None:
        return await self.db.get(Product, product_id)

    async def list(
        self,
        page:      int  = 1,
        limit:     int  = 20,
        is_active: bool = True,
    ) -> tuple[list[Product], int]:
        base_query = select(Product).where(Product.is_active == is_active)
        total      = (await self.db.execute(
            select(func.count()).select_from(base_query.subquery())
        )).scalar_one()
        rows = (await self.db.execute(
            base_query.offset((page - 1) * limit).limit(limit).order_by(Product.id)
        )).scalars().all()
        return list(rows), total

    async def create(self, data: ProductCreate) -> Product:
        product = Product(**data.model_dump())
        self.db.add(product)
        await self.db.flush()
        await self.db.refresh(product)
        return product

    async def update(self, product_id: int, data: ProductUpdate) -> Product | None:
        product = await self.get_by_id(product_id)
        if product is None:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(product, field, value)
        await self.db.flush()
        await self.db.refresh(product)
        return product

    async def delete(self, product_id: int) -> bool:
        product = await self.get_by_id(product_id)
        if product is None:
            return False
        product.is_active = False   # soft delete
        return True
```

### L.3 Router Product CRUD

```python
# app/routers/products.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.core.database import get_db
from app.repositories.product_repo import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])

DB = Annotated[AsyncSession, Depends(get_db)]

def get_repo(db: DB) -> ProductRepository:
    return ProductRepository(db)

Repo = Annotated[ProductRepository, Depends(get_repo)]


@router.get("/", response_model=dict)
async def list_products(
    repo:  Repo,
    page:  int  = Query(default=1, ge=1),
    limit: int  = Query(default=20, ge=1, le=100),
):
    products, total = await repo.list(page=page, limit=limit)
    return {
        "data":  [ProductResponse.model_validate(p) for p in products],
        "total": total,
        "page":  page,
        "limit": limit,
    }


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, repo: Repo):
    product = await repo.get_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail=f"Product {product_id} không tồn tại")
    return product


@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(data: ProductCreate, repo: Repo):
    return await repo.create(data)


@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, data: ProductUpdate, repo: Repo):
    product = await repo.update(product_id, data)
    if product is None:
        raise HTTPException(status_code=404, detail=f"Product {product_id} không tồn tại")
    return product


@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: int, repo: Repo):
    deleted = await repo.delete(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Product {product_id} không tồn tại")
```

### L.4 main.py hoàn chỉnh

```python
# main.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine
from app.routers import products

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()

app = FastAPI(
    title="Product API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)

@app.get("/health", tags=["System"])
async def health():
    return {"status": "ok"}
```

### L.5 Chạy và test

```bash
# Tạo DB và chạy migration
createdb myapp_db
alembic upgrade head

# Chạy server
uvicorn main:app --reload

# Test API
# GET  http://localhost:8000/docs
# POST http://localhost:8000/products
# GET  http://localhost:8000/products
# GET  http://localhost:8000/products/1
# PATCH http://localhost:8000/products/1
# DELETE http://localhost:8000/products/1
```

---

## M — Java vs FastAPI — Bảng Đối Chiếu Khối 11

| Khái niệm | Spring Boot | FastAPI |
|-----------|-------------|---------|
| DI container | `ApplicationContext` | FastAPI request scope tự quản lý |
| Inject dependency | `@Autowired` | `param: Type = Depends(func)` |
| Dependency function | `@Bean` trong `@Configuration` | Hàm Python thường |
| Cleanup resource | `@PreDestroy` / try-with-resources | `yield` trong dependency function |
| ORM | JPA / Hibernate | SQLAlchemy 2.0 |
| Entity | `@Entity @Table` class | `class Model(Base)` |
| Column | `@Column` annotation | `mapped_column()` với type hint `Mapped[T]` |
| EntityManager | `EntityManager` / `JpaRepository` | `AsyncSession` |
| persist | `em.persist(entity)` | `session.add(obj)` |
| find by id | `repo.findById(id)` | `await session.get(Model, id)` |
| JPQL query | `@Query("SELECT u FROM User u WHERE...")` | `select(User).where(User.x == y)` |
| Transaction | `@Transactional` | `get_db()` dependency tự commit/rollback |
| Migration | Flyway: `V1__init.sql` | Alembic: `alembic revision --autogenerate` |
| Run migration | Auto khi startup (Flyway config) | `alembic upgrade head` explicit |
| Repository pattern | `JpaRepository<Entity, ID>` interface | Class Python với `AsyncSession` |
| Startup hook | `@PostConstruct` / `ApplicationRunner` | `lifespan` context manager |

---

## N — Bài Tập Thực Hành

```python
# ============================================================
# Bài 1 — Dependency Chain: Token → User → Role check
# ============================================================

from fastapi import FastAPI, Depends, Header, HTTPException
from typing import Annotated

app = FastAPI(title="Block 11 Practice")

FAKE_TOKENS = {
    "token-alice": {"id": 1, "name": "Alice", "role": "admin"},
    "token-bob":   {"id": 2, "name": "Bob",   "role": "user"},
}

async def get_token(authorization: str = Header(...)) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Format: Bearer <token>")
    return authorization.removeprefix("Bearer ").strip()

async def get_current_user(token: str = Depends(get_token)) -> dict:
    user = FAKE_TOKENS.get(token)
    if user is None:
        raise HTTPException(401, "Token không hợp lệ")
    return user

async def require_admin(user: dict = Depends(get_current_user)) -> dict:
    if user["role"] != "admin":
        raise HTTPException(403, "Chỉ admin mới được phép")
    return user

CurrentUser = Annotated[dict, Depends(get_current_user)]
AdminUser   = Annotated[dict, Depends(require_admin)]

@app.get("/me")
async def get_me(user: CurrentUser):
    return user

@app.get("/admin/users")
async def admin_list_users(admin: AdminUser):
    return {"admin": admin["name"], "users": list(FAKE_TOKENS.values())}


# ============================================================
# Bài 2 — SQLAlchemy + CRUD hoàn chỉnh (dùng SQLite để dễ test)
# ============================================================

from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncSession
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Numeric, Boolean, select
from pydantic import BaseModel, Field
from decimal import Decimal
from typing import AsyncGenerator

# --- Setup DB ---
SQLITE_URL = "sqlite+aiosqlite:///./practice.db"
engine     = create_async_engine(SQLITE_URL, echo=True)
Session    = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

# --- Model ---
class Item(Base):
    __tablename__ = "items"

    id:       Mapped[int]          = mapped_column(Integer, primary_key=True, autoincrement=True)
    name:     Mapped[str]          = mapped_column(String(100), nullable=False)
    price:    Mapped[Decimal]      = mapped_column(Numeric(10, 2), nullable=False)
    quantity: Mapped[int]          = mapped_column(Integer, default=0)
    active:   Mapped[bool]         = mapped_column(Boolean, default=True)

# --- Schemas ---
class ItemCreate(BaseModel):
    name:     str     = Field(min_length=1, max_length=100)
    price:    Decimal = Field(gt=0)
    quantity: int     = Field(ge=0, default=0)

class ItemUpdate(BaseModel):
    name:     str | None     = None
    price:    Decimal | None = None
    quantity: int | None     = None
    active:   bool | None    = None

class ItemResponse(BaseModel):
    id:       int
    name:     str
    price:    Decimal
    quantity: int
    active:   bool

    model_config = {"from_attributes": True}

# --- DB Dependency ---
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

DB = Annotated[AsyncSession, Depends(get_db)]

# --- Create tables on startup ---
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app2 = FastAPI(title="Practice CRUD", lifespan=lifespan)

# --- Endpoints ---
@app2.get("/items", response_model=list[ItemResponse])
async def list_items(db: DB):
    rows = (await db.execute(select(Item).where(Item.active == True))).scalars().all()
    return rows

@app2.post("/items", response_model=ItemResponse, status_code=201)
async def create_item(data: ItemCreate, db: DB):
    item = Item(**data.model_dump())
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item

@app2.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, db: DB):
    item = await db.get(Item, item_id)
    if item is None:
        raise HTTPException(404, f"Item {item_id} không tồn tại")
    return item

@app2.patch("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, data: ItemUpdate, db: DB):
    item = await db.get(Item, item_id)
    if item is None:
        raise HTTPException(404, f"Item {item_id} không tồn tại")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    await db.flush()
    await db.refresh(item)
    return item

@app2.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int, db: DB):
    item = await db.get(Item, item_id)
    if item is None:
        raise HTTPException(404, f"Item {item_id} không tồn tại")
    item.active = False   # soft delete

# Chạy: uvicorn main:app2 --reload --port 8001
# Test:  http://localhost:8001/docs
```

---

## Tóm Tắt — Điểm Cần Nhớ

| Điều | Ghi nhớ |
|------|---------|
| `Depends()` | Inject dependency — FastAPI tự gọi và truyền vào, không tự gọi |
| `yield` trong dependency | Giống try-with-resources — cleanup đảm bảo xảy ra |
| Nested dependency | FastAPI tự giải chain — chỉ gọi mỗi dependency 1 lần/request |
| `Annotated[Type, Depends(...)]` | Cú pháp gọn — tạo type alias cho dependency tái sử dụng |
| `Depends` cache | Mặc định cache trong 1 request — `use_cache=False` để tắt |
| `DeclarativeBase` | Base class cho tất cả ORM model trong SQLAlchemy 2.0 |
| `Mapped[str]` vs `Mapped[str \| None]` | NOT NULL vs NULLable — suy ra từ type hint |
| `expire_on_commit=False` | Object không bị invalidate sau commit — không cần query lại |
| `model_dump(exclude_unset=True)` | PATCH: chỉ update field được gửi lên, không ghi đè None |
| `model_config = {"from_attributes": True}` | Cho phép Pydantic đọc từ SQLAlchemy ORM object |
| `selectinload` | Load quan hệ không bị N+1 — phát 2 query thay vì N+1 |
| `alembic upgrade head` | Chạy migration lên version mới nhất |
| `--autogenerate` | Alembic tự detect thay đổi Model → sinh migration file |
| Transaction trong `get_db()` | commit khi thành công, rollback khi exception — tự động |
