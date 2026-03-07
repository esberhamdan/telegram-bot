import requests
import random
import time
import threading
import sqlite3
from datetime import datetime

# ==============================
# بيانات البوت
# ==============================

BOT_TOKEN = "8621477107:AAGPbCgxuqDzmjgw3CQx-TmWJ89H0DPqJUE"
CHAT_ID = "-1003709871403"

API_KEY = "Ds7CjNIyaa5S1uWBqnT1VceR1D8O47YNbVpVpiH3CqJtoNVFumCnWYw3H42eXwsH"
SECRET_KEY = "629qixBt4fOtE2pw6Y4J8yFX0KphzpwYdV4QkWUOJ0NLZHVIRjMeZNCvI2o75Zax"
ADMIN_ID=8289549810
# ==============================

WALLET_ADDRESS="0xB0313B2C13F1461Dc7aDfE6839196e495fc3D96c"

CHANNEL_LINK="https://t.me/+9ztPgIHL-GIyNjU0"

# ==============================
# قاعدة البيانات
# ==============================

db=sqlite3.connect("bot.db",check_same_thread=False)
cursor=db.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users(chat_id INTEGER PRIMARY KEY)")
cursor.execute("CREATE TABLE IF NOT EXISTS used_txid(txid TEXT PRIMARY KEY)")

db.commit()

# ==============================

coins=[
"BTCUSDT","ETHUSDT","BNBUSDT","XRPUSDT","ADAUSDT",
"SOLUSDT","DOGEUSDT","MATICUSDT","DOTUSDT","LTCUSDT",
"TRXUSDT","AVAXUSDT","SHIBUSDT","ATOMUSDT","LINKUSDT",
"UNIUSDT","ETCUSDT","XLMUSDT","ICPUSDT","APTUSDT",
"NEARUSDT","FILUSDT","ALGOUSDT","HBARUSDT","EGLDUSDT"
]

last_update_id=None
waiting_txid={}
broadcast_mode=False

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
# سعر Binance
# ==============================

def get_price(symbol):

    url=f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"

    try:
        data=requests.get(url).json()
        return float(data["price"])
    except:
        return None

# ==============================
# التحقق من المعاملة
# ==============================

def verify_tx(txid):

    url=f"https://api.bscscan.com/api?module=proxy&action=eth_getTransactionByHash&txhash={txid}&apikey={API_KEY}"

    try:

        data=requests.get(url).json()
        result=data["result"]

        if result is None:
            return False

        to_address=result["to"].lower()

        value=int(result["value"],16)/10**18

        if to_address==WALLET_ADDRESS.lower() and value>=15:
            return True

        return False

    except:
        return False

# ==============================
# القائمة الرئيسية
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
# استقبال الرسائل
# ==============================

def handle_updates():

    global last_update_id,broadcast_mode

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

            # حفظ المستخدم
            cursor.execute("INSERT OR IGNORE INTO users(chat_id) VALUES(?)",(chat_id,))
            db.commit()

            # ======================
            # start
            # ======================

            if text=="/start":

                welcome="""
أهلاً وسهلاً بك في المنصة الاحترافية 📊

نقدم إشارات أكثر من 25 عملة
كل 5 دقائق بواسطة تحليل ذكي.

اختر من القائمة:
"""

                send_message(chat_id,welcome,main_menu())

            # ======================
            # شروط
            # ======================

            elif text=="شروط دخول المنصة":

                msg="""
لدخول المنصة يجب الاشتراك بقيمة 15$

ونعد بتحقيق أكثر من 150$
خلال أول أسبوع بإذن الله.
"""

                send_message(chat_id,msg)

            # ======================
            # الدفع
            # ======================

            elif text=="ارسال قيمة الاشتراك":

                msg=f"""
يرجى ارسال 15$

إلى محفظة BEP20 التالية:

{WALLET_ADDRESS}

بعد الدفع اضغط
(أكمل التحقق)
"""

                send_message(chat_id,msg)

            # ======================
            # طلب TXID
            # ======================

            elif text=="أكمل التحقق":

                waiting_txid[chat_id]=True

                send_message(chat_id,"أرسل TXID الخاص بالمعاملة الآن")

            # ======================
            # استقبال TXID
            # ======================

            elif chat_id in waiting_txid:

                txid=text.strip()

                cursor.execute("SELECT txid FROM used_txid WHERE txid=?",(txid,))
                used=cursor.fetchone()

                if used:

                    send_message(chat_id,"❌ تم استخدام TXID مسبقاً")
                    continue

                send_message(chat_id,"جاري التحقق من المعاملة...")

                if verify_tx(txid):

                    cursor.execute("INSERT INTO used_txid(txid) VALUES(?)",(txid,))
                    db.commit()

                    send_message(chat_id,"✅ تم التحقق بنجاح")

                    msg=f"""
أهلاً بك في مجتمع المتداولين المحترفين

انضم للقناة الخاصة:

{CHANNEL_LINK}
"""

                    send_message(chat_id,msg)

                    del waiting_txid[chat_id]

                else:

                    send_message(chat_id,"❌ المعاملة غير صحيحة")

            # ======================
            # لوحة المشرف
            # ======================

            elif text=="/admin" and chat_id==ADMIN_ID:

                keyboard={
                    "keyboard":[
                        ["📊 الإحصائيات"],
                        ["📢 بث رسالة"]
                    ],
                    "resize_keyboard":True
                }

                send_message(chat_id,"لوحة التحكم",keyboard)

            # ======================
            # الإحصائيات
            # ======================

            elif text=="📊 الإحصائيات" and chat_id==ADMIN_ID:

                cursor.execute("SELECT COUNT(*) FROM users")
                users=cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM used_txid")
                payments=cursor.fetchone()[0]

                msg=f"""
📊 إحصائيات البوت

👤 المستخدمين: {users}

💰 المدفوعات: {payments}
"""

                send_message(chat_id,msg)

            # ======================
            # بث رسالة
            # ======================

            elif text=="📢 بث رسالة" and chat_id==ADMIN_ID:

                broadcast_mode=True

                send_message(chat_id,"أرسل الرسالة الآن")

            elif broadcast_mode and chat_id==ADMIN_ID:

                cursor.execute("SELECT chat_id FROM users")

                users=cursor.fetchall()

                for user in users:

                    try:
                        send_message(user[0],text)
                    except:
                        pass

                broadcast_mode=False

                send_message(chat_id,"تم إرسال الرسالة")

        time.sleep(2)

# ==============================
# توليد الإشارات
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
# ارسال الإشارات
# ==============================

def signal_loop():

    while True:

        msg=generate_signal()

        send_message(CHAT_ID,msg)

        print("signals sent")

        time.sleep(300)

# ==============================

print("Bot started...")

threading.Thread(target=handle_updates).start()

signal_loop()
