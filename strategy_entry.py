import os
import pandas as pd
from datetime import datetime
import requests

TELEGRAM_TOKEN = "7801456150:AAHO6AHaUUS8M6H_m_RYD-Fgzk_Mg72NiXk"
CHAT_ID = "663235772"

# إرسال التنبيه

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

# تحميل بيانات 4H

def load_4h(symbol):
    path = f"data/{symbol}USDT_4h.csv"
    if not os.path.exists(path):
        return None
    df = pd.read_csv(path)
    df.columns = [col.strip().capitalize() for col in df.columns]
    if 'Date' not in df.columns or 'Close' not in df.columns:
        return None
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])
    df = df.sort_values(by='Date')
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    df['Low'] = pd.to_numeric(df['Low'], errors='coerce')
    df['High'] = pd.to_numeric(df['High'], errors='coerce')
    df['Open'] = pd.to_numeric(df['Open'], errors='coerce')
    return df

# تحقق من Wick + FVG + Liquidity Void + BBR

def detect_entry(df):
    last = df.tail(5)
    wick = last.iloc[-2]
    fvg = last.iloc[-1]

    wick_body = abs(wick['Close'] - wick['Open'])
    wick_range = wick['High'] - wick['Low']
    has_wick = wick_range > wick_body * 2

    fvg_gap = (fvg['Low'] > wick['High'])

    liquidity_void = (df['Low'].iloc[-4] > wick['High']) and (df['Low'].iloc[-3] > wick['High'])

    bbr_detected = (df['High'].iloc[-3] < df['High'].iloc[-2]) and (df['Low'].iloc[-2] > df['Low'].iloc[-1])

    return has_wick and fvg_gap and liquidity_void and bbr_detected

# العملات المختارة (مثلاً فقط BTC حالياً)
symbols = ["BTC"]

for symbol in symbols:
    df = load_4h(symbol)
    if df is None:
        continue
    if detect_entry(df):
else:
    print(f"❌ لا توجد فرص حالياً على {symbol}USDT")
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        msg = f"""
🚨 <b>إشارة دخول استراتيجية (مدى بعيد)</b> 🚨

<b>📌 العملة:</b> {symbol}USDT
<b>⏰ الفاصل الزمني:</b> 4H
<b>📅 التاريخ:</b> {now}

──────────────
🧠 <b>نموذج الدخول:</b>
✅ Wick يسحب سيولة واضحة
✅ FVG مباشرة بعده
✅ Liquidity Void خلف الويك
✅ BBR (تقاطع FVG داخل FVG)

📈 <b>نوع الصفقة:</b> شراء (LONG)
📍 الدخول من قاعدة FVG
🎯 الهدف: +3R أو أقرب OB
──────────────
⚠️ Weekly Bias: صعود ✅
"""
        send_telegram_alert(msg)
        print(f"✅ إرسال تنبيه 4H لـ {symbol}USDT")

