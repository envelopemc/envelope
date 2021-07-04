from subprocess import Popen, PIPE
from threading import Thread
from queue import Queue, Empty
import logging


class ServerHandler(Thread):
    # initialize thread for server handler
    def __init__(self, config):
        Thread.__init__(self)
        self.install_location = config[0]
        self.server = Popen('./start.sh', stdout=PIPE, stdin=PIPE,
                            universal_newlines=True, cwd=self.install_location, shell=True, bufsize=1)
        self.q = Queue()

    def run(self):
        try:
            logging.debug('SERVER HANDLER: Starting server handler thread...')
            # create a subprocess for the server (make the work directory the install location
            while True:
                # simply print server output to the command line for the time being
                output = self.server.stdout.readline()
                print(output.strip())
                return_code = self.server.poll()
                if return_code is not None:
                    print('RETURN CODE', return_code)
                    # Process has finished, read rest of the output
                    for output in self.server.stdout.readlines():
                        print(output.strip())
                    break

        except Exception as e:
            raise e

    def command(self, command):
        self.server.communicate(command)
