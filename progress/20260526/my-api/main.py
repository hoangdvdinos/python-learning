# main.py
from fastapi import FastAPI

# Tạo instance FastAPI — tương đương @SpringBootApplication
# title, description, version → hiển thị trong /docs
app = FastAPI(
    title="My API",
    version="1.0.0",
    description="API demo cho Java developer",
)

# Endpoint đầu tiên
# @app.get("/") = @GetMapping("/") trong @RestController
@app.get("/")
async def root():
    # Trả dict → FastAPI tự chuyển thành JSON + set Content-Type: application/json
    return {"message": "Hello, xin chào FastAPI", "status": "running"}