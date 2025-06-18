import requests
import time
import telebot
import threading

BOT_TOKEN = 'TOKEN_BOT_CỦA_BẠN'
bot = telebot.TeleBot(BOT_TOKEN)

users = set()
sent_ids = set()

API_URL = 'https://namdinhbox.quetxu.live/api/boxes'

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.chat.id
    if user_id not in users:
        users.add(user_id)
        bot.send_message(user_id, "✅ Bot đã bật! Mình sẽ gửi box xu TikTok cho bạn khi có.")
    else:
        bot.send_message(user_id, "✅ Bạn đã bật rồi nhé!")

def send_to_all(msg):
    for uid in list(users):
        try:
            bot.send_message(uid, msg)
        except:
            users.remove(uid)

def check_loop():
    while True:
        try:
            res = requests.get(API_URL)
            data = res.json()
            for box in data.get('boxes', []):
                if int(box['gold'], 0) >= 100:
                    if box['id'] not in sent_ids:
                        link = f"https://www.tiktok.com/@{box['unique_id']}/live"
                        msg = f"🎁 Box: {box['gold']} xu\n👥 {box['online']} người\n🕒 Đếm ngược: {box['countdown']}s\n🔗 Link: {link}"
                        send_to_all(msg)
                        sent_ids.add(box['id'])
        except Exception as e:
            print("❌ Lỗi:", e)
        time.sleep(15)

threading.Thread(target=check_loop).start()
bot.polling()
