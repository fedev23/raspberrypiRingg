from machine import Pin
import utime

BUTTON_PIN    = 0       # GP0
USE_INT_PULL  = False   # True si NO usás la 10k externa
DEBOUNCE_MS   = 25      # 20–40 ms
COOLDOWN_MS   = 1500    # 1.5 s entre "timbrazos" (ajustá a gusto)

btn = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP) if USE_INT_PULL else Pin(BUTTON_PIN, Pin.IN)
led = Pin("LED", Pin.OUT, value=0)

last_edge = 0          # para anti-rebote de la IRQ
pending   = False      # flag puesto por la IRQ
locked    = False      # bloquea nuevos eventos hasta liberar y cumplir cooldown
last_fire = -COOLDOWN_MS

def isr(p):
    # Se dispara en flanco de bajada (con pull-up, apretar = 0)
    global last_edge, pending
    now = utime.ticks_ms()
    if p.value() == 0 and utime.ticks_diff(now, last_edge) > DEBOUNCE_MS:
        last_edge = now
        pending = True

btn.irq(trigger=Pin.IRQ_FALLING, handler=isr)

while True:
    now = utime.ticks_ms()

    # Dispara solo si no está bloqueado y terminó el cooldown
    if pending and not locked and utime.ticks_diff(now, last_fire) >= COOLDOWN_MS:
        pending = False
        locked  = True
        last_fire = now

        # acción del "timbre"
        led.value(1)
        print("RING", now, "ms")
        utime.sleep_ms(120)
        led.value(0)

    # Desbloquea cuando el botón fue soltado y pasó el cooldown
    if locked and btn.value() == 1 and utime.ticks_diff(now, last_fire) >= COOLDOWN_MS:
        locked = False

    utime.sleep_ms(2)
