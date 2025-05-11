import subprocess
import time
import os

def run_script(script_name):
    try:
        print(f"\n🔍 تشغيل {script_name} ...")
        subprocess.run(["python3", script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ خطأ أثناء تشغيل {script_name}: {e}")

def run_main_bot():
    run_script("wsf_data_fetcher.py")
    run_script("smt_scanner_1h.py")
    run_script("smart_consolidation_entry.py")
    run_script("strategy_entry.py")
    run_script("telegram_alert.py")

if __name__ == "__main__":
    print("⏱️ تم تفعيل الجدولة. البوت سيعمل تلقائيًا.\nاضغط Ctrl+C للإيقاف.\n")
    while True:
        run_main_bot()
        print("✅ انتهى تشغيل البوت.")
        print("—" * 80)
        time.sleep(180)  # كل 3 دقائق

