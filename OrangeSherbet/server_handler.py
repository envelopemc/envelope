from subprocess import Popen, PIPE
from threading import Thread


class ServerHandler(Thread):
    # initialize thread for server handler
    def __init__(self, config):
        Thread.__init__(self)
        self.install_location = config[0]

    def run(self):
        try:
            # create a subprocess for the server (make the work directory the install location
            server = Popen('./start.sh', stdout=PIPE,
                           universal_newlines=True, cwd=self.install_location, shell=True)
            while True:
                # simply print server output to the command line for the time being
                output = server.stdout.readline()
                print(output.strip())
                return_code = server.poll()
                if return_code is not None:
                    print('RETURN CODE', return_code)
                    # Process has finished, read rest of the output
                    for output in server.stdout.readlines():
                        print(output.strip())
                    break

        except Exception as e:
            raise e

