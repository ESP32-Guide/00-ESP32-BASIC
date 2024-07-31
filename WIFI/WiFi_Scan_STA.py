'''
Wifi scan all nearby stations


''' 

import network

WiFi = network.WLAN(network.STA_IF)  # station mode

WiFi.active(True)

networks = WiFi.scan()

print(networks)
