import gspread
import os
import json
from datetime import datetime
from google.oauth2.service_account import Credentials

# ========================
# 1. CONFIG
# ========================
# Dán ID bạn vừa copy vào đây (Cực kỳ quan trọng)
SPREADSHEET_ID = "1r7c1I-Km2dPngfIz9DlkmvDeCww6XzSF3S993Yu0WF0" 
WORKSHEET_NAME = "Sheet1"

# ========================
# 2. AUTH GOOGLE
# ========================
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_creds():
    service_account_json = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON')
    
    if service_account_json:
        print("Đang sử dụng credentials từ biến môi trường...")
        info = json.loads(service_account_json)
        return Credentials.from_service_account_info(info, scopes=scopes)
    
    elif os.path.exists("creds.json"):
        print("Đang sử dụng credentials từ file creds.json...")
        return Credentials.from_service_account_file("creds.json", scopes=scopes)
    
    else:
        raise ValueError("LỖI: Không tìm thấy Secret GOOGLE_CREDENTIALS trên GitHub!")

# ========================
# 3. CHƯƠNG TRÌNH CHÍNH
# ========================
def main():
    sheet = None
    try:
        creds = get_creds()
        client = gspread.authorize(creds)
        
        print(f"Đang mở Spreadsheet ID: {SPREADSHEET_ID}")
        # Sử dụng open_by_key để tránh lỗi với file .xlsx
        sh = client.open_by_key(SPREADSHEET_ID)
        sheet = sh.worksheet(WORKSHEET_NAME)
        
    except gspread.exceptions.SpreadsheetNotFound:
        print("LỖI: Không tìm thấy Sheet. Hãy kiểm tra ID và chắc chắn đã Share cho Email Service Account.")
    except Exception as e:
        print(f"Lỗi khởi tạo chi tiết: {e}")

    if sheet is None:
        return

    print("Đang ghi dữ liệu vào Google Sheet...")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [now, "VNSTOCK-CRON", "SUCCESS"]

    try:
        sheet.append_row(row)
        print(f"GHI THÀNH CÔNG lúc: {now}!")
    except Exception as e:
        print(f"Lỗi khi ghi dòng: {e}")

if __name__ == "__main__":
    main()
