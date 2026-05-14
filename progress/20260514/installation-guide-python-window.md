# Cài đặt Python 3.12+ trên Windows — Từ con số 0

> Tài liệu này dành cho người **chưa biết gì về Python**. Mỗi bước đều giải thích **"tại sao làm"** chứ không chỉ "làm thế nào".

---

## 0. Hiểu trước khi cài: Python là gì? Mình đang cài cái gì?

**Python** là một ngôn ngữ lập trình. Khi cháu viết code Python (file `.py`), máy tính không hiểu trực tiếp — cần một chương trình **"phiên dịch"** đọc file đó rồi chạy. Chương trình phiên dịch đó gọi là **Python interpreter** (`python.exe`).

→ **"Cài Python" = cài chương trình `python.exe` lên máy.**

Cài xong, mỗi khi cháu gõ `python tenfile.py` trong terminal, Windows sẽ gọi `python.exe` để chạy file đó.

### Vì sao chọn version 3.12+?

Python có 2 nhánh lớn: Python 2 (đã chết, không support nữa) và Python 3 (đang dùng). Trong Python 3, mỗi năm ra 1 version mới (3.10, 3.11, 3.12, 3.13...). Version mới nhanh hơn, có syntax mới, fix bug.

→ **Chọn 3.12+ vì đó là version stable hiện đại, tài liệu/thư viện đều support.**

---

## 1. Download Python

Vào trang chính thức: <https://www.python.org/downloads/windows/>

Tải file installer **Windows installer (64-bit)** — tên dạng `python-3.12.x-amd64.exe`.

> ⚠️ **Đừng cài Python từ Microsoft Store.** Bản đó bị Windows giới hạn permission, sau này `pip install` hay bị lỗi "Access denied" rất khó debug. Luôn cài từ python.org.

---

## 2. Cài đặt — và những ô tick "tưởng nhỏ nhưng cực quan trọng"

Chạy file `.exe` vừa tải. Ở màn hình đầu tiên sẽ có 2 ô tick ở dưới — **đây là phần dễ sai nhất**:

### ✅ Tick: "Add python.exe to PATH"

**PATH là gì?** PATH là danh sách các thư mục mà Windows sẽ tìm khi cháu gõ một lệnh trong terminal. Ví dụ gõ `python`, Windows sẽ duyệt qua các thư mục trong PATH để tìm file tên `python.exe`. Nếu Python không nằm trong PATH, gõ `python` sẽ báo **"không tìm thấy lệnh"**.

→ **Tick ô này = Windows biết `python.exe` ở đâu, gõ `python` ở bất kỳ đâu cũng chạy được.** Nếu quên tick, sau này phải set tay rất phiền.

### ✅ Tick: "Use admin privileges when installing py.exe"

Cài cho mọi user trên máy, không bị giới hạn quyền.

### Tiếp theo: chọn "Customize installation"

Không bấm "Install Now" — chọn **Customize** để control được cài gì.

**Optional Features**: tick hết. Trong đó:
- **pip** — công cụ cài thư viện (giải thích kỹ ở bước 4). **Bắt buộc tick**.
- **tcl/tk** — để chạy được GUI nếu sau này học `tkinter`.
- **py launcher** — tool quản lý nhiều version Python cùng lúc.

**Advanced Options**:
- ✅ Install Python for all users
- ✅ Add Python to environment variables
- Đổi install location về `C:\Python312` cho gọn (mặc định path rất dài và rối)

Bấm **Install** → đợi → **Close**.

---

## 3. Kiểm tra cài đặt — Xác nhận máy đã "biết" Python

Mở **PowerShell** (gõ "PowerShell" ở Start Menu). Chạy:

```powershell
python --version
pip --version
```

**Mục đích**: gõ 2 lệnh này để xác nhận
1. Windows tìm thấy `python.exe` (= PATH set đúng)
2. `pip` cũng đã được cài kèm

Output mong đợi:

```
Python 3.12.x
pip 24.x.x from ...
```

### Nếu báo lỗi `'python' is not recognized`

Nghĩa là **PATH không có Python** → cách fix:
- Mở lại file installer → chọn **Modify** → tick **Add Python to environment variables** → Next.
- Đóng PowerShell cũ, mở PowerShell mới (PATH chỉ load khi terminal khởi động).

---

## 4. pip là gì? Tại sao cần upgrade?

**pip** là **package manager** của Python — công cụ để **cài thư viện** (code của người khác viết sẵn) về máy.

Ví dụ: muốn gọi API HTTP, không phải tự code từ đầu — chỉ cần `pip install requests` là có ngay thư viện `requests` để dùng.

pip được cài kèm Python, nhưng thường là version cũ. Upgrade lên bản mới:

```powershell
python -m pip install --upgrade pip
python -m pip install --upgrade setuptools wheel
```

Giải thích lệnh:
- `python -m pip` = "chạy module pip thông qua Python" — cách an toàn nhất, tránh nhầm version pip nếu máy có nhiều Python.
- `setuptools`, `wheel` — 2 thư viện nền tảng giúp việc cài package khác trơn tru hơn.

---

## 5. venv (virtual environment) — Khái niệm quan trọng nhất khi mới học

### Vấn đề nếu không dùng venv

