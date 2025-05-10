import requests
import pandas as pd
import os

# معلومات التليجرام
TOKEN = "7801456150:AAHO6AHaUUS8M6H_m_RYD-Fgzk_Mg72NiXk"
CHAT_ID = "663235772"

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("✅ تم إرسال التنبيه إلى Telegram.")
    else:
        print(f"❌ فشل الإرسال: {response.text}")

def load_entry_signals():
    path = os.path.expanduser("~/Desktop/Bot_BB4WFB/data/entry_signals.csv")
    if not os.path.exists(path):
        return None
    
    df = pd.read_csv(path)
    if df.empty:
        return None
    return df

def format_signals(df):
    msg = "📥 *إشارات دخول (Wick + FVG)*\n\n"
    for _, row in df.iterrows():
        msg += f"• `{row['symbol']}` @ {row['date']} ✅ {row['type']} ({row['note']})\n"
    return msg

if __name__ == "__main__":
    df = load_entry_signals()
    if df is not None:
        message = format_signals(df)
    else:
        message = "❌ لا توجد إشارات دخول حالياً."

    send_message(message)

