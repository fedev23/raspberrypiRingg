from machine import Pin
import utime
import secrets
import wifi

from send_MSGTelegram import send_telegram

# --- Config ---
BUTTON_PIN    = 0
USE_INT_PULL  = False          # True if you are NOT using an external 10k (uses internal pull-up)
DEBOUNCE_MS   = 30             # 20–40 ms typical
COOLDOWN_MS   = 10 * 1000      # 30s wait after each send

# Button and LED
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP) if USE_INT_PULL else Pin(BUTTON_PIN, Pin.IN)
led    = Pin("LED", Pin.OUT, value=0)

_last_edge = 0
_pending   = False
cooldown_until = 0  # 0 = no cooldown

def isr(p):
    global _last_edge, _pending
    now = utime.ticks_ms()
    # falling edge + debounce
    if p.value() == 0 and utime.ticks_diff(now, _last_edge) > DEBOUNCE_MS:
        _last_edge = now
        _pending = True

button.irq(trigger=Pin.IRQ_FALLING, handler=isr)

def flash(ms):  # visual feedback
    led.value(1); utime.sleep_ms(ms); led.value(0)

while True:
    now = utime.ticks_ms()

    # exit cooldown when time has passed
    if cooldown_until and utime.ticks_diff(now, cooldown_until) >= 0:
        cooldown_until = 0
        # short flash to indicate "ready again"
        flash(120)

    if _pending:
        _pending = False
        print(">> Procesando botón en loop, ms:", now)
        # if in cooldown, ignore the press
        if cooldown_until:
            # DEBUG ONLY
            print("En cooldown… faltan", utime.ticks_diff(cooldown_until, now), "ms")
        else:
            # 1) turn on Wi‑Fi and connect
            ok, ip = wifi.connect(secrets.WIFI_SSID, secrets.WIFI_PASS, timeout_ms=12000)
            print("Wi-Fi:", ok, "| IP:", ip)

            # 2) send message
            if ok:
                send_telegram("ALERTA: necesito ayuda.")
                        
                flash(300)  # send confirmation
            else:
                print("No se pudo enviar")

            # 3) turn off Wi‑Fi to save battery
            wifi.off()

            # 4) activate 30s cooldown
            cooldown_until = utime.ticks_add(now, COOLDOWN_MS)

    utime.sleep_ms(2)
