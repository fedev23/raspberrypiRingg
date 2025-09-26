import utime, urequests, ubinascii

from secrets import TWILIO_SID, TWILIO_TOKEN, TWILIO_FROM, TWILIO_TO

THROTTLE_MS = 60_000
_last_send = -THROTTLE_MS

# URL-encode compatible MicroPython (UTF-8). OJO: convierte '+' en %2B.
def _urlencode(params):
    def esc(val):
        b = val.encode("utf-8") if isinstance(val, str) else val
        out = []
        for ch in b:
            if (48 <= ch <= 57) or (65 <= ch <= 90) or (97 <= ch <= 122) or ch in b"-_.~":
                out.append(chr(ch))
            else:
                out.append("%%%02X" % ch)
        return "".join(out)
    return "&".join("{}={}".format(esc(k), esc(v)) for k, v in params.items())


def send_whatsapp(to, text):
    """Envía un WhatsApp via Twilio Sandbox con rate-limit y encoding correcto."""
    global _last_send
    now = utime.ticks_ms()
    if utime.ticks_diff(now, _last_send) < THROTTLE_MS:
        print("Twilio THROTTLED (espera)",
              THROTTLE_MS - utime.ticks_diff(now, _last_send), "ms")
        return False    

    _last_send = now

    url = "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json".format(TWILIO_SID)
    auth = "Basic " + ubinascii.b2a_base64(("{}:{}".format(TWILIO_SID, TWILIO_TOKEN)).encode()).decode().strip()
    headers = {
        "Authorization": auth,
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }
    payload =_urlencode({"To": to, "From": TWILIO_FROM, "Body": text})

    try:
        r = urequests.post(url, headers=headers, data=payload)
        code = r.status_code
        txt  = r.text
        r.close()
        print("Twilio status:", code)
        if not (200 <= code < 300):
            print("Resp:", txt)   # <-- clave para ver el motivo exacto
        return 200 <= code < 300
    except Exception as e:
        print("Twilio error:", e)
        return False
