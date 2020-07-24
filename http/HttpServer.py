import socket
import sys
import threading

from dispatcher.dispatcher import Dispatcher
from http.HttpRequest import HttpRequest

from http.HttpResponse import HttpResponse


class HttpServer:
    PACKET_SIZE = 1024

    def __init__(self):
        self.host = socket.gethostname()
        self.port = 8081
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def close(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except:
            pass

    def start(self):
        try:
            self.socket.bind((self.host, self.port))
        except Exception as e:
            self.socket.shutdown(socket.SHUT_RDWR)
        else:
            self.socket.listen()
            while True:
                (client, address) = self.socket.accept()
                client.settimeout(60)
                threading.Thread(target=self._handle_request, args=(client, address)).start()

    def _handle_request(self, client: socket, address):
        try:
            data = self._retrieve_request_data(client)
            request = HttpRequest(data)
            response = HttpResponse(request)
            Dispatcher.dispatch(response)
            client.send(response.render())
            client.close()
        except:
            sys.exit()

    def _retrieve_request_data(self, client):
        data = ''
        while True:
            temp = client.recv(self.PACKET_SIZE).decode()
            data += temp
            if len(temp) < self.PACKET_SIZE:
                break
        return data
