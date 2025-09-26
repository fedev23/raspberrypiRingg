import network, time
wlan = None

def connect(ssid, password, timeout_ms=15000):
    global wlan
    if wlan is None:
        wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, password)
        t0 = time.ticks_ms()
        while not wlan.isconnected():
            if time.ticks_diff(time.ticks_ms(), t0) > timeout_ms:
                return False, None
            time.sleep_ms(200)
    return True, wlan.ifconfig()[0]

def off():
    global wlan
    if wlan:
        wlan.active(False)
