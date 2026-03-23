import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials

# ========================
# 1. CONFIG
# ========================

SPREADSHEET_NAME = "trading_price_board_vci"  # ⚠️ sửa lại
WORKSHEET_NAME = "Sheet1"

# ========================
# 2. AUTH GOOGLE
# ========================

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "google_credentials.json",
    scopes=scopes
)

client = gspread.authorize(creds)

# ========================
# 3. OPEN SHEET
# ========================

sheet = client.open(SPREADSHEET_NAME).worksheet(WORKSHEET_NAME)

# ========================
# 4. TEST WRITE
# ========================

def main():
    print("Start test Google Sheet...")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row = [
        now,
        "TEST",
        "OK"
    ]

    sheet.append_row(row)

    print("Write success!")

# ========================
# 5. RUN
# ========================

if __name__ == "__main__":
    main()
