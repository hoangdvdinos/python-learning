# import asyncio

# async def fetch_data(name: str, delay: float) -> str:
#     print(f"  [{name}] Bắt đầu fetch...")
#     await asyncio.sleep(delay)
#     print(f"  [{name}] Hoàn thành sau {delay}s")
#     return f"data từ {name}"

# async def main():
#     # Tạo Task — lên lịch coroutine chạy song song NGAY LẬP TỨC
#     task_a = asyncio.create_task(fetch_data("ServiceA", 1.0))
#     task_b = asyncio.create_task(fetch_data("ServiceB", 0.5))
#     task_c = asyncio.create_task(fetch_data("ServiceC", 1.5))

#     # Chờ tất cả task hoàn thành
#     result_a = await task_a
#     result_b = await task_b
#     result_c = await task_c

#     print(f"Kết quả: {result_a}, {result_b}, {result_c}")

# import time
# start = time.perf_counter()
# asyncio.run(main())
# elapsed = time.perf_counter() - start
# print(f"Tổng thời gian: {elapsed:.2f}s")   # ~1.50s (không phải 1+0.5+1.5=3.0s)

import asyncio
import time
import httpx
import requests  # pip install requests — sync HTTP

URLS = [
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://jsonplaceholder.typicode.com/posts/2",
    "https://jsonplaceholder.typicode.com/posts/3",
    "https://jsonplaceholder.typicode.com/posts/4",
    "https://jsonplaceholder.typicode.com/posts/5",
]

# --- CÁCH 1: Synchronous (Blocking) ---
# def fetch_sync(url: str) -> dict:
#     return requests.get(url).json()

# def fetch_all_sync(urls: list[str]) -> list[dict]:
#     return [fetch_sync(url) for url in urls]

# start = time.perf_counter()
# sync_results = fetch_all_sync(URLS)
# sync_elapsed = time.perf_counter() - start
# print(f"Sync:  {sync_elapsed:.2f}s — {len(sync_results)} results")

async def fetch_async(client: httpx.AsyncClient, url: str) -> dict:
    response = await client.get(url)
    return response.json()

async def fetch_all_async(urls: list[str]) -> list[dict]:
    async with httpx.AsyncClient() as client:
        tasks = [fetch_async(client, url) for url in urls]
        return await asyncio.gather(*tasks)

start = time.perf_counter()
async_results = asyncio.run(fetch_all_async(URLS))
async_elapsed = time.perf_counter() - start
print(f"Async: {async_elapsed:.2f}s — {len(async_results)} results")