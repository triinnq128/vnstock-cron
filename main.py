import gspread
import os
import json
from datetime import datetime
from google.oauth2.service_account import Credentials

# ========================
# 1. CONFIG
# ========================
SPREADSHEET_NAME = "trading_price_board_vci" 
WORKSHEET_NAME = "Sheet1"

# ========================
# 2. AUTH GOOGLE
# ========================
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_creds():
    # Ưu tiên lấy từ biến môi trường (Chạy trên GitHub Actions)
    service_account_json = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON')
    
    if service_account_json:
        print("Đang sử dụng credentials từ biến môi trường...")
        info = json.loads(service_account_json)
        return Credentials.from_service_account_info(info, scopes=scopes)
    
    # Nếu không có biến môi trường, thử tìm file vật lý (Chạy trên máy cá nhân)
    elif os.path.exists("creds.json"):
        print("Đang sử dụng credentials từ file creds.json...")
        return Credentials.from_service_account_file("creds.json", scopes=scopes)
    
    else:
        raise ValueError("LỖI: Không tìm thấy Secret GOOGLE_CREDENTIALS trên GitHub!")

# Khởi tạo client
try:
    creds = get_creds()
    client = gspread.authorize(creds)
    sheet = client.open(SPREADSHEET_NAME).worksheet(WORKSHEET_NAME)
except Exception as e:
    print(f"Lỗi khởi tạo: {e}")
    sheet = None

# ========================
# 3. CHƯƠNG TRÌNH CHÍNH
# ========================
def main():
    if sheet is None:
        return

    print("Đang ghi dữ liệu vào Google Sheet...")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row = [now, "VNSTOCK-CRON", "SUCCESS"]

    try:
        sheet.append_row(row)
        print(f"Ghi thành công lúc: {now}")
    except Exception as e:
        print(f"Lỗi khi ghi dòng: {e}")

if __name__ == "__main__":
    main()
