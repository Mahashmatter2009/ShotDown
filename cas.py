import os
import requests
import time

TOKEN = "7487040227:AAFXEM7WJFycH40qLc_3H9sGfUcG8E0tsJY"
USER_ID = 6808756378
API = f"https://api.telegram.org/bot{TOKEN}"

offset = 0

def send(msg):
    requests.post(f"{API}/sendMessage", data={"chat_id": USER_ID, "text": msg})

def download_file(file_id, file_name):
    file_info = requests.get(f"{API}/getFile?file_id={file_id}").json()
    path = file_info["result"]["file_path"]
    url = f"https://api.telegram.org/file/bot{TOKEN}/{path}"
    content = requests.get(url).content
    with open(file_name, "wb") as f:
        f.write(content)

while True:
    try:
        updates = requests.get(f"{API}/getUpdates", params={"offset": offset, "timeout": 10}).json()
        for result in updates["result"]:
            offset = result["update_id"] + 1
            msg = result.get("message", {})
            sender = msg.get("from", {}).get("id")

            if sender != USER_ID:
                continue  # تجاهل أي شخص غيرك

            text = msg.get("text", "")
            if text == "/start":
                send("✅ البوت يعمل الآن وجاهز لاستقبال الملفات.")
                continue

            if "document" in msg:
                file_id = msg["document"]["file_id"]
                file_name = msg["document"]["file_name"]
                download_file(file_id, file_name)
                send(f"✅ تم حفظ الملف: {file_name}")
            elif "photo" in msg:
                file_id = msg["photo"][-1]["file_id"]
                file_name = f"photo_{file_id}.jpg"
                download_file(file_id, file_name)
                send(f"✅ تم حفظ الصورة باسم: {file_name}")
            else:
                send("❌ أرسل ملف فقط.")

    except Exception as e:
        print("Error:", str(e))
        time.sleep(3)
