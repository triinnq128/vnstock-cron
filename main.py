import gspread
import os
import json
from datetime import datetime
from google.oauth2.service_account import Credentials

# ========================
# 1. CONFIG
# ========================

SPREADSHEET_NAME = "trading_price_board_vci"  # Đảm bảo tên này khớp chính xác với Google Sheet của bạn
WORKSHEET_NAME = "Sheet1"

# ========================
# 2. AUTH GOOGLE (Sử dụng Biến môi trường)
# ========================

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Lấy nội dung JSON từ biến môi trường thay vì đọc file vật lý
service_account_json = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON')

if not service_account_json:
    # Nếu chạy ở máy cá nhân mà chưa có biến môi trường, code sẽ thử tìm file .json
    if os.path.exists("GOOGLE_CREDENTIALS.json"):
        creds = Credentials.from_service_account_file("GOOGLE_CREDENTIALS.json", scopes=scopes)
    else:
        raise ValueError("LỖI: Không tìm thấy biến môi trường GOOGLE_SERVICE_ACCOUNT_JSON hoặc file JSON!")
else:
    # Nếu chạy trên GitHub Actions, nó sẽ dùng biến môi trường
    service_account_info = json.loads(service_account_json)
    creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)

client = gspread.authorize(creds)

# ========================
# 3. OPEN SHEET
# ========================

# Để an toàn hơn, chúng ta nên mở sheet bên trong hàm main hoặc dùng try-except
try:
    sheet = client.open(SPREADSHEET_NAME).worksheet(WORKSHEET_NAME)
except Exception as e:
    print(f"Lỗi khi mở Google Sheet: {e}")
    sheet = None

# ========================
# 4. TEST WRITE
# ========================

def main():
    if not sheet:
        print("Không thể kết nối tới Google Sheet. Vui lòng kiểm tra quyền chia sẻ (Share) cho Email Service Account.")
        return

    print("Start test Google Sheet...")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row = [
        now,
        "TEST",
        "OK"
    ]

    try:
        sheet.append_row(row)
        print(f"Write success at {now}!")
    except Exception as e:
        print(f"Lỗi khi ghi dữ liệu: {e}")

# ========================
# 5. RUN
# ========================

if __name__ == "__main__":
    main()
