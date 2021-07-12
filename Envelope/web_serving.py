"""
Class for handling the various threads needed for the program to function correctly.
"""
from gevent.pywsgi import WSGIServer


class ServerThread():

    def __init__(self, app):
        self.http_server = WSGIServer(('', 5000), app)

    def run(self):
        self.http_server.serve_forever()

    def shutdown(self):
        self.http_server.stop()
