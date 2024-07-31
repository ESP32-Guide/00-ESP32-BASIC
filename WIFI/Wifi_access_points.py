'''
Wifi easily connect to wifi


''' 

import network

WiFi = network.WLAN(network.AP_IF)  # access point mode

WiFi.active(True)

WiFi.config(essid = 'ESP32_DOOR_LOCK', password = '12345678', authmode = network.AUTH_WPA_WPA2_PSK)

print(WiFi.ifconfig())
