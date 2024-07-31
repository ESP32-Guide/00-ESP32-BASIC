import network
import time

# Set up WiFi in station mode
WiFi = network.WLAN(network.STA_IF)
WiFi.active(True)

# Connect to the WiFi network
WiFi.connect('vivo Y21A', '1234567890')

# Wait for the connection with a timeout
timeout = 10  # seconds
start = time.time()

while not WiFi.isconnected() and (time.time() - start) < timeout:
    time.sleep(1)

# Check if the connection was successful
if WiFi.isconnected():
    print("Connected successfully!")
    print(WiFi.ifconfig())
else:
    print("Failed to connect within the timeout period.")

