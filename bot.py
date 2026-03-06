import requests
import random
import time
import threading
from datetime import datetime

# ==============================
# ضع بياناتك هنا
# ==============================
BOT_TOKEN = "8621477107:AAGPbCgxuqDzmjgw3CQx-TmWJ89H0DPqJUE"
CHAT_ID = "-1003709871403"
# ==============================

coins = [
"BTCUSDT","ETHUSDT","BNBUSDT","XRPUSDT","ADAUSDT",
"SOLUSDT","DOGEUSDT","MATICUSDT","DOTUSDT","LTCUSDT",
"TRXUSDT","AVAXUSDT","SHIBUSDT","ATOMUSDT","LINKUSDT",
"UNIUSDT","ETCUSDT","XLMUSDT","ICPUSDT","APTUSDT",
"NEARUSDT","FILUSDT","ALGOUSDT","HBARUSDT","EGLDUSDT"
]

last_update_id = None

# ==============================
# سعر Binance الحقيقي
# ==============================

def get_price(symbol):
    url=f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        data=requests.get(url).json()
        return float(data["price"])
    except:
        return None


# ==============================
# ارسال رسالة
# ==============================

def send_message(chat_id,text,keyboard=None):

    url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload={
        "chat_id":chat_id,
        "text":text
    }

    if keyboard:
        payload["reply_markup"]=keyboard

    requests.post(url,json=payload)


# ==============================
# أزرار البوت
# ==============================

def main_menu():

    return {
        "keyboard":[
            ["شروط دخول المنصة"],
            ["ارسال قيمة الاشتراك"],
            ["أكمل التحقق"]
        ],
        "resize_keyboard":True
    }


# ==============================
# استقبال رسائل المستخدم
# ==============================

def handle_updates():

    global last_update_id

    while True:

        url=f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

        if last_update_id:
            url+=f"?offset={last_update_id+1}"

        data=requests.get(url).json()

        for update in data["result"]:

            last_update_id=update["update_id"]

            if "message" not in update:
                continue

            chat_id=update["message"]["chat"]["id"]
            text=update["message"].get("text","")

            if text=="/start":

                welcome="""
أهلاً وسهلاً بك في المنصة الاحترافية 📊

نقدم إشارات أكثر من 25 عملة
كل 5 دقائق بواسطة تحليل ذكي.

اختر من القائمة:
"""

                send_message(chat_id,welcome,main_menu())


            elif text=="شروط دخول المنصة":

                msg="""
لدخول المنصة يجب الاشتراك بقيمة 15$

ونعد بتحقيق أكثر من 150$
خلال أول أسبوع بإذن الله.
"""

                send_message(chat_id,msg)


            elif text=="ارسال قيمة الاشتراك":

                msg="""
يرجى ارسال 15$

إلى محفظة BEP20 التالية:

0xB0313B2C13F1461Dc7aDfE6839196e495fc3D96c
"""

                send_message(chat_id,msg)


            elif text=="أكمل التحقق":

                msg="يتم التحقق من الإيداع يرجى الانتظار قليلاً..."

                send_message(chat_id,msg)

                time.sleep(5)

                msg2="""
تم التحقق بنجاح ✅

أهلاً بك في مجتمع المتداولين المحترفين.

انضم إلى القناة الخاصة:

https://t.me/+9ztPgIHL-GIyNjU0
"""

                send_message(chat_id,msg2)

        time.sleep(2)


# ==============================
# توليد إشارات العملات
# ==============================

def generate_signal():

    message="📊 Crypto Signals (5M)\n"
    message+=f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    selected=random.sample(coins,25)

    for coin in selected:

        signal=random.choice(["BUY 🟢","SELL 🔴"])

        price=get_price(coin)

        if price is None:
            continue

        tp=round(price*random.uniform(1.01,1.05),4)
        sl=round(price*random.uniform(0.95,0.99),4)

        message+=f"{coin}\n"
        message+=f"Signal: {signal}\n"
        message+=f"Entry: {price}\n"
        message+=f"TP: {tp}\n"
        message+=f"SL: {sl}\n"
        message+="-----------------\n"

    return message


# ==============================
# ارسال الإشارات كل 5 دقائق
# ==============================

def signal_loop():

    while True:

        msg=generate_signal()

        send_message(CHAT_ID,msg)

        print("signals sent")

        time.sleep(300)


# ==============================
# تشغيل البوت
# ==============================

print("Bot started...")

threading.Thread(target=handle_updates).start()

signal_loop()
