
import gspread
from google.oauth2.service_account import Credentials

# scope
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# load credentials
creds = Credentials.from_service_account_file(
    "sheet-bot.json",
    scopes=scopes
)

client = gspread.authorize(creds)

# mở file
sheet = client.open("trading_price_board_vci").sheet1

# ghi data
sheet.append_row(["Hello", "World"])
