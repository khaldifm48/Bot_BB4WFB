import os
import pandas as pd
from datetime import datetime
import requests

TELEGRAM_TOKEN = "7801456150:AAHO6AHaUUS8M6H_m_RYD-Fgzk_Mg72NiXk"
CHAT_ID = "663235772"

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"❌ Telegram Error: {e}")

def load_price_data(symbol):
    path = f"data/{symbol}USDT_15m.csv"
    if not os.path.exists(path):
        print(f"❌ البيانات غير موجودة: {path}")
        return None
    df = pd.read_csv(path)
    df.columns = [c.strip().capitalize() for c in df.columns]
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])
    df = df.sort_values(by='Date')
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    df['Low'] = pd.to_numeric(df['Low'], errors='coerce')
    df['High'] = pd.to_numeric(df['High'], errors='coerce')
    return df

def detect_consolidation(df, lookback=24):
    recent = df.tail(lookback)
    if recent['Close'].max() == 0 or recent['Close'].min() == 0:
        return False
    range_pct = (recent['Close'].max() - recent['Close'].min()) / recent['Close'].min()
    return range_pct < 0.015

def detect_sweep(df):
    lows = df['Low'].tail(5)
    return lows.iloc[-1] < lows.min()

def detect_rejection_block(df):
    last = df.iloc[-1]
    body = abs(last['Close'] - last['Open'])
    wick = last['High'] - max(last['Close'], last['Open'])
    return wick > 2 * body

def check_entry_conditions(symbol):
    df = load_price_data(symbol)
    if df is None or len(df) < 30:
        return False
    in_consolidation = detect_consolidation(df)
    has_sweep = detect_sweep(df)
    rejection = detect_rejection_block(df)
    return in_consolidation and has_sweep and rejection

def main():
    smt_path = "data/smt_signals.csv"
    if not os.path.exists(smt_path):
        print("❌ ملف إشارات SMT غير موجود.")
        return

    smt_df = pd.read_csv(smt_path)
    if smt_df.empty:
        print("❌ لا توجد إشارات SMT حالياً.")
        return

    for _, row in smt_df.iterrows():
        symbol = row['symbol'].strip().upper().replace("USDT", "")
        entry_ok = check_entry_conditions(symbol)
        if entry_ok:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            msg = f"""
📊 <b>فرصة دخول ذكية</b>

<b>⏱️ الفريم:</b> 15m
<b>📈 العملة:</b> {symbol}USDT
<b>📅 التوقيت:</b> {now}

✅ Consolidation ملحوظ
✅ حصل Sweep للقاع
✅ تأكيد Rejection Block موجود

📌 مؤكد من إشارات SMT السابقة
#WSF #Entry #{symbol}USDT
"""
            send_telegram_alert(msg)
        else:
            print(f"⛔️ لم تتحقق الشروط على {symbol}.")

if __name__ == "__main__":
    main()

