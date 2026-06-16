import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.exceptions import AppException
from app.routers import categories_router, reports_router, transactions_router


# --- Lifespan ---
# asynccontextmanager biến hàm generator thành context manager bất đồng bộ.
# FastAPI dùng lifespan để chạy code khi app khởi động (trước yield)
# và khi app tắt (sau yield) — thay thế cho on_event("startup"/"shutdown") cũ.
@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Starting up {settings.APP_NAME} v{settings.APP_VERSION}...")
    yield  # <-- App chạy ở đây; code sau yield chỉ chạy khi shutdown
    print("Shutting down...")


# --- App Instance ---
# Tạo instance FastAPI chính. title/version hiển thị trên Swagger UI (/docs).
# lifespan truyền vào để FastAPI biết dùng hàm nào quản lý vòng đời app.
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# --- Middleware ---

# CORS (Cross-Origin Resource Sharing): cho phép trình duyệt gọi API từ domain khác.
# Ở đây chỉ cho phép frontend dev (localhost:3000 Vite/CRA, localhost:5173 Vite).
# allow_methods=["*"] và allow_headers=["*"] nghĩa là không giới hạn method/header.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware log request: chạy bọc quanh MỌI request (tương tự Filter trong Java/Spring).
# call_next là hàm gọi handler tiếp theo trong chuỗi middleware → trả về response.
# Pattern: ghi nhận thời điểm vào, gọi next, tính thời gian xử lý, gắn header vào response.
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())[:8]  # ID ngắn 8 ký tự để trace log
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    print(f"[{request_id}] {request.method} {request.url.path} -> {response.status_code} ({duration:.3f}s)")
    response.headers["X-Request-Id"] = request_id  # Gắn request ID vào response header để client trace
    return response


# --- Exception Handlers ---

# Handler cho AppException (custom exception của app).
# type(exc).__name__ lấy tên class (vd: "NotFoundException"), rồi bỏ đuôi "Exception"
# và viết hoa → error_code = "NOTFOUND". Giúp client phân biệt loại lỗi mà không cần HTTP status.
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    error_code = type(exc).__name__.replace("Exception", "").upper()
    return JSONResponse(
        status_code=exc.status_code,
        content={"error_code": error_code, "message": exc.message, "detail": None},
    )


# Fallback handler cho mọi exception không được bắt ở trên.
# Luôn trả 500 với message chung — tránh lộ stack trace ra ngoài (security best practice).
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"error_code": "INTERNAL_ERROR", "message": "An unexpected error occurred.", "detail": None},
    )


# --- Routers ---

# Prefix chung cho toàn bộ API — versioning theo URL (/api/v1/...).
# Khi cần nâng version chỉ cần thêm prefix v2 và include router mới, không phá vỡ client cũ.
API_PREFIX = "/api/v1"

app.include_router(categories_router, prefix=API_PREFIX)
app.include_router(transactions_router, prefix=API_PREFIX)
app.include_router(reports_router, prefix=API_PREFIX)


# Health check endpoint: dùng để load balancer / container orchestrator (K8s liveness probe)
# kiểm tra app còn sống không. Không cần auth, trả về nhanh.
@app.get("/health")
async def health_check():
    return {"status": "ok", "version": settings.APP_VERSION}
