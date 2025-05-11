import schedule
import time
import os

def run_script(script):
    print(f"🔍 تشغيل {script} ...")
    os.system(f"/usr/bin/python3 ~/Desktop/Bot_BB4WFB/{script}")

# سكربتات كل 3 دقائق
def run_main_bot():
    run_script("wsf_data_fetcher.py")
    run_script("smt_scanner_1h.py")
    run_script("smart_consolidation_entry.py")
    run_script("strategy_entry.py")
    run_script("telegram_alert.py")
    print("✅ انتهى تشغيل البوت.")
    print("————————————————————————————————————————————————————————————————")

# سكربت USDT.D كل 6 ساعات
schedule.every(6).hours.do(lambda: run_script("usdt_dominance_fetcher.py"))

# تشغيل باقي البوت كل 3 دقائق
schedule.every(3).minutes.do(run_main_bot)

print("\n⏱️ تم تفعيل الجدولة. البوت سيعمل تلقائيًا.")
print("اضغط Ctrl+C للإيقاف.\n")

while True:
    schedule.run_pending()
    time.sleep(1)

