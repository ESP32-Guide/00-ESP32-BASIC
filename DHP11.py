'''
DHT11 Sensor

Temperature and Humidity Sensor

save the file as main.py 
'''
from machine import Pin
from dht import DHT11
from time import sleep

# let's choose GPIO PIN 15 
data_pin = 15


while True:
    s = DHT11(Pin(data_pin))
    
    s.measure()
    
    print(s.temperature(), s.humidity())
    
    # sleep for 1 sec
    sleep(1)
    

