import os
import yfinance as yf
from binance.client import Client
import pandas as pd
from datetime import datetime, timedelta

os.makedirs("data", exist_ok=True)

symbols = [
    "BTC", "ETH", "AVAX", "DOGE", "PEPE", "BNB", "XRP", "ADA", "LINK", "SOL",
    "MATIC", "ARB", "APT", "OP", "SUI", "LDO", "INJ", "GRT", "FTM", "NEAR",
    "AAVE", "SNX", "CRV", "GMX", "RPL", "DYDX", "UNI", "CAKE", "LTC", "COMP",
    "DOT", "ATOM", "TRX", "EOS", "ZIL", "ONE", "FLOW", "BAND", "CHZ", "ENJ",
    "XLM", "XTZ", "KSM", "STX", "COTI", "TWT", "FET", "RNDR", "NKN", "WOO"
]

def fetch_binance_data():
    client = Client()
    for symbol in symbols:
        base = f"{symbol}USDT"
        try:
            klines_1h = client.get_klines(symbol=base, interval=Client.KLINE_INTERVAL_1HOUR)
            df_1h = pd.DataFrame(klines_1h, columns=[
                "Time", "Open", "High", "Low", "Close", "Volume",
                "Close_time", "Quote_asset_volume", "Number_of_trades",
                "Taker_buy_base_volume", "Taker_buy_quote_volume", "Ignore"])
            df_1h["Date"] = pd.to_datetime(df_1h["Time"], unit="ms")
            df_1h.to_csv(f"data/{symbol}USDT_1h.csv", index=False)
            print(f"✅ Binance 1H data saved: data/{symbol}USDT_1h.csv")

            klines_15m = client.get_klines(symbol=base, interval=Client.KLINE_INTERVAL_15MINUTE)
            df_15m = pd.DataFrame(klines_15m, columns=[
                "Time", "Open", "High", "Low", "Close", "Volume",
                "Close_time", "Quote_asset_volume", "Number_of_trades",
                "Taker_buy_base_volume", "Taker_buy_quote_volume", "Ignore"])
            df_15m["Date"] = pd.to_datetime(df_15m["Time"], unit="ms")
            df_15m.to_csv(f"data/{symbol}USDT_15m.csv", index=False)
            print(f"✅ Binance 15m data saved: data/{symbol}USDT_15m.csv")

        except Exception as e:
            print(f"❌ Error fetching {symbol}: {e}")

def fetch_usdt_dominance():
    file_path = "data/usdt_dominance_data.csv"
    if os.path.exists(file_path):
        try:
            df_old = pd.read_csv(file_path)
            last_date = pd.to_datetime(df_old['Date'].iloc[-1])
            if last_date.date() == datetime.now().date():
                print("⏩ USDT Dominance already updated today.")
                return
        except Exception as e:
            print(f"⚠️ Error reading existing USDT Dominance file: {e}")

    try:
        df = yf.download("USDT-USD", interval="1d")
        if not df.empty:
            df.reset_index(inplace=True)
            df.to_csv(file_path, index=False)
            print("✅ USDT Dominance data saved.")
        else:
            print("⚠️ No data returned for USDT-USD")
    except Exception as e:
        print(f"❌ فشل تحميل USDT Dominance: {e}")

fetch_binance_data()
fetch_usdt_dominance()

