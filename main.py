import gspread
import os
import json
import pandas as pd
from datetime import datetime
from google.oauth2.service_account import Credentials
from vnstock import register_user, Trading

# ========================
# 1. CONFIG & AUTH VNSTOCK
# ========================
# Lấy API Key từ Secret của GitHub (như đã làm với Google Credentials)
API_KEY = os.environ.get('API_KEY_STOCK') 
register_user(API_KEY)

SPREADSHEET_ID = "1r7c1I-Km2dPngfIz9DlkmvDeCww6XzSF3S993Yu0WF0" 
WORKSHEET_NAME = "Sheet1"

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_google_creds():
    service_account_json = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON')
    if service_account_json:
        info = json.loads(service_account_json)
        return Credentials.from_service_account_info(info, scopes=scopes)
    elif os.path.exists("creds.json"):
        return Credentials.from_service_account_file("creds.json", scopes=scopes)
    else:
        raise ValueError("Không tìm thấy Google Credentials!")

# ========================
# 2. LẤY DỮ LIỆU CHỨNG KHOÁN
# ========================
def get_stock_data():
    print("🚀 Đang lấy dữ liệu từ vnstock...")
    trading = Trading(source='VCI')
    symbols = [
        'ACB','BID','BMP','BVH','DGC','DXG','FPT','GAS','GMD','HDB','HPG','HVN','IDC','KBC','KDH','MBB','MSN','MWG','NT2','POW','PTB','PVD',
        'PVI','PVS','SAB','SCS','SHB','SIP','SSI','STB','TCB','VCB','VHC','VNM','VPB','VIC', 'LPB','VHM','MCH','VJC','CTG','VCK','EIB','VIX','VND'
    ]
    
    df = trading.price_board(symbols_list=symbols)
    
    # Xử lý Multi-index columns
    df.columns = [f"{lvl0}_{lvl1}" for lvl0, lvl1 in df.columns]
    
    # Chọn các cột cần dùng
    cols = [
        'listing_symbol','listing_organ_name', 'listing_ceiling','listing_floor','listing_ref_price',
        "match_match_price",'listing_stock_type','listing_exchange','listing_trading_status',
        'listing_trading_date','listing_listed_share','listing_sending_time',
        'match_accumulated_value','match_accumulated_volume',
    ]
    
    df = df.loc[:, df.columns.intersection(cols)]
    
    # Chuyển đổi các giá trị NaN/NaT thành chuỗi rỗng để gspread không bị lỗi
    df = df.fillna("")
    return df

# ========================
# 3. CHƯƠNG TRÌNH CHÍNH
# ========================
def main():
    try:
        # 1. Khởi tạo Google Sheet
        creds = get_google_creds()
        client = gspread.authorize(creds)
        sh = client.open_by_key(SPREADSHEET_ID)
        worksheet = sh.worksheet(WORKSHEET_NAME)

        # 2. Lấy dữ liệu chứng khoán
        df = get_stock_data()

        # 3. XÓA DỮ LIỆU CŨ VÀ GHI MỚI
        print(f"🧹 Đang xóa dữ liệu cũ trong {WORKSHEET_NAME}...")
        worksheet.clear() # Xóa sạch nội dung và định dạng cũ

        # 4. Ghi tiêu đề (Header)
        header = df.columns.tolist()
        # 5. Ghi dữ liệu (Data)
        data = df.values.tolist()
        
        # Ghi cả header và data bắt đầu từ ô A1
        worksheet.update('A1', [header] + data)
        
        print(f"✅ Ghi thành công {len(df)} dòng lúc {datetime.now()}!")

    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    main()
