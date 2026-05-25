# Bài 1: Đọc file CSV, xử lý dữ liệu, ghi file JSON
# - Đọc file employees.csv (tạo trong bài nếu chưa có)
# - Tính lương trung bình theo phòng ban
# - Ghi kết quả ra report.json

import csv
import json
from pathlib import Path
from collections import defaultdict

# Path("employees.csv").write_text(
#     "name,department,salary\n"
#     "Alice,Engineering,35000000\n"
#     "Bob,Marketing,28000000\n"
#     "Charlie,Engineering,40000000\n"
#     "Dave,Marketing,32000000\n"
#     "Eve,Engineering,38000000\n",
#     encoding="utf-8"
# )

# dept_salaries: dict[str, list[int]] = defaultdict(list)

# with open("employees.csv", "r", encoding="utf-8") as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         dept_salaries[row["department"]].append(int(row["salary"]))
        
# report = {
#     dept: {
#         "count": len(salaries),
#         "average_salary": sum(salaries) / len(salaries),
#         "total_salary": sum(salaries)
#     } for dept, salaries in dept_salaries.items()
# }

# with open("report.json", "w", encoding="utf-8") as f:
#     json.dump(report, f, indent=2, ensure_ascii=False)

# with open("report.json", "r", encoding="utf-8") as f:
#     content = json.load(f)
#     print(json.dumps(content, indent=2, ensure_ascii=False))
    
# Bài 2: Log writer với rotation
# - Ghi log vào file, mỗi dòng có timestamp
# - Nếu file > 1KB thì rotate sang file mới (backup)
# from datetime import datetime
# import os

# class SimpleLogger:
#     def __init__(self, path: str, max_bytes: int = 1024):
#         self.path = Path(path)
#         self.max_bytes = max_bytes

#     def _rotate(self) -> None:
#         backup = self.path.with_suffix(".log.bak")
#         if backup.exists():
#             backup.unlink()
#         self.path.rename(backup)

#     def log(self, level: str, message: str) -> None:
#         if self.path.exists() and self.path.stat().st_size > self.max_bytes:
#             self._rotate()

#         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         with open(self.path, "a", encoding="utf-8") as f:
#             f.write(f"[{timestamp}] [{level}] {message}\n")
#             f.flush()

# logger = SimpleLogger("app.log", max_bytes=200)
# for i in range(10):
#     logger.log("INFO", f"Processing record #{i}")
# logger.log("ERROR", "Something went wrong")

# print(f"app.log size: {Path('app.log').stat().st_size} bytes")
# if Path("app.log.bak").exists():
#     print("Rotated! app.log.bak tồn tại")

import json
from pathlib import Path

class ConfigError(Exception):
    pass

class ConfigNotFoundError(ConfigError):
    def __init__(self, path: str):
        super().__init__(f"Config file không tìm thấy: {path}")
        self.path = path

class ConfigParseError(ConfigError):
    def __init__(self, path: str, detail: str):
        super().__init__(f"Config file không hợp lệ [{path}]: {detail}")
        self.path = path

class ConfigValidationError(ConfigError):
    def __init__(self, field: str, reason: str):
        super().__init__(f"Config validation failed — {field}: {reason}")
        self.field = field

def load_config(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except FileNotFoundError:
        raise ConfigNotFoundError(path)
    except json.JSONDecodeError as e:
        raise ConfigParseError(path, str(e)) from e

    # Validate
    required = ["host", "port", "database"]
    for field in required:
        if field not in config:
            raise ConfigValidationError(field, "Trường bắt buộc bị thiếu")

    if not isinstance(config["port"], int) or not (1 <= config["port"] <= 65535):
        raise ConfigValidationError("port", f"Phải là int từ 1-65535, nhận: {config['port']!r}")

    return config

# Test
test_cases = [
    ("nonexistent.json", "File không tồn tại"),
    ("bad_config.json", "JSON không hợp lệ"),
    ("missing_field.json", "Thiếu trường bắt buộc"),
    ("valid_config.json", "Config hợp lệ"),
]

# Tạo file test
Path("bad_config.json").write_text("{ not valid json", encoding="utf-8")
Path("missing_field.json").write_text('{"host": "localhost"}', encoding="utf-8")
Path("valid_config.json").write_text(
    '{"host": "localhost", "port": 5432, "database": "myapp"}',
    encoding="utf-8"
)

for filename, description in test_cases:
    print(f"\n--- {description} ---")
    try:
        config = load_config(filename)
        print(f"OK: {config}")
    except ConfigNotFoundError as e:
        print(f"ConfigNotFoundError: {e}")
    except ConfigParseError as e:
        print(f"ConfigParseError: {e}")
    except ConfigValidationError as e:
        print(f"ConfigValidationError: {e} (field={e.field})")
    except ConfigError as e:
        print(f"ConfigError: {e}")