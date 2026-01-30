import os
import requests
from bs4 import BeautifulSoup

TOKEN = os.environ["TG_BOT_TOKEN"]
CHAT_ID = os.environ["TG_CHAT_ID"]

URL = "https://racing.hkjc.com/racing/information/Chinese/Racing/LocalResults.aspx"

def get_latest():
    r = requests.get(URL, timeout=20)
    print("HKJC status:", r.status_code)
    print("HKJC content-type:", r.headers.get("content-type"))
    print("HKJC first 200 chars:", r.text[:200].replace("\n", " "))

    soup = BeautifulSoup(r.text, "html.parser")
    title = (soup.title.text.strip() if soup.title else "")
    print("Parsed title:", title)

    if not title:
        title = f"(抓取不到標題，HKJC status={r.status_code})"
    return title

def send_telegram(msg):
    api = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": f"📢 香港馬會最新資訊\n\n{msg}\n\n{URL}"
    }

    resp = requests.post(api, data=data, timeout=20)
    print("Telegram status:", resp.status_code)
    print("Telegram response:", resp.text)


if __name__ == "__main__":
    news = get_latest()
    send_telegram(news)
