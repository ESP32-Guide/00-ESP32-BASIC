'''
timer in ESP32
'''

from machine import Timer, Pin


LED = Pin(2, Pin.OUT)

timer = Timer(0)

# PERIOD To call back to function
timer.init(period = 1000, mode = Timer.PERIODIC, callback = lambda t: LED.value(not LED.value()))