Mặc định, khi `pip install requests`, thư viện sẽ cài **global** (cài chung cho toàn máy). Vấn đề xảy ra khi:

- Project A cần `requests` version 2.28
- Project B cần `requests` version 2.31

→ Cài cái này thì cái kia chạy sai. **Conflict dependency** là vấn đề kinh điển của Python.

### venv giải quyết thế nào?

`venv` = tạo một **"hộp Python riêng"** cho mỗi project. Mỗi project có 1 folder `.venv` chứa Python interpreter và thư viện riêng. Cài gì vào đây chỉ ảnh hưởng project đó, không đụng tới các project khác.

**Quy tắc cần khắc cốt ghi tâm: mỗi project 1 venv riêng, không bao giờ cài package vào Python global.**

### Cách dùng venv

```powershell
# 1. Tạo folder project
mkdir my-project
cd my-project

# 2. Tạo venv — câu lệnh này tạo ra folder .venv chứa Python "riêng"
python -m venv .venv

# 3. Activate venv — "bước vào" hộp riêng của project
.\.venv\Scripts\Activate.ps1
```

Khi activate thành công, terminal sẽ có prefix `(.venv)` ở đầu dòng:

```
(.venv) PS C:\my-project>
```

Lúc này gõ `pip install requests` → thư viện chỉ cài vào `.venv` của project này, không cài ra ngoài.

Khi xong việc, thoát venv:

```powershell
deactivate
```

### Lỗi phổ biến: PowerShell chặn script

Lần đầu chạy `Activate.ps1` có thể báo:

```
running scripts is disabled on this system
```

**Nguyên nhân**: Windows mặc định chặn chạy script `.ps1` để bảo mật.

**Fix**: mở PowerShell **as Administrator** (chuột phải → Run as Administrator), chạy:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Lệnh này cho phép chạy script do mình tạo. Chỉ cần làm 1 lần duy nhất.

---

## 6. Cài IDE — Editor để viết code

**IDE** (Integrated Development Environment) = phần mềm để viết code, có syntax highlight, autocomplete, debug...

Khuyến nghị **VS Code** — miễn phí, nhẹ, phổ biến nhất hiện nay.

Tải tại: <https://code.visualstudio.com/>

Cài xong, mở VS Code → vào tab **Extensions** (icon 4 ô vuông bên trái, hoặc `Ctrl+Shift+X`), cài:

- **Python** (publisher: Microsoft) — support cơ bản: chạy code, debug
- **Pylance** (Microsoft) — autocomplete thông minh, gợi ý type
- **Ruff** (Astral Software) — bắt lỗi và format code tự động

### Quan trọng: Cho VS Code biết dùng venv nào

Mỗi project có venv riêng → phải bảo VS Code dùng đúng venv của project đó:

1. Mở folder project trong VS Code
2. Bấm `Ctrl+Shift+P` (mở Command Palette)
3. Gõ `Python: Select Interpreter`
4. Chọn cái có chữ `.venv` trong đường dẫn

Sau bước này, VS Code sẽ tự động activate venv khi mở terminal trong nó.

---

## 7. Test thử — File Python đầu tiên

Trong folder project, tạo file `hello.py`:

```python
def main():
    name = input("Tên của bạn: ")
    print(f"Hello, {name}! Python is working.")

if __name__ == "__main__":
    main()
```

Trong terminal (đã activate venv), chạy:

```powershell
python hello.py
```

Nếu nó hỏi tên rồi in lời chào → setup xong. 🎉

---

## 8. Tool nên biết (chưa cần cài ngay, học sau)

| Tool | Mục đích | Khi nào cần |
|------|----------|-------------|
| `uv` | Thay thế pip + venv, nhanh hơn 10-100x | Khi đã quen, muốn workflow hiện đại |
| `ruff` | Linter (bắt lỗi style) + formatter | Khi bắt đầu viết code dài, cần code sạch |
| `mypy` | Kiểm tra type tĩnh | Khi học type hints, viết code lớn |
| `pytest` | Viết unit test | Khi học testing |
| `ipython` | REPL nâng cao (gõ code thử nhanh) | Khi cần thử nghiệm code lẻ |

---

## Checklist hoàn thành

Sau khi xong, cháu phải làm được hết những điều sau:

- [ ] Hiểu **Python interpreter là gì**, mình đã cài cái gì lên máy
- [ ] `python --version` ra version 3.12+ ở bất kỳ terminal nào
- [ ] `pip --version` chạy được
- [ ] Hiểu **PATH là gì** và tại sao phải tick lúc cài
- [ ] Hiểu **venv là gì** và tại sao mỗi project cần venv riêng
- [ ] Tự tạo được venv, activate được, thoát được
- [ ] VS Code chọn đúng interpreter từ `.venv` của project
- [ ] Chạy được file `hello.py` đầu tiên

---

## Tóm tắt mental model

Sau khi đọc xong, hãy nhớ 3 ý chính sau:

1. **Python là chương trình `python.exe`** — cài lên để máy biết cách chạy file `.py`.
2. **PATH là cách Windows tìm `python.exe`** — không có PATH thì gõ `python` không ra gì.
3. **venv là hộp cô lập** — mỗi project 1 hộp, package không trộn lẫn, không bao giờ cài global.

Nắm chắc 3 ý này là đủ để không bị rối khi đọc tutorial Python sau này.