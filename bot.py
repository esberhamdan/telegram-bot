import requests
import time
import random

# ==============================
# 🔑 ضع التوكن والـ Chat ID
# ==============================

TOKEN = os.getenv("8621477107:AAGw6TiBLiGq8--o_NfB7K2yjxR5hFheZGk")
CHAT_ID = "1003709871403"

# ==============================
# 📊 قائمة العملات
# ==============================

symbols = [
    "BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT",
    "ADAUSDT","DOGEUSDT","AVAXUSDT","MATICUSDT","DOTUSDT",
    "LINKUSDT","LTCUSDT","TRXUSDT","UNIUSDT","ATOMUSDT",
    "APTUSDT","OPUSDT","ARBUSDT","NEARUSDT","FILUSDT"
]

# ==============================
# 📈 جلب السعر الحقيقي من Binance
# ==============================

def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    data = response.json()
    return float(data["price"])

# ==============================
# 🚀 إرسال الإشارة
# ==============================

def send_signal():
    pair = random.choice(symbols)
    signal_type = random.choice(["BUY", "SELL"])

    price = get_price(pair)

    # نحسب TP و SL بنسبة 1%
    tp = price * 1.01
    sl = price * 0.99

    message = f"""
🚀 Trading Signal

Pair: {pair}
Type: {signal_type}
Entry: {round(price, 4)}
Take Profit: {round(tp, 4)}
Stop Loss: {round(sl, 4)}

#Crypto #Signal
"""

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)

# ==============================
# 🔁 تشغيل كل 5 دقائق
# ==============================

while True:
    send_signal()
    time.sleep(300)
# ==============================
