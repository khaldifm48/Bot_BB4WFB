import os
import pandas as pd
from datetime import datetime
import requests

# ✅ إعدادات التليغرام
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

def load_csv(symbol):
    path = f"data/{symbol}_4h.csv"
    if not os.path.exists(path):
        print(f"❌ البيانات غير موجودة: {path}")
        return None
    df = pd.read_csv(path)
    df.columns = [col.strip().capitalize() for col in df.columns]
    if 'Date' not in df.columns or 'Close' not in df.columns:
        return None
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
    df = df.set_index("Date")
    df = df.sort_index()
    return df

def detect_entry(df):
    last = df.iloc[-1]
    prev = df.iloc[-2]

    wick_size = (last["High"] - last["Low"]) > 2 * abs(last["Close"] - last["Open"])
    fvg = abs(last["Open"] - prev["Close"]) > 0.001 * prev["Close"]
    body_above_mid = last["Close"] > (last["High"] + last["Low"]) / 2
    return wick_size and fvg and body_above_mid

def check_bbr(df):
    if len(df) < 3:
        return False
    a, b, c = df.iloc[-3], df.iloc[-2], df.iloc[-1]
    return (a["High"] < b["Low"]) and (b["Low"] > c["High"])

symbols = ["BTCUSDT", "AVAXUSDT"]

for symbol in symbols:
    df = load_csv(symbol)
    if df is None or len(df) < 3:
        continue

    if detect_entry(df) or check_bbr(df):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        msg = f"""
📊 <b>فرصة دخول 4H</b>

<b>📈 الزوج:</b> {symbol}
<b>⏰ الفريم:</b> 4H
<b>🕯️ النموذج:</b> Wick + FVG
<b>🔁 تأكيد BBR:</b> {"✅" if check_bbr(df) else "❌"}
<b>📅 التوقيت:</b> {now}

#WSF #FVG #BBR #{symbol}
"""
        send_telegram_alert(msg)

