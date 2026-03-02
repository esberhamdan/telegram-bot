import requests
import time
import random

TOKEN = "8621477107:AAGw6TiBLiGq8--o_NfB7K2yjxR5hFheZGk"
CHAT_ID = "-1003709871403"

def send_signal():
    signal_type = random.choice(["BUY", "SELL"])
    price = random.randint(30000, 70000)

    message = f"""
🚀 Trading Signal

Pair: BTCUSDT
Type: {signal_type}
Entry: {price}
Take Profit: {price + 500}
Stop Loss: {price - 500}

#Crypto #Signal
"""

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)

while True:
    send_signal()
    time.sleep(300)  # كل 5 دقائق
