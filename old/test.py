# test_pc.py
import requests
from requests.auth import HTTPBasicAuth  # más simple que armar el header a mano
from secrets import TWILIO_SID, TWILIO_TOKEN, TWILIO_FROM, TWILIO_TO

url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json"
data = {
    "To": TWILIO_TO,           # ej: "whatsapp:+54911XXXXXXXX"
    "From": TWILIO_FROM,       # ej: "whatsapp:+14155238886"  (sandbox)
    "Body": "Juli batata gorda boluda",
}

r = requests.post(url, data=data, auth=HTTPBasicAuth(TWILIO_SID, TWILIO_TOKEN))
print(r.status_code, r.text)   # 201 = Created (OK)
