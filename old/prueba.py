from machine import Pin
import utime, micropython

BUTTON_PIN   = 0      # GP0
DEBOUNCE_MS  = 200
USE_INT_PULL = False  # True si NO usás la resistencia externa

ENTRE_AL_PICO = 0                 # contador de toques
COOLDOWN_MS   = 5 * 60 * 1000     # 5 minutos en ms
cooldown_until = 0                # 0 = sin cooldown; si no, timestamp ticks_ms hasta el que ignoramos

# === botón ===
if USE_INT_PULL:
    button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)   # pull-up interno
else:
    button = Pin(BUTTON_PIN, Pin.IN)                # sin pull interno (usás la 10k a 3V3)

led = Pin("LED", Pin.OUT, value=0)

_last = 0
def on_press(ts):
    led.toggle()
    print("BTN", ts, "ms")   # ASCII simple

def isr(pin):
    global _last, ENTRE_AL_PICO, cooldown_until
    now = utime.ticks_ms()

    # Si estamos en cooldown, ignorar pulsos hasta que termine
    if cooldown_until and utime.ticks_diff(now, cooldown_until) < 0:
        return
    # Si el cooldown terminó, limpiar estado
    if cooldown_until and utime.ticks_diff(now, cooldown_until) >= 0:
        cooldown_until = 0
        ENTRE_AL_PICO  = 0

    # Debounce + registrar pulsación
    if utime.ticks_diff(now, _last) >= DEBOUNCE_MS:
        _last = now
        ENTRE_AL_PICO += 1
        micropython.schedule(on_press, now)

        # Al llegar a 4 pulsos: arrancar cooldown de 5 min
        if ENTRE_AL_PICO >= 4:
            print(">>> COOLDOWN 5 min")
            cooldown_until = utime.ticks_add(now, COOLDOWN_MS)
            # opcional: feedback del inicio del cooldown
            # micropython.schedule(lambda t: print(">>> COOLDOWN 5 min"), 0)

button.irq(trigger=Pin.IRQ_FALLING, handler=isr)

while True:
    utime.sleep_ms(1)
