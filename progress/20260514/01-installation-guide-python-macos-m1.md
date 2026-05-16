# Cài đặt Python 3.12+ trên macOS M1 Pro — Từ con số 0

> Tài liệu này dành cho người **chưa biết gì về Python**. Mỗi bước đều giải thích **"tại sao làm"** chứ không chỉ "làm thế nào".

---

## 0. Hiểu trước khi cài: Python là gì? Mình đang cài cái gì?

**Python** là một ngôn ngữ lập trình. Khi bạn viết code Python (file `.py`), máy tính không hiểu trực tiếp — cần một chương trình **"phiên dịch"** đọc file đó rồi chạy. Chương trình phiên dịch đó gọi là **Python interpreter** (`python3`).

→ **"Cài Python" = cài chương trình `python3` lên máy.**

Cài xong, mỗi khi bạn gõ `python3 tenfile.py` trong terminal, macOS sẽ gọi `python3` để chạy file đó.

### Vì sao chọn version 3.12+?

Python có 2 nhánh lớn: Python 2 (đã chết, không support nữa) và Python 3 (đang dùng). Trong Python 3, mỗi năm ra 1 version mới (3.10, 3.11, 3.12, 3.13...). Version mới nhanh hơn, có syntax mới, fix bug.

→ **Chọn 3.12+ vì đó là version stable hiện đại, tài liệu/thư viện đều support.**

### M1 Pro là chip gì? Có khác gì không?

Mac M1 Pro dùng chip **ARM (Apple Silicon)** — khác với chip Intel (x86) trên Mac cũ và Windows. Điều này quan trọng vì:

- Một số thư viện Python cũ chưa có bản ARM native → chạy chậm hơn hoặc lỗi.
- **Homebrew** và **Python từ python.org** đều đã có bản ARM native cho M1 — không lo.
- Khi cài đúng cách, Python chạy **nhanh hơn** trên M1 so với Intel Mac.

---

## 1. Chuẩn bị: Homebrew — Package manager cho macOS

Trên macOS, không có "file .exe" như Windows để cài Python. Cách được khuyến nghị là dùng **Homebrew** — package manager phổ biến nhất cho Mac.

**Homebrew là gì?** Giống như App Store nhưng cho developer, dùng terminal. Gõ 1 lệnh là cài được Python, Git, Node... Homebrew quản lý cập nhật và phụ thuộc giúp bạn.

### Kiểm tra Homebrew đã có chưa

Mở **Terminal** (Spotlight: `Cmd+Space`, gõ "Terminal"), chạy:

```bash
brew --version
```

Nếu thấy `Homebrew x.x.x` → đã có, bỏ qua bước cài Homebrew.

### Cài Homebrew (nếu chưa có)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Lệnh này sẽ:
1. Tải script cài đặt từ GitHub
2. Hỏi password máy (nhập bình thường, terminal không hiện ký tự khi gõ password — đó là bình thường)
3. Tự cài **Xcode Command Line Tools** nếu chưa có (cần cho nhiều tool dev)

**Sau khi cài xong**, Homebrew sẽ in hướng dẫn thêm vào PATH. **Làm theo đúng hướng dẫn đó** — thường là:

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

> ⚠️ **Chú ý đường dẫn `/opt/homebrew`**: Đây là đường dẫn của Homebrew trên M1. Mac Intel dùng `/usr/local/homebrew` — khác nhau, đừng nhầm nếu đọc tài liệu cũ.

Kiểm tra lại:

```bash
brew --version
```

---

## 2. Cài Python qua Homebrew

```bash
brew install python@3.12
```

Homebrew sẽ tải và cài Python 3.12 bản **ARM native** — tối ưu cho M1.

Sau khi cài xong, kiểm tra:

```bash
python3 --version
pip3 --version
```

Output mong đợi:

```
Python 3.12.x
pip 24.x.x from /opt/homebrew/lib/python3.12/site-packages/pip (python 3.12)
```

### Tại sao là `python3` không phải `python`?

