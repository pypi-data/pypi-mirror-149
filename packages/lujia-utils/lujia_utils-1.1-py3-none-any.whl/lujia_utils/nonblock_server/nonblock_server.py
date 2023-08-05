from http.server import HTTPServer
import time
import threading


class NonBlockServer(HTTPServer):
    def __init__(self, server_address, handler, bind_and_activate=True):
        super().__init__(server_address, handler, bind_and_activate)

    def shutdown_thread(self):
        time.sleep(1)
        self.shutdown()

    def serve_forever(self, poll_interval=0.5):
        t = threading.Thread(target=self.shutdown_thread)
        t.start()
        super().serve_forever(poll_interval)
        t.join()
