import os
import requests
from bs4 import BeautifulSoup

TOKEN = os.environ["TG_BOT_TOKEN"]
CHAT_ID = os.environ["TG_CHAT_ID"]

URL = "https://racing.hkjc.com/racing/information/Chinese/Racing/LocalResults.aspx"

def fetch_hkjc_text():
    r = requests.get(URL, timeout=20, headers={
        "User-Agent": "Mozilla/5.0"
    })
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    # 1) 頁面標題
    title = soup.title.text.strip() if soup.title else "HKJC"

    # 2) 嘗試搵「最新賽果」表格入面頭幾行（通常會有場次/馬名/名次等）
    lines = []
    table = soup.find("table")
    if table:
        rows = table.find_all("tr")
        for tr in rows[:8]:  # 取頭幾行就夠，避免太長
            tds = [td.get_text(" ", strip=True) for td in tr.find_all(["th", "td"])]
            if tds:
                line = " | ".join(tds)
                # 避免太多空白行
                if line and line not in lines:
                    lines.append(line)

    # 如果搵唔到表格，就用標題頂住先
    if not lines:
        lines = [f"(暫時未抽到表格內容，可能網站結構改咗)"]

    msg = "📢 香港賽馬會更新\n\n"
    msg += f"\n\n"
    msg += "\n".join(lines[:6])  # 控制長度
    msg += f"\n\n🔗 {URL}"
    return msg

def send_telegram(text):
    api = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "disable_web_page_preview": False
    }
    resp = requests.post(api, data=data, timeout=20)
    print("Telegram status:", resp.status_code)
    print("Telegram response:", resp.text)
    resp.raise_for_status()

if __name__ == "__main__":
    text = fetch_hkjc_text()
    send_telegram(text)
