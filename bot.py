import requests
import time
import random

# ==============================
# 🔑 ضع التوكن والـ Chat ID هنا
# ==============================

TOKEN = "8621477107:AAGw6TiBLiGq8--o_NfB7K2yjxR5hFheZGk"
CHAT_ID = "-1003709871403"
# ==============================
# 📊 قائمة العملات (20+ عملة)
# ==============================

symbols = [
    "BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT",
    "ADAUSDT","DOGEUSDT","AVAXUSDT","MATICUSDT","DOTUSDT",
    "LINKUSDT","LTCUSDT","TRXUSDT","UNIUSDT","ATOMUSDT",
    "APTUSDT","OPUSDT","ARBUSDT","NEARUSDT","FILUSDT",
    "SANDUSDT","AAVEUSDT"
]

# ==============================
# 🚀 دالة إرسال الإشارة
# ==============================

def send_signal():
    pair = random.choice(symbols)
    signal_type = random.choice(["BUY", "SELL"])

    price = random.randint(100, 70000)
    tp = price + random.randint(300, 800)
    sl = price - random.randint(300, 800)

    message = f"""
🚀 Trading Signal

Pair: {pair}
Type: {signal_type}
Entry: {price}
Take Profit: {tp}
Stop Loss: {sl}

#Crypto #Signal
"""

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)

# ==============================
# 🔁 تشغيل البوت كل 5 دقائق
# ==============================

while True:
    send_signal()
    time.sleep(300)  # كل 5 دقائق
