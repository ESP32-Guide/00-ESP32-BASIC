'''
dynamic ip host

Socket

'''

from machine import Pin, Timer
import usocket as socket
import time
import network

# Initialize the timer
timer1 = Timer(0)

# LED
YLED = Pin(2, Pin.OUT)
GLED = Pin(4, Pin.OUT)

wifi = network.WLAN(network.STA_IF)

# Restarting WiFi
wifi.active(False)
time.sleep(0.5)
wifi.active(True)

# Get the IP address of the ESP32
host_ip = wifi.ifconfig()[0]

try:
    print(host_ip)
except:
    pass

wifi.connect('vivo 1851', '987654321')

# Function to indicate AP mode is active
def ap_mode_active():
    timer1.deinit()
    GLED.value(0)
    # LED blinking to indicate AP mode is active
    timer1.init(period=100, mode=Timer.PERIODIC, callback=lambda t: YLED.value(not YLED.value()))

# Function to indicate AP mode is inactive
def ap_mode_inactive():
    # LED stable OFF
    timer1.deinit()
    YLED.value(0)
    timer1.init(period=100, mode=Timer.PERIODIC, callback=lambda t: GLED.value(not GLED.value()))

# Attempt to connect to WiFi
if not wifi.isconnected():
    print('connecting..')
    while not wifi.isconnected():  # Increased timeout for reliability
        ap_mode_inactive()
        time.sleep(1)
     

if wifi.isconnected():
    ap_mode_active()
    print('Connected...')
    print('network config:', wifi.ifconfig())
else:
    print('Failed to connect to WiFi')
    raise Exception('WiFi connection failed')

# HTML Document
html = '''<!DOCTYPE html>
<html>
    <head>
        <title>ESP32 Webserver</title>
    </head>
    <body>
        <center><h2>ESP32 Webserver</h2></center>
        <form>
            <center>
                <h3>LED Control</h3>
                <button name="LED" value="ON" type="submit">ON</button>
                <button name="LED" value="OFF" type="submit">OFF</button>
            </center>
        </form>
    </body>
</html>
'''

# Ensure the LED is off initially
GLED.value(0)

# Initializing Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET - Internet Socket, SOCK_STREAM - TCP protocol

Host = ''  # Empty means it will allow all IP addresses to connect
Port = 80  # HTTP port
s.bind((Host, Port))  # Host, Port

s.listen(5)  # It will handle a maximum of 5 clients at a time

print('Server listening on port', Port)

# Main loop
while True:
    try:
        connection_socket, address = s.accept()  # Storing Conn_socket & address of new client connected
        print("Got a connection from", address)
        request = connection_socket.recv(1024)  # Storing Response coming from client
        print("Content", request)  # Printing Response
        request = str(request)  # Converting Bytes to String
        # Comparing & Finding Position of word in String
        LED_ON = request.find('/?LED=ON')
        LED_OFF = request.find('/?LED=OFF')

        if LED_ON != -1:
            GLED.value(1)
            print("LED turned ON")
        if LED_OFF != -1:
            GLED.value(0)
            print("LED turned OFF")

        # Sending HTML document in response every time to all connected clients
        response = html
        connection_socket.send('HTTP/1.1 200 OK\r\n')
        connection_socket.send('Content-Type: text/html\r\n')
        connection_socket.send('Connection: close\r\n\r\n')
        connection_socket.sendall(response)

        # Closing the socket
        connection_socket.close()
    except Exception as e:
        print('Error:', e)
        if 'connection_socket' in locals():
            connection_socket.close()
        continue

