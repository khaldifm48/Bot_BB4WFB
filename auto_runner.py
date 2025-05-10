import time
import subprocess
import schedule
import os

# تحديد المجلد الحالي تلقائيًا
base_dir = os.path.dirname(os.path.abspath(__file__))

def run_bot():
    print("🚀 بدء تشغيل WSF_Bot...")
    print("————————————————————————————————————————")

    print("🔍 تشغيل wsf_data_fetcher.py ...")
    subprocess.run(["python3", os.path.join(base_dir, "wsf_data_fetcher.py")])

    print("🔍 تشغيل smt_scanner_1h.py ...")
    subprocess.run(["python3", os.path.join(base_dir, "smt_scanner_1h.py")])

    print("🔍 تشغيل smart_consolidation_entry.py ...")
    subprocess.run(["python3", os.path.join(base_dir, "smart_consolidation_entry.py")])

    print("🔍 تشغيل strategy_entry.py ...")
    subprocess.run(["python3", os.path.join(base_dir, "strategy_entry.py")])

    print("📨 تشغيل telegram_alert.py ...")
    subprocess.run(["python3", os.path.join(base_dir, "telegram_alert.py")])

    print("✅ انتهى تشغيل البوت.")
    print("————————————————————————————————————————\n")

# كل 10 دقائق
schedule.every(10).minutes.do(run_bot)

print("⏱️ تم تفعيل الجدولة. البوت سيعمل كل 10 دقائق.")
print("اضغط Ctrl+C للإيقاف.\n")

# تشغيل أول مرة فورًا
run_bot()

# التكرار
while True:
    schedule.run_pending()
    time.sleep(1)

