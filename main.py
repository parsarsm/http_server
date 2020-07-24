import threading

from http.HttpServer import HttpServer


class Main:
    def __init__(self):
        self.server = None
        self.thread = None

    def run(self):
        self.server = HttpServer()
        self.thread = threading.Thread(target=self.server.start)
        self.thread.start()

        while True:
            if 'exit'.startswith(input().lower()):
                exit(1)

Main().run()