macOS có sẵn một Python 2 cũ ở `/usr/bin/python` (hoặc stub). Để không đè lên hệ thống, Homebrew đặt Python 3 là `python3`. Bạn có thể tạo alias nếu muốn gõ ngắn hơn (xem phần cuối).

---

## 3. PATH là gì? Tại sao quan trọng?

**PATH** là danh sách các thư mục mà macOS sẽ tìm khi bạn gõ một lệnh trong terminal. Ví dụ gõ `python3`, macOS sẽ duyệt qua từng thư mục trong PATH để tìm file tên `python3`. Nếu Python không nằm trong PATH, gõ `python3` sẽ báo **"command not found"**.

Homebrew đã tự thêm Python vào PATH khi cài — đó là lý do bước trên cần chạy lệnh `eval "$(/opt/homebrew/bin/brew shellenv)"`.

Kiểm tra Python đang được load từ đâu:

```bash
which python3
```

Output đúng: `/opt/homebrew/bin/python3`

Nếu thấy `/usr/bin/python3` → đang dùng bản hệ thống, không phải bản vừa cài → kiểm tra lại PATH.

---

## 4. pip là gì? Tại sao cần upgrade?

**pip** là **package manager** của Python — công cụ để **cài thư viện** (code của người khác viết sẵn) về máy.

Ví dụ: muốn gọi API HTTP, không phải tự code từ đầu — chỉ cần `pip3 install requests` là có ngay thư viện `requests` để dùng.

pip được cài kèm Python, nhưng thường là version cũ. Upgrade lên bản mới:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade setuptools wheel
```

Giải thích lệnh:
- `python3 -m pip` = "chạy module pip thông qua Python" — cách an toàn nhất, tránh nhầm version pip nếu máy có nhiều Python.
- `setuptools`, `wheel` — 2 thư viện nền tảng giúp việc cài package khác trơn tru hơn.

---

## 5. venv (virtual environment) — Khái niệm quan trọng nhất khi mới học

### Vấn đề nếu không dùng venv

Mặc định, khi `pip3 install requests`, thư viện sẽ cài **global** (cài chung cho toàn máy). Vấn đề xảy ra khi:

- Project A cần `requests` version 2.28
- Project B cần `requests` version 2.31

→ Cài cái này thì cái kia chạy sai. **Conflict dependency** là vấn đề kinh điển của Python.

### venv giải quyết thế nào?

`venv` = tạo một **"hộp Python riêng"** cho mỗi project. Mỗi project có 1 folder `.venv` chứa Python interpreter và thư viện riêng. Cài gì vào đây chỉ ảnh hưởng project đó, không đụng tới các project khác.

**Quy tắc cần khắc cốt ghi tâm: mỗi project 1 venv riêng, không bao giờ cài package vào Python global.**

### Cách dùng venv trên macOS

```bash
# 1. Tạo folder project
mkdir my-project
cd my-project

# 2. Tạo venv — câu lệnh này tạo ra folder .venv chứa Python "riêng"
python3 -m venv .venv

