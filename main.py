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

    # menyiapkan variabel
    html = ''

    # loop data mahasiswa dan ubah jadi string
    for d in content['mahasiswa']:
        html += f"<tr><td>{d['nim']}</td><td>{d['nama']}</td><td>{d['angkatan']}</td></tr>"

    # jadikan satu variabel html dengan html_jadi
    html_jadi = f'<html>'\
                f'<head><title>JSON</title></head>'\
                f'<body>'\
                f'<table border="1"><tr><td>NIM</td><td>Nama</td><td>Angkatan</td></tr>{html}</table>'\
                f'</body></html>'

    # tulis file baru
    with open('index_rendered.html', 'w') as f:
        f.write(html_jadi)

    # baca file baru
    with open('index_rendered.html', 'r') as bebas:
        html_ren = bebas.read()


    # Send HTTP response (json)
    response = f"HTTP/1.0 200 OK\n\n {html_ren}"
    client_connection.sendall(response.encode())
    client_connection.close()

# Close socket
server_socket.close()
