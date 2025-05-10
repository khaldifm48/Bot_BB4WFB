import pandas as pd
import os
from datetime import timedelta

# تحديد مجلد البيانات
DATA_DIR = "data"
SIGNAL_FILE = os.path.join(DATA_DIR, "smt_signals.csv")

# تحديد مدة الكونسلديشن (مثلاً 6 ساعات)
CONSOLIDATION_HOURS = 6

def is_consolidating(df, threshold=0.3):
    """
    يتحقق إذا كانت العملة تتحرك ضمن نطاق ضيق لفترة معينة (تُعتبر Consolidation)
    """
    recent = df[-int(CONSOLIDATION_HOURS * 4):]  # عدد شموع 15 دقيقة في 6 ساعات
    high = recent["high"].max()
    low = recent["low"].min()
    change_percent = ((high - low) / low) * 100
    return change_percent < threshold, change_percent

def detect_consolidation():
    if not os.path.exists(SIGNAL_FILE):
        print("❌ ملف إشارات SMT غير موجود.")
        return

    smt_df = pd.read_csv(SIGNAL_FILE)
    entries = []

    for _, row in smt_df.iterrows():
        symbol = row["symbol"]
        pair = symbol.replace("USDT", "")  # مثال: AVAXUSDT → AVAX
        file_path = os.path.join(DATA_DIR, f"{pair}USDT_15m.csv")

        if not os.path.exists(file_path):
            print(f"❌ بيانات {symbol} غير موجودة.")
            continue

        df = pd.read_csv(file_path)
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])
        df.set_index("Date", inplace=True)
        df.columns = [col.lower().strip() for col in df.columns]

        cond, pct = is_consolidating(df)
        if cond:
            entries.append((symbol, round(pct, 2)))
            print(f"✅ {symbol} في Consolidation ({round(pct, 2)}%)")

    if not entries:
        print("❌ لا توجد فرص Consolidation حالياً.")
    else:
        print("\n📊 فرص دخول ممكنة:")
        for sym, pct in entries:
            print(f"• {sym} ({pct}%)")

if __name__ == "__main__":
    detect_consolidation()