# 3. Activate venv — "bước vào" hộp riêng của project
source .venv/bin/activate
```

Khi activate thành công, terminal sẽ có prefix `(.venv)` ở đầu dòng:

```
(.venv) macbook@MacBook-Pro my-project %
```

Lúc này gõ `pip install requests` → thư viện chỉ cài vào `.venv` của project này, không cài ra ngoài.

Khi xong việc, thoát venv:

```bash
deactivate
```

> **Khác với Windows**: Trên macOS không có vấn đề "execution policy" như PowerShell. Lệnh `source .venv/bin/activate` chạy được ngay, không cần cấu hình thêm.

---

## 6. Cài IDE — Editor để viết code

**IDE** (Integrated Development Environment) = phần mềm để viết code, có syntax highlight, autocomplete, debug...

Khuyến nghị **VS Code** — miễn phí, nhẹ, phổ biến nhất hiện nay.

Tải tại: <https://code.visualstudio.com/>

Khi cài trên M1, tải bản **Apple Silicon** (không phải Intel) để chạy native, nhanh hơn.

Cài xong, mở VS Code → vào tab **Extensions** (icon 4 ô vuông bên trái, hoặc `Cmd+Shift+X`), cài:

- **Python** (publisher: Microsoft) — support cơ bản: chạy code, debug
- **Pylance** (Microsoft) — autocomplete thông minh, gợi ý type
- **Ruff** (Astral Software) — bắt lỗi và format code tự động

### Cài VS Code command line tool

Để mở folder trong VS Code từ terminal bằng lệnh `code .`:

1. Mở VS Code
2. Bấm `Cmd+Shift+P` (mở Command Palette)
3. Gõ `Shell Command: Install 'code' command in PATH`
4. Bấm Enter

Sau đó từ terminal có thể gõ `code ten-folder` để mở trực tiếp.

### Quan trọng: Cho VS Code biết dùng venv nào

Mỗi project có venv riêng → phải bảo VS Code dùng đúng venv của project đó:

1. Mở folder project trong VS Code (`code my-project`)
2. Bấm `Cmd+Shift+P` (mở Command Palette)
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

```bash
python3 hello.py
```

Nếu nó hỏi tên rồi in lời chào → setup xong. 🎉

---

## 8. (Tùy chọn) Tạo alias `python` → `python3`

Nếu muốn gõ `python` thay vì `python3`, thêm alias vào shell config:

```bash
echo 'alias python=python3' >> ~/.zshrc
echo 'alias pip=pip3' >> ~/.zshrc
source ~/.zshrc
```

Sau đó `python --version` sẽ hoạt động như `python3 --version`.

> **Lưu ý**: File config là `~/.zshrc` vì macOS mặc định dùng **zsh** từ macOS Catalina trở lên. Nếu bạn đang dùng bash thì file là `~/.bash_profile`.

---

## 9. Tool nên biết (chưa cần cài ngay, học sau)

| Tool | Mục đích | Khi nào cần |
|------|----------|-------------|
| `uv` | Thay thế pip + venv, nhanh hơn 10-100x | Khi đã quen, muốn workflow hiện đại |
| `ruff` | Linter (bắt lỗi style) + formatter | Khi bắt đầu viết code dài, cần code sạch |
| `mypy` | Kiểm tra type tĩnh | Khi học type hints, viết code lớn |
| `pytest` | Viết unit test | Khi học testing |
| `ipython` | REPL nâng cao (gõ code thử nhanh) | Khi cần thử nghiệm code lẻ |

---

## Checklist hoàn thành

Sau khi xong, bạn phải làm được hết những điều sau:

- [ ] Hiểu **Python interpreter là gì**, mình đã cài cái gì lên máy
- [ ] `python3 --version` ra version 3.12+ ở bất kỳ terminal nào
- [ ] `pip3 --version` chạy được
- [ ] `which python3` trả về `/opt/homebrew/bin/python3` (không phải `/usr/bin/python3`)
- [ ] Hiểu **PATH là gì** và tại sao phải cấu hình sau khi cài Homebrew
- [ ] Hiểu **venv là gì** và tại sao mỗi project cần venv riêng
- [ ] Tự tạo được venv, activate được (`source .venv/bin/activate`), thoát được (`deactivate`)
- [ ] VS Code chọn đúng interpreter từ `.venv` của project
- [ ] Chạy được file `hello.py` đầu tiên

---

## Tóm tắt mental model

Sau khi đọc xong, hãy nhớ 3 ý chính sau:

1. **Python là chương trình `python3`** — cài qua Homebrew để máy biết cách chạy file `.py`.
2. **PATH là cách macOS tìm `python3`** — Homebrew tự thêm vào, nhưng phải chạy lệnh `eval` sau khi cài.
3. **venv là hộp cô lập** — mỗi project 1 hộp, package không trộn lẫn, không bao giờ cài global.

Nắm chắc 3 ý này là đủ để không bị rối khi đọc tutorial Python sau này.
