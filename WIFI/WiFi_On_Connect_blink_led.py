'''
if wifi is not connected then blink led at pin 4
else blink 2
'''

import network
from machine import Pin, Timer
import time

# Initialize the LED pin
led = Pin(2, Pin.OUT)
Gled = Pin(4, Pin.OUT)

# Initialize the timer
timer1 = Timer(0)

# Function to indicate AP mode is active
def ap_mode_active():
    timer1.deinit()
    Gled.value(0)
    # LED blinking to indicate AP mode is active
    timer1.init(period=100, mode=Timer.PERIODIC, callback=lambda t: led.value(not led.value()))

# Function to indicate AP mode is inactive
def ap_mode_inactive():
    # LED stable OFF
    timer1.deinit()
    led.value(0)
    timer1.init(period=100, mode=Timer.PERIODIC, callback=lambda t: Gled.value(not Gled .value()))

# Set up WiFi in access point mode
WiFi = network.WLAN(network.AP_IF)
# Restarting WiFi
WiFi.active(False)
time.sleep(0.5)
WiFi.active(True)

WiFi.config(essid='ESP32_DOOR_LOCK', password='12345678', authmode=network.AUTH_WPA_WPA2_PSK)

# Print the IP configuration
print(WiFi.ifconfig())

def check():
    timeout = 0  # WiFi Connection Timeout variable
    if not WiFi.isconnected():
        print('connecting..')
        while (not WiFi.isconnected() and timeout < 5):
            print(5 - timeout)
            timeout = timeout + 1
            time.sleep(1)
            ap_mode_inactive()
            
    if WiFi.isconnected():
        print('Connected...')
        print('network config:', WiFi.ifconfig())
        # Indicate AP mode is active by blinking the LED
        ap_mode_active()

# Keep the AP mode running indefinitely
while True:
    check()
    time.sleep(1)  # Add a small delay to prevent overwhelming the CPU

