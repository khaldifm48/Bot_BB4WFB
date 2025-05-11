import pandas as pd
import os

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
smt_path = os.path.join(data_dir, "smt_signals.csv")

if not os.path.exists(smt_path):
    print("❌ ملف إشارات SMT غير موجود.")
    exit()

smt_signals = pd.read_csv(smt_path)

if smt_signals.empty:
    print("❌ لا توجد إشارات SMT حالياً.")
    exit()

symbols = smt_signals['symbol'].unique()
found = False

for symbol in symbols:
    file_path = os.path.join(data_dir, f"{symbol}_4h.csv")
    if not os.path.exists(file_path):
        print(f"❌ البيانات غير موجودة: {file_path}")
        continue

    df = pd.read_csv(file_path)
    df.columns = [col.strip().lower() for col in df.columns]
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])

    if len(df) < 20:
        continue

    # نأخذ آخر شمعتين
    prev = df.iloc[-2]
    curr = df.iloc[-1]

    # Wick: سحب سيولة من الأعلى
    wick = float(prev['high']) - float(prev['close']) > (float(prev['high']) - float(prev['low'])) * 0.5

    # FVG: شمعة جديدة فتحت فوق أعلى قمة
    fvg = float(curr['open']) > float(prev['high'])

    # Liquidity Void: قاع الشمعة الجديدة أعلى من قاع السابقة
    liquidity_void = float(curr['low']) > float(prev['low'])

    if wick and fvg and liquidity_void:
        found = True
        print(f"✅ إشارة دخول على {symbol}")
    else:
        print(f"⚠️ لا يوجد نموذج واضح على {symbol}")

if not found:
    print("❌ لا توجد إشارات دخول حالياً.")

