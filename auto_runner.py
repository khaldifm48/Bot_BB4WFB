import schedule
import time
import os

def run_script(script):
    print(f"🔍 تشغيل {script} ...")
    os.system(f"/usr/bin/python3 ~/Desktop/Bot_BB4WFB/{script}")

print("\n⏱️ تم تفعيل الجدولة. البوت سيعمل تلقائيًا.")
print("اضغط Ctrl+C للإيقاف.\n")

# تشغيل كل 10 دقائق
schedule.every(10).minutes.do(run_script, "wsf_data_fetcher.py")
schedule.every(10).minutes.do(run_script, "smt_scanner_1h.py")
schedule.every(10).minutes.do(run_script, "smart_consolidation_entry.py")
schedule.every(10).minutes.do(run_script, "strategy_entry.py")
schedule.every(10).minutes.do(run_script, "telegram_alert.py")

# تشغيل usdt_dominance_fetcher فقط كل 6 ساعات
schedule.every(6).hours.do(run_script, "usdt_dominance_fetcher.py")

while True:
    schedule.run_pending()
    time.sleep(1)

