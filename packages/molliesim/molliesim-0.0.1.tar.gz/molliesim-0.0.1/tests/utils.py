from threading import Thread
from http.server import ThreadingHTTPServer
from unittest import TestCase
import time

from molliesim.server import MollieRequestHandler
from molliesim import storage


class TestServer(Thread):
    def __init__(self, addr="localhost", port=3333):
        self.server = ThreadingHTTPServer((addr, port), MollieRequestHandler)
        super().__init__()

    def run(self):
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()


class MollieTestCase(TestCase):


    def setUp(self):
        self.server = TestServer()
        self.server.start()


    def tearDown(self):
        self.server.stop()
        self.server.join()
        storage.clear()
