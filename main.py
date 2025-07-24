import requests
import time
from telegram import Bot

# Replace with your actual token and chat ID
TOKEN = "7865504031:AAEj0lfTVx6nNxHhQa47BjiE5whAZmM1lP8"
CHAT_ID = "1127944772"

bot = Bot(token=TOKEN)

def fetch_total2():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    try:
        resp = requests.get(url)
        data = resp.json()
        return data["ethereum"]["usd"]
    except Exception as e:
        print(f"Error in fetch_total2: {e}")
        return None

def fetch_usdt_d():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=usd"
    try:
        resp = requests.get(url)
        data = resp.json()
        return data["tether"]["usd"]
    except Exception as e:
        print(f"Error in fetch_usdt_d: {e}")
        return None

def send(msg):
    bot.send_message(chat_id=CHAT_ID, text=msg)

def monitor():
    prev_t2 = fetch_total2()
    prev_usdt = fetch_usdt_d()
    while True:
        t2 = fetch_total2()
        usdt = fetch_usdt_d()

        if t2 and prev_t2 and abs(t2 - prev_t2) >= 10:
            send(f"ETH Price Change Alert: {prev_t2} → {t2} USD")
            prev_t2 = t2

        if usdt and prev_usdt and abs(usdt - prev_usdt) >= 0.01:
            send(f"USDT Price Change Alert: {prev_usdt} → {usdt} USD")
            prev_usdt = usdt

        time.sleep(60)

if __name__ == "__main__":
    monitor()
