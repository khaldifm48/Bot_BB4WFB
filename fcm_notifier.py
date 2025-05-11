import requests
import json

# ✅ بيانات FCM
FCM_URL = "https://fcm.googleapis.com/fcm/send"
SERVER_KEY = "AAAA[...]YOUR_SERVER_KEY[...]AAA"  # استبدلها بالمفتاح الصحيح من Firebase
TOPIC = "wsf_signals"  # أو استخدم توكن فردي إن حبيت

def send_fcm_notification(title, body):
    headers = {
        "Authorization": f"key={SERVER_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "to": f"/topics/{TOPIC}",
        "notification": {
            "title": title,
            "body": body
        }
    }
    try:
        response = requests.post(FCM_URL, headers=headers, data=json.dumps(payload))
        print("✅ تم إرسال إشعار للتطبيق:", response.json())
    except Exception as e:
        print("❌ فشل إرسال FCM:", e)

