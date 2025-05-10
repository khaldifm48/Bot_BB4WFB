import os
import schedule
import time
import subprocess

base_dir = os.path.expanduser("~/Desktop/Bot_BB4WFB")

# تعريف المهام

def run_bot():
    print("\n🚀 بدء تشغيل WSF_Bot...")
    print("\n🔄 تحديث البيانات...")
    subprocess.run(["python3", os.path.join(base_dir, "wsf_data_fetcher.py")])

    print("\n🔍 تحليل SMT...")
    subprocess.run(["python3", os.path.join(base_dir, "smt_scanner_1h.py")])

    print("\n🎯 تحليل فرص 15m...")
    subprocess.run(["python3", os.path.join(base_dir, "smart_consolidation_entry.py")])

    print("\n📈 تحليل فرص 4H...")
    subprocess.run(["python3", os.path.join(base_dir, "strategy_entry.py")])

    print("\n✅ انتهى تشغيل البوت.\n")

# جدولة كل 10 دقائق
schedule.every(10).minutes.do(run_bot)

print("⏱️ تم تفعيل الجدولة. البوت سيعمل كل 10 دقائق.")
print("اضغط Ctrl+C للإيقاف.")

while True:
    schedule.run_pending()
    time.sleep(1)

