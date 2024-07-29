'''
ESP32 OLED

CONNECT SCL - PIN(22)
SDA - PIN(21)
GND - GND
VCC - 3V3

Save the library ssd1306.py

'''

from machine import Pin, SoftI2C
import ssd1306
from time import sleep

# ESP32 Pin assignment 
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

# ESP8266 Pin assignment
#i2c = SoftI2C(scl=Pin(5), sda=Pin(4))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

oled.text('WELCOME!', 0, 0)
oled.text('Hello, RAJ!', 0, 10)
oled.text('GOOD MORNING!', 0, 30)
oled.text('ESP32 - IOT!', 0, 50)
        
oled.show()
