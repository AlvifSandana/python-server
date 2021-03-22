import json
import socket

# host dan port
HOST = '127.0.0.1'
PORT = 8000

# membuat socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print('Listening on port %s ...' % PORT)

while True:
    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    # Get the client request
    request = client_connection.recv(1024).decode()
    print(request)

    # buka data.json
    fin = open('data.json')
    content = json.load(fin)
    ctn = json.dumps(content)
    fin.close()

    # Send HTTP response (json)
    response = f'HTTP/1.0 200 OK\nContent-Type: text-json\n\n{ctn}'
    client_connection.sendall(response.encode())
    client_connection.close()

# Close socket
server_socket.close()
