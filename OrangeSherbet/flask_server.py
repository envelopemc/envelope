import json
import logging
import os
from typing import Optional
from flask import Flask, request, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
from flask_socketio import SocketIO
from OrangeSherbet.web_serving import ServerThread

console_log = []


class FlaskServer:
    def __init__(self, minecraft_server, cache_dict):
        self.cache = cache_dict
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.cors = CORS(self.app)
        self.web_server = ServerThread(self.app)
        self.app.config['CORS_HEADERS'] = 'Content-Type'
        self.mc_server = minecraft_server
        self.parser = reqparse.RequestParser()
        self.sio = SocketIO(self.app, cors_allowed_origins="*")
        self.poller = Poller(self, self.cache)

        @self.sio.on('connected')
        def client_connected(data):
            print('connected' + data)
            if data == '':
                self.sio.emit('console_update', {'data': console_log})

        @self.app.route('/command', methods=['GET', 'POST'])
        def command_getter():
            if request.method == 'POST':
                try:
                    print(request.headers)
                    print(request.server)
                    print(request.form.to_dict())
                    command = request.form.get('cmd')
                    self.mc_server.command(command)
                    return jsonify(result={"status": 200})
                except Exception as e:
                    return e
            else:
                return request.method

        @self.app.route('/sendconsole', methods=['GET', 'POST'])
        def send_console():
            if request.method == 'POST':
                console_line = request.data.decode()
                console_log.append(console_line)
                self.sio.emit('console_update', {'data': console_line.strip('\n')})
                return jsonify(result={"status": 200})

    def socket_console(self, into):
        self.sio.emit('console_update', {'data': into})

    def start(self):
        self.sio.run(self.app, port=5000)

    def join(self, timeout: Optional[float] = ...):
        self.web_server.shutdown()
