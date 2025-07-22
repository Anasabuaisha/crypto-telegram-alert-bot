import os, requests, time
from datetime import datetime
from telegram import Bot

BOT = Bot(token=os.getenv("BOT_TOKEN"))
CHAT_ID = os.getenv("CHAT_ID")

THRESHOLD = 5.0  # percent
INTERVAL = 1800  # 30 minutes

def fetch_total2():
    url = "https://api.coingecko.com/api/v3/global"
    resp = requests.get(url).json()
    total1 = resp['data']['total_market_cap']['usd']
    btc_pct = resp['data']['market_cap_percentage']['btc']
    btc_cap = total1 * btc_pct / 100
    total2 = total1 - btc_cap
    return total2

def fetch_usdtd():
    url = "https://api.coingecko.com/api/v3/coins/tether"
    resp = requests.get(url).json()
    dominance = resp['market_data']['market_cap']['usd'] / resp['market_data']['total_market_cap']['usd'] * 100
    return dominance

def monitor():
    prev_t2 = fetch_total2()
    prev_ud = fetch_usdtd()
    while True:
        time.sleep(INTERVAL)
        curr_t2 = fetch_total2()
        curr_ud = fetch_usdtd()

        pct_t2 = (curr_t2 - prev_t2)/prev_t2*100
        pct_ud = curr_ud - prev_ud

        msgs = []
        if abs(pct_t2) >= THRESHOLD:
            msgs.append(f"📊 TOTAL2 Alert:\nChange: {'+' if pct_t2>0 else ''}{pct_t2:.2f}%\nValue: ${curr_t2/1e12:.2f}T")
            prev_t2 = curr_t2

        if abs(pct_ud) >= THRESHOLD:
            msgs.append(f"📊 USDT.D Alert:\nChange: {'+' if pct_ud>0 else ''}{pct_ud:.2f}%\nValue: {curr_ud:.2f}%")
            prev_ud = curr_ud

        if msgs:
            BOT.send_message(chat_id=CHAT_ID, text="\n\n".join(msgs), parse_mode="Markdown")

if __name__=="__main__":
    monitor()
