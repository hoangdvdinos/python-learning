# Đọc Code Từ Thấp Lên Cao

## Tại Sao Đọc Chậm

### Không biết bắt đầu từ đâu

### Đọc từ trên xuống ngay

### Sa vào chi tiết quá sớm

### Không hình dung data trông như thế nào

### Thiếu câu hỏi dẫn đường

## Nguyên Tắc Cốt Lõi

### Hiểu data trước, logic sau

### Đọc theo tầng, không đọc tất cả

### Đặt 1 câu hỏi cho mỗi tầng

### Trace 1 request từ đầu đến cuối

### Dừng đúng chỗ đủ hiểu

## Tầng 1 - Models (Thấp Nhất)

### Đây là gì

#### Schema thật của DB

#### Tương đương JPA Entity trong Java

### Đọc gì ở đây

#### Bảng tên gì

#### Cột tên gì, kiểu gì

#### Quan hệ giữa các bảng

### Câu hỏi cần trả lời

#### Data trông như thế nào?

#### Bảng nào liên quan nhau?

### File cần đọc

#### app/models/category.py

#### app/models/transaction.py

#### app/models/base.py

## Tầng 2 - Schemas (Pydantic)

### Đây là gì

#### Data shape cho API

#### Validate input/output

#### Tương đương DTO trong Java

### Đọc gì ở đây

#### Request nhận gì

#### Response trả gì

#### Field nào optional, bắt buộc

### Câu hỏi cần trả lời

#### Người dùng gửi lên gì?

#### API trả về gì?

### File cần đọc

#### app/schemas/category.py

#### app/schemas/transaction.py

## Tầng 3 - Repositories

### Đây là gì

#### Tầng truy cập DB

#### Tương đương Spring Data JPA

### Đọc gì ở đây

#### Hàm làm gì

#### Query như thế nào

#### Trả về kiểu gì

### Câu hỏi cần trả lời

#### Lấy data bằng cách nào?

#### Filter, sort, join ở đâu?

### File cần đọc

#### app/repositories/category_repo.py

#### app/repositories/transaction_repo.py

#### app/repositories/report_repo.py

## Tầng 4 - Routers

### Đây là gì

#### HTTP endpoint handler

#### Tương đương @RestController trong Java

### Đọc gì ở đây

#### URL path là gì

#### HTTP method gì

#### Gọi repository nào

### Câu hỏi cần trả lời

#### Client gọi URL nào?

#### Luồng từ request đến response?

### File cần đọc

#### app/routers/categories.py

#### app/routers/transactions.py

#### app/routers/reports.py

## Tầng 5 - Core (Cao Nhất)

### Đây là gì

#### Config, DB init, Exception

#### Tương đương ApplicationContext Spring

### Đọc gì ở đây

#### App cấu hình ra sao

#### DB kết nối kiểu gì

#### Exception xử lý ở đâu

### Câu hỏi cần trả lời

#### App khởi động như thế nào?

#### Đọc config từ đâu?

### File cần đọc

#### app/core/config.py

#### app/core/database.py

#### app/main.py

## Quy Trình Đọc 1 Feature

### Bước 1 - Xác định mục tiêu

#### Muốn hiểu feature gì

#### Ví dụ: tạo category

### Bước 2 - Đọc Model trước

#### Bảng category có gì

#### Cột name, type, is_deleted

### Bước 3 - Đọc Schema

#### CreateCategoryRequest nhận gì

#### CategoryResponse trả gì

### Bước 4 - Đọc Repository

#### create() làm gì

#### get_by_id() query ra sao

### Bước 5 - Đọc Router

#### POST /categories gọi gì

#### Trả về status gì

### Bước 6 - Trace luồng đầy đủ

#### Request vào → Router → Repo → DB

#### DB → Repo → Schema → Response

## Kỹ Năng Đọc Code Nhanh

### Đọc tên trước, body sau

#### Tên hàm đã nói lên 70% ý nghĩa

#### Đọc body khi cần chi tiết

### Tìm entry point

#### Với web: tìm router

#### Với script: tìm main()

### Đọc type/signature

#### Input là gì

#### Output là gì

#### Không cần đọc hết body

### Dùng Go To Definition

#### Bấm vào tên hàm

#### Nhảy thẳng vào định nghĩa

## Lỗi Hay Mắc

### Đọc từ main.py xuống

#### main.py là glue code, không có logic

#### Nên đọc models trước

### Đọc tất cả file cùng lúc

#### Chọn 1 feature, trace theo luồng

### Không biết dừng

#### Đủ trả lời câu hỏi là dừng

### Quên mất mình đang tìm gì

#### Viết câu hỏi ra trước khi đọc

## Checklist Trước Khi Đọc

### Mình muốn hiểu gì?

### Bắt đầu từ tầng nào?

### Câu hỏi cần trả lời là gì?

## Checklist Sau Khi Đọc

### Data trông như thế nào rồi?

### Hàm này làm gì rồi?

### Trace được 1 request chưa?

### Hiểu tại sao có tầng này chưa?

## Tóm Tắt Một Câu

### Đọc từ data shape lên logic rồi mới lên luồng
