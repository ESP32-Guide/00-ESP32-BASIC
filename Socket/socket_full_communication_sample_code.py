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

# Connect to WiFi
wifi.connect('vivo 1851', '987654321')

# Function to indicate AP mode is active
def ap_mode_active():
    timer1.deinit()
    GLED.value(0)
    timer1.init(period=100, mode=Timer.PERIODIC, callback=lambda t: YLED.value(not YLED.value()))

# Function to start blinking for 15 seconds
def power_for_15_sec():
    GLED.value(0)
    timer1.init(period=100, mode=Timer.PERIODIC, callback=lambda t: GLED.value(not GLED.value()))
    timer1.init(period=15000, mode=Timer.ONE_SHOT, callback=lambda t: stop_blinking())

# Function to stop blinking
def stop_blinking():
    timer1.deinit()
    GLED.value(0)

# Function to indicate AP mode is inactive
def ap_mode_inactive():
    timer1.deinit()
    YLED.value(0)
    timer1.init(period=100, mode=Timer.PERIODIC, callback=lambda t: GLED.value(not GLED.value()))

# Attempt to connect to WiFi
print('Connecting to WiFi...')
if not wifi.isconnected():
    while not wifi.isconnected():
        ap_mode_inactive()
        time.sleep(1)

if wifi.isconnected():
    ap_mode_active()
    print('Connected...')
    print('Network config:', wifi.ifconfig())
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

# HTML Document
html_Greeting = '''<!DOCTYPE html>
<html>
    <head>
        <title>ESP32 Webserver</title>
    </head>
    <body>
        <center><h2>ESP32 Webserver</h2></center>
        <form>
            <center>
                <h3>Thank You!</h3>
                <p> Please lock the door properly </p>
            </center>
        </form>
    </body>
</html>
'''

# Ensure the LED is off initially
GLED.value(0)

# Function to restart the server
def restart_server():
    print('Restarting server...')
    time.sleep(5)  # Delay to allow resources to be freed
    return start_server()

# Initializing Socket with retry logic
def start_server(max_retries=5, retry_delay=5):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Host = ''  # Empty means it will allow all IP addresses to connect
    Port = 80   # HTTP port

    for attempt in range(max_retries):
        try:
            s.bind((Host, Port))  # Bind to host and port
            s.listen(5)  # Handle a maximum of 5 clients at a time
            print('Server listening on port', Port)
            return s
        except OSError as e:
            print(f'Error binding socket (attempt {attempt + 1}/{max_retries}): {e}')
            s.close()
            time.sleep(retry_delay)
        except Exception as e:
            print(f'Unexpected error (attempt {attempt + 1}/{max_retries}): {e}')
            s.close()
            time.sleep(retry_delay)
    
    return None

# Retry starting the server with a full restart
server_socket = start_server()

if not server_socket:
    # If server couldn't start, try restarting the process
    server_socket = restart_server()

if server_socket:
    # Main loop
    while True:
        try:
            connection_socket, address = server_socket.accept()
            print("Got a connection from", address)
            request = connection_socket.recv(1024)
            print("Content", request)
            request = str(request)
            print("-------------- request ", request)
            LED_ON = request.find('/?LED=ON')
            LED_OFF = request.find('/?LED=OFF')

            if LED_ON != -1:
                GLED.value(1)
                print("LED turned ON")
                response = html_Greeting
                connection_socket.sendall(response)
                time.sleep(10) # sleep for 10 sec
                print("Thank You !")
                
            if LED_OFF != -1:
                GLED.value(0)
                print("LED turned OFF")

            response = html
            connection_socket.send('HTTP/1.1 200 OK\r\n')
            connection_socket.send('Content-Type: text/html\r\n')
            connection_socket.send('Connection: close\r\n\r\n')
            connection_socket.sendall(response)
            connection_socket.close()
        except Exception as e:
            print('Error:', e)
            if 'connection_socket' in locals():
                connection_socket.close()
            continue
else:
    print('Server could not start after multiple attempts. Restarting the process is needed.')

