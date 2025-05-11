import pandas as pd
import requests
from io import StringIO

def fetch_usdt_dominance():
    url = "https://raw.githubusercontent.com/khaldifm48/Bot_BB4WFB/main/data/usdt_dominance_data.csv"
    path = "data/usdt_dominance_data.csv"

    try:
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text))
        df.to_csv(path, index=False)
        print("✅ تم حفظ بيانات USDT Dominance بنجاح.")
    except Exception as e:
        print(f"❌ فشل في تحميل بيانات USDT.D: {e}")

if __name__ == "__main__":
    fetch_usdt_dominance()

