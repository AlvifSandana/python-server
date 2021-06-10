# Module name : webserver.py
# created by alvifsandanamahardika at 6/10/21

import socket
import sys
import time
import threading


class WebServer(object):
    """
    Simple HTTP server class
    """

    def __init__(self, port=8080):
        # define socket with address family and socket type.
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # define host
        self.host = socket.gethostname().split('.')[0]
        # define port
        self.port = port
        # define working web directi=ory
        self.htdocs_dir = 'htdocs'

    def start(self):
        """
        Create and bind a socket to launch the server
        """
        try:
            print(f'Starting server on {self.host}:{self.port}')
            # try to binding the socket
            self.socket.bind((self.host, self.port))
            print(f'Server started on port {self.port}')
        except Exception as e:
            print(f'Error: Could not bind to port {self.port}')
            print(f'Information: {e}')
            # handle exception and shutdown the server
            self.shutdown()
            sys.exit(1)
        self._listen()

    def shutdown(self):
        """
        Shutdown the server
        """
        try:
            print("Shutting down server...")
            self.socket.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print(f'Error: {e}')
            sys.exit(1)

    @staticmethod
    def _generate_headers(res_code):
        """
        Generate HTTP response headers.
        :param res_code: HTTP response code. 200 and 404 supported
        :return: A formatted HTTP header for the given response code
        """
        # initialize header
        header = ''
        # check response code
        if res_code == 200:
            header += 'HTTP/1.1 200 OK\n'
        elif res_code == 404:
            header += 'HTTP/.1 404 Not Found\n'
        # Add time record to the header
        now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        header += f'Date: {now}'
        # Add server name
        header += 'Server: Simple-Python-Server\n'
        # indicate that the server connection will be closed after
        # completing the requests
        header += 'Connection: close\n\n'
        return header

    def _listen(self):
        """
        Listen on self.port for any incoming connection.
        """
        self.socket.listen(5)
        while True:
            client, address = self.socket.accept()
            client.settimeout(60)
            print(f'Received connection from {address}')
            threading.Thread(target=self._handle_client, args=(client, address)).start()

    def _handle_client(self, client, address):
        """
        Main loop for handling connected clients and serving files from htdocs
        :param client: socket client from accept()
        :param address: socket address from accept()
        """
        res_data = b''
        packet_size = 1024
        while True:
            print('Client', client)
            data = client.recv(packet_size).decode()

            if not data: break

            req_method = data.split(' ')[0]
            print(f'Method: {req_method}')
            print(f'Request Body: {data}')

            if req_method == 'GET' or req_method == 'HEAD':
                file_req = data.split(' ')[1]
                file_req = file_req.split('?')[0]

                if file_req == '/':
                    file_req = '/index.html'

                filepath_to_serve = self.htdocs_dir + file_req
                print(f'Serving page [{filepath_to_serve}]')

                try:
                    f = open(filepath_to_serve, 'rb')
                    if req_method == 'GET':
                        res_data = f.read()
                    f.close()
                    res_header = self._generate_headers(200)
                except Exception as e:
                    print(f'Error: {e}\n\n')
                    print('File not found. Serving 404 page.\n\n')
                    res_header = self._generate_headers(404)
                    if req_method == 'GET':
                        f = open(self.htdocs_dir + '/404.html', 'rb')
                        res_data = f.read()

                response = res_header.encode()
                if req_method == 'GET':
                    response += res_data

                client.send(response)
                client.close()
                break
            else:
                print(f'Unknown HTTP request method: {req_method}')
