import ccxt
import pandas as pd
import os
from datetime import datetime

# قائمة العملات المطلوبة
symbols = [
    "BTC/USDT", "ETH/USDT", "AVAX/USDT", "DOGE/USDT", "PEPE/USDT", "BNB/USDT",
    "XRP/USDT", "ADA/USDT", "LINK/USDT", "SOL/USDT", "MATIC/USDT", "ARB/USDT",
    "APT/USDT", "OP/USDT", "SUI/USDT", "LDO/USDT", "INJ/USDT", "GRT/USDT",
    "FTM/USDT", "NEAR/USDT", "AAVE/USDT", "SNX/USDT", "CRV/USDT", "GMX/USDT",
    "RPL/USDT", "DYDX/USDT", "UNI/USDT", "CAKE/USDT", "LTC/USDT", "COMP/USDT",
    "DOT/USDT", "ATOM/USDT", "TRX/USDT", "EOS/USDT", "ZIL/USDT", "ONE/USDT",
    "FLOW/USDT", "BAND/USDT", "CHZ/USDT", "ENJ/USDT", "XLM/USDT", "XTZ/USDT",
    "KSM/USDT", "STX/USDT", "COTI/USDT", "TWT/USDT", "FET/USDT", "RNDR/USDT", "NKN/USDT", "WOO/USDT"
]

# تهيئة Binance
binance = ccxt.binance()
os.makedirs("data", exist_ok=True)

# تحميل OHLCV
def fetch_ohlcv(symbol, timeframe="1h", limit=200):
    try:
        ohlcv = binance.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df[["date", "open", "high", "low", "close", "volume"]]
    except Exception as e:
        print(f"❌ Error loading {symbol} @ {timeframe}: {e}")
        return None

# تنزيل البيانات لكل فريم
for symbol in symbols:
    base = symbol.replace("/", "")
    for tf in ["1d", "4h", "1h", "15m"]:
        df = fetch_ohlcv(symbol, tf)
        if df is not None:
            filename = f"data/{base}_{tf}.csv"
            df.to_csv(filename, index=False)
            print(f"✅ Saved: {filename}")

