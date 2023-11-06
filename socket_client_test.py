import socket

BACKLOG = 5
BUFFER_SIZE = 1024
IP = "127.0.0.1"
PORT = 5008


class Client:
    def __init__(self, ip = IP, port = PORT):
        self.client_socket = self.create_socket(ip, port)

    def create_socket(self, ip, port):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, port))
        print("Connected to server at port {}".format(port))
        return client_socket

    def send_message(self, message):
        self.client_socket.send(message.encode())

    def receive_message(self):
        return self.client_socket.recv(BUFFER_SIZE).decode()

    def run(self):
        while True:
            message = input("Enter your message: ")
            self.send_message(message)
            response = self.receive_message()
            print(f"Server response: {response}")


client = Client()
client.run()