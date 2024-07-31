import socket

# ESP32 server details
esp32_ip = '192.168.1.100'
esp32_port = 8080

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((esp32_ip, esp32_port))
print(f"Connected to {esp32_ip}:{esp32_port}")

# Prepare the HTTP request
http_request = "GET /?LED=ON HTTP/1.1\r\nHost: {}\r\n\r\n".format(esp32_ip)

# Send the request to turn the LED on
client_socket.sendall(http_request.encode())
print("Sent request to turn LED on")

# Receive and print the response
response = client_socket.recv(4096)
print("Response from server:")
print(response.decode())

# Close the socket
client_socket.close()
print("Connection closed")
