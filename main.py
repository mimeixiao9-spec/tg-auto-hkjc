import os
import requests
from bs4 import BeautifulSoup

TOKEN = os.environ["TG_BOT_TOKEN"]
CHAT_ID = os.environ["TG_CHAT_ID"]

URL = "https://racing.hkjc.com/racing/information/Chinese/Racing/LocalResults.aspx"

def get_latest():
    r = requests.get(URL, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.title.text.strip()
    return title

def send_telegram(msg):
    api = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": f"📢 香港馬會最新資訊\n\n{msg}\n\n{URL}"
    }
    requests.post(api, data=data)

if __name__ == "__main__":
    news = get_latest()
    send_telegram(news)
