import os 
import subprocess

# مسار مجلد البوت
base_dir = os.path.expanduser("~/Desktop/Bot_BB4WFB")

# قراءة الانحياز الأسبوعي
bias_file = os.path.join(base_dir, "weekly_bias.txt")
if not os.path.exists(bias_file):
    print("❌ ملف weekly_bias.txt غير موجود.")
    exit()

with open(bias_file, "r") as f:
    bias = f.read().strip().lower()

print(f"📊 Weekly Bias: {bias}")

# إيقاف التنفيذ في حال الانحياز هابط
if bias not in ["صعود", "محايد"]:
    print("⛔️ السوق ليس في وضع يسمح بالدخول حالياً.")
    exit()

print("🚀 بدء تشغيل WSF_Bot...\n" + "—" * 40)

# 1. تحليل SMT
print("🔍 تشغيل smt_scanner.py ...")
subprocess.run(["python3", os.path.join(base_dir, "smt_scanner.py")])
print("—" * 40)

# 2. تحليل الدخول Wick + FVG + BBR
print("🔍 تشغيل strategy_entry.py ...")
subprocess.run(["python3", os.path.join(base_dir, "strategy_entry.py")])
print("—" * 40)

# 3. إرسال التنبيهات
print("📨 تشغيل telegram_alert.py ...")
subprocess.run(["python3", os.path.join(base_dir, "telegram_alert.py")])
print("—" * 40)

print("✅ انتهى تشغيل البوت.")

