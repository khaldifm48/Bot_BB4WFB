import os
import pandas as pd
from datetime import datetime
import requests

# ✅ بيانات التليجرام
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
    path = f"data/{symbol}USDT_1h.csv"
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
    return df

def calculate_slope(df, length=5):
    last = df['Close'].iloc[-length:]
    if last.isnull().any():
        return 0
    return (last.iloc[-1] - last.iloc[0]) / length

def check_smt_general(btc_df, alt_df):
    btc_slope = calculate_slope(btc_df)
    alt_slope = calculate_slope(alt_df)
    return btc_slope * alt_slope < 0  # دايفرجنسي إذا الاتجاهات عكس بعض

def check_smt_usdt(btc_df, usdt_df):
    btc = btc_df['Close'].iloc[-2:]
    usdt = usdt_df['Close'].iloc[-2:]
    if btc.isnull().any() or usdt.isnull().any():
        return False
    return (btc.iloc[-1] - btc.iloc[0]) * (usdt.iloc[-1] - usdt.iloc[0]) < 0

# ✅ قائمة العملات
symbols = [
    "ETH", "AVAX", "DOGE", "PEPE", "BNB", "XRP", "ADA", "LINK", "SOL",
    "MATIC", "ARB", "APT", "OP", "SUI", "LDO", "INJ", "GRT", "FTM", "NEAR",
    "AAVE", "SNX", "CRV", "GMX", "RPL", "DYDX", "UNI", "CAKE", "LTC", "COMP",
    "DOT", "ATOM", "TRX", "EOS", "ZIL", "ONE", "FLOW", "BAND", "CHZ", "ENJ",
    "XLM", "XTZ", "KSM", "STX", "COTI", "TWT", "FET", "RNDR", "NKN", "WOO"
]

btc = load_csv("BTC")
usdt = load_csv("USDT")

if btc is None:
    print("❌ لا يمكن تحميل BTC")
    exit()

# 🔁 SMT مع USDT Dominance (آخر شمعتين فقط)
if usdt is not None and check_smt_usdt(btc, usdt):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    msg = f"""
🚨 <b>SMT Detected</b> 🚨

<b>⏰ الفريم:</b> 1H
<b>📊 الانفصال:</b> BTC ↔️ USDT Dominance
<b>📅 التاريخ:</b> {now}

🔁 تم رصد Divergence سريع بين BTC و USDT.D على آخر شمعتين
📌 سيتم مراقبة فرص الدخول على فريم 15m...

#WSF #SMT #BTCUSDT
"""
    send_telegram_alert(msg)

# 🔁 SMT مع باقي العملات
for symbol in symbols:
    alt = load_csv(symbol)
    if alt is None:
        continue
    if check_smt_general(btc, alt):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        msg = f"""
🚨 <b>SMT Detected</b> 🚨

<b>⏰ الفريم:</b> 1H
<b>📊 الانفصال:</b> BTC ↔️ {symbol}
<b>📅 التاريخ:</b> {now}

📈 تم رصد Divergence واضح بناءً على ميل الحركة.
📌 سيتم تحليل 15m لاكتشاف دخول ذكي.

#WSF #SMT #{symbol}USDT
"""
        send_telegram_alert(msg)
        print(f"✅ SMT مع {symbol} تم اكتشافه.")

