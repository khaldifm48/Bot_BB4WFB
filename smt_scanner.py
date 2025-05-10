import pandas as pd
import os

def load_csv(symbol):
    path = f"data/{symbol}_1d.csv"
    if not os.path.exists(path):
        print(f"❌ الملف غير موجود: {path}")
        return None
    df = pd.read_csv(path)
    df.columns = [col.strip().capitalize() for col in df.columns]
    if 'Date' not in df.columns:
        print(f"⚠️ العمود 'Date' غير موجود في {path}")
        return None
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])
    df.set_index('Date', inplace=True)
    df = df.sort_index()
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')  # ✅ مهم
    return df

def find_smt_pair(base, other, restrict_last_two=False):
    if base is None or other is None:
        return False

    base_last = base.iloc[-2:] if restrict_last_two else base.iloc[-5:]
    other_last = other.iloc[-2:] if restrict_last_two else other.iloc[-5:]

    try:
        base_diff = base['Close'].iloc[-1] - base['Close'].iloc[0]
        other_diff = other['Close'].iloc[-1] - other['Close'].iloc[0]
        return base_diff * other_diff < 0
    except Exception as e:
        print(f"⚠️ SMT calculation failed: {e}")
        return False

def scan_all():
    signals = []
    base = load_csv("BTC")
    
    usdt_path = "data/usdt_dominance_data.csv"
    if not os.path.exists(usdt_path):
        print("❌ ملف USDT Dominance غير موجود.")
        return pd.DataFrame()

    usdt = pd.read_csv(usdt_path)
    usdt.columns = [col.strip().capitalize() for col in usdt.columns]
    usdt['Date'] = pd.to_datetime(usdt['Date'], errors='coerce')
    usdt = usdt.dropna(subset=['Date'])
    usdt.set_index('Date', inplace=True)
    usdt = usdt.sort_index()
    usdt['Close'] = pd.to_numeric(usdt['Close'], errors='coerce')  # ✅ مهم

    if find_smt_pair(base, usdt, restrict_last_two=True):
        signals.append({"symbol": "BTCUSDT", "type": "Bullish", "pair_used": "BTC vs USDT.D"})

    other_coins = ["ETH", "AVAX", "DOGE", "PEPE", "BNB", "XRP", "ADA", "LINK"]
    for symbol in other_coins:
        df = load_csv(symbol)
        if find_smt_pair(base, df):
            signals.append({"symbol": symbol + "USDT", "type": "Bullish", "pair_used": f"BTC vs {symbol}"})

    return pd.DataFrame(signals)

if __name__ == "__main__":
    smt_df = scan_all()

    if not smt_df.empty:
        print("✅ SMT Detected:")
        print(smt_df)
        save_path = os.path.expanduser("~/Desktop/Bot_BB4WFB/data/smt_signals.csv")
        smt_df.to_csv(save_path, index=False)
        print(f"✅ تم حفظ إشارات SMT في: {save_path}")
    else:
        print("❌ لا يوجد SMT حالياً.")

