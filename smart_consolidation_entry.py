import os
import pandas as pd
from datetime import datetime, timedelta
import requests

# بيانات التليجرام
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

from fcm_notifier import send_fcm_notification
send_fcm_notification("🚨 إشارة جديدة", "تم رصد فرصة جديدة من WSF_Bot ✅")

def load_csv(symbol):
    path = f"data/{symbol}_15m.csv"
    if not os.path.exists(path):
        print(f"❌ البيانات غير موجودة: {path}")
        return None
    df = pd.read_csv(path)
    df.columns = [col.strip().capitalize() for col in df.columns]
    if 'Date' not in df.columns or 'Close' not in df.columns:
        print(f"❌ تنسيق غير صالح في الملف: {path}")
        return None
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
    df = df.set_index("Date")
    df = df.sort_index()
    return df

def is_consolidating(df, hours=6, max_range=0.5):
    recent_data = df.last(f"{hours}h")
    if len(recent_data) < 5:
        return False, 0
    high = recent_data["High"].max()
    low = recent_data["Low"].min()
    perc_range = ((high - low) / low) * 100
    return perc_range < max_range, perc_range

def detect_sweep(df):
    last_candle = df.iloc[-1]
    second_last = df.iloc[-2]
    return last_candle["Low"] < second_last["Low"]

def detect_rejection_block(df):
    last = df.iloc[-1]
    body = abs(last["Close"] - last["Open"])
    wick = last["High"] - last["Low"]
    return wick > 2 * body and last["Close"] > last["Open"]

symbols = ["BTCUSDT", "AVAXUSDT"]

for symbol in symbols:
    df = load_csv(symbol)
    if df is None:
        continue

    cons, perc = is_consolidating(df, hours=6, max_range=0.6)

    if cons:
        sweep = detect_sweep(df)
        rejection = detect_rejection_block(df)

        if sweep and rejection:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            msg = f"""
📊 <b>فرصة دخول ذكية</b>

<b>📈 الزوج:</b> {symbol}
<b>⏰ الفريم:</b> 15m
<b>📦 Consolidation:</b> تم رصده لمدة 6 ساعات (نطاق: {perc:.2f}%)
<b>⚡ Sweep:</b> قاع تم كسره للتو
<b>🧱 Rejection Block:</b> تم تأكيده ✅
<b>📅 التوقيت:</b> {now}

#WSF #SmartEntry #{symbol}
"""
            send_telegram_alert(msg)

