import urequests
import secrets

URL = "https://api.telegram.org/bot" + secrets.TELEGRAM_BOT_TOKEN + "/sendMessage"


def send_telegram(text):
    try:
        r = urequests.post(URL, json={"chat_id": secrets.CHAT_ID, "text": text})
        r.close()
        return r.status_code == 200
    except Exception as e:
        return False



