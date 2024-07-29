'''
DHT11 Sensor

Temperature and Humidity Sensor

if humidity is high then off the LED

:) Blow air from your mouth near sensor it will increase humidity :) Good for testing

save the file as main.py 
'''
from machine import Pin
from dht import DHT11
from time import sleep

# let's choose GPIO PIN 15 
data_pin = 15

# let's connect led at pin 2
LED = Pin(2, Pin.OUT)

while True:
    s = DHT11(Pin(data_pin))
    
    s.measure()
    
    print(s.temperature(), s.humidity())
    
    if s.humidity() >= 80:
        LED.value(0)
    else: 
        LED.value(1)
    
    # sleep for 1 sec
    sleep(1)
    

