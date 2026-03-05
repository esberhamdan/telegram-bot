import requests
import random
import time
from datetime import datetime

# ==============================
# ضع بياناتك هنا
# ==============================
BOT_TOKEN = "8621477107:AAGPbCgxuqDzmjgw3CQx-TmWJ89H0DPqJUE"
CHAT_ID = "-1003709871403"
# ==============================

# قائمة 25 عملة
coins = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT",
    "SOLUSDT", "DOGEUSDT", "MATICUSDT", "DOTUSDT", "LTCUSDT",
    "TRXUSDT", "AVAXUSDT", "SHIBUSDT", "ATOMUSDT", "LINKUSDT",
    "UNIUSDT", "ETCUSDT", "XLMUSDT", "ICPUSDT", "APTUSDT",
    "NEARUSDT", "FILUSDT", "ALGOUSDT", "HBARUSDT", "EGLDUSDT"
]

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    try:
        requests.post(url, data=payload)
        print("Signal sent successfully")
    except Exception as e:
        print("Error sending message:", e)

def generate_signal():
    message = "📊 Crypto Signals (5M)\n"
    message += f"🕒 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    selected_coins = random.sample(coins, 25)

    for coin in selected_coins:
        signal_type = random.choice(["BUY 🟢", "SELL 🔴"])
        price = round(random.uniform(0.1, 50000), 4)
        tp = round(price * random.uniform(1.01, 1.05), 4)
        sl = round(price * random.uniform(0.95, 0.99), 4)

        message += f"{coin}\n"
        message += f"Signal: {signal_type}\n"
        message += f"Entry: {price}\n"
        message += f"TP: {tp}\n"
        message += f"SL: {sl}\n"
        message += "---------------------\n"

    return message

print("Bot started...")

while True:
    try:
        signal_message = generate_signal()
        send_message(signal_message)
        print("Waiting 5 minutes...")
        time.sleep(300)  # 5 دقائق
    except Exception as e:
        print("Main loop error:", e)
        time.sleep(10)
