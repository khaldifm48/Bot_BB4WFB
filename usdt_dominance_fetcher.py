import pandas as pd
import datetime
import requests
from io import StringIO

def fetch_usdt_dominance():
    # Yahoo Finance CSV URL لـ USDT Dominance
    url = "https://query1.finance.yahoo.com/v7/finance/download/CRYPTOCAP:USDT.D?period1=1609459200&period2=9999999999&interval=1d&events=history"

    try:
        response = requests.get(url)
        response.raise_for_status()

        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)

        # حفظ آخر 10 أيام فقط من البيانات
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values(by='Date', ascending=False).head(10)

        df.to_csv("usdt_dominance_data.csv", index=False)
        print("✅ تم حفظ بيانات USDT Dominance بنجاح في usdt_dominance_data.csv")

    except Exception as e:
        print(f"❌ فشل في تحميل البيانات: {e}")

if __name__ == "__main__":
    fetch_usdt_dominance()

