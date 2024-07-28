# save this file as main.py on micropython device

import machine
import time

led = machine.Pin(2, machine.Pin.OUT)

while True:
    time.sleep(1)
    led.value(1)    # light up
    
    time.sleep(1)
    led.value(0)    # light down
