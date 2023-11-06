import socket
import os

BACKLOG = 5
BUFFER_SIZE = 1024
IP = "127.0.0.1"
PORT = 5008

class SocketServer:
    def __init__(self, ip = IP, port = PORT):
        self.server_socket = self.create_socket(ip, port)
        self.client_socket = None

    def create_socket(self, ip, port):
        # create an INET, STREAMing socket
        server_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        # if already used the port, reuse it
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind the socket to a public host, and a well-known port
        server_socket.bind((ip, port))
        # become a server socket
        server_socket.listen(BACKLOG)
        print("Server is listening on port {}".format(port))
        return server_socket

    def accept_connections(self):
        print("Waiting for connection...")
        (self.client_socket, address) = self.server_socket.accept()
        print(f"Connection from {address}")
        
    def receive_message(self):
        return self.client_socket.recv(BUFFER_SIZE).decode()

    def send_message(self, message):
        self.client_socket.send(message.encode())

    def close_connection(self):
        self.client_socket.close()

    def run(self):
        self.accept_connections()
        while True:
            data = self.receive_message()
            print(f"Received: {data}")
            self.send_message(f"Received: {data}")
        self.close_connection()

server = SocketServer()
server.run()