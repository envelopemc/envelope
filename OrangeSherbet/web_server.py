from flask import Flask
from threading import Thread


class FlaskServer(Thread):
    def __init__(self, server):
        Thread.__init__(self)
        self.app = Flask(__name__)

    def run(self):
        self.app.run(port=6969)