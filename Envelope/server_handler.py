import json
import os
from subprocess import Popen, PIPE
from threading import Thread
import requests
import logging
from typing import Optional

console_log = []


def delete_console_log():
    if os.path.exists('console.txt'):
        os.remove('console.txt')
    else:
        pass


def write_console_log(into):
    try:
        r = requests.post("http://localhost:5000/sendconsole", data=into)
        console_log.append(into)
    except Exception as e:
        logging.debug(e)


class ServerHandler(Thread):
    # initialize thread for server handler
    def __init__(self, config):
        Thread.__init__(self)
        self.install_location = config[0]
        self.server = Popen('./start.sh', stdout=PIPE, stdin=PIPE,
                            cwd=self.install_location, shell=True)
        self.output = ''

    def send_console(self, flask_server):
        flask_server.socket_console(self.output)

    def run(self):
        try:
            delete_console_log()
            logging.debug('SERVER HANDLER: Starting server handler thread...')
            # create a subprocess for the server (make the work directory the install location
            while True:
                # simply print server output to the command line for the time being
                output = self.server.stdout.readline()
                write_console_log(output)
                return_code = self.server.poll()
                if return_code is not None:
                    print('RETURN CODE', return_code)
                    # Process has finished, read rest of the output
                    self.server.stdout.close()
                    self.server.stdin.close()
                    break

        except Exception as e:
            raise e

    def join(self, timeout: Optional[float] = ...):
        self.server.stdin.write(str.encode('stop'))

    def command(self, command):
        self.server.stdin.write(str.encode(command + '\n'))
        self.server.stdin.flush()
