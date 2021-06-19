"""
This class is for generating the proper batch file used to start the server in ./paper_server.

Class will read config for OS
"""

import Orange0


class BatchGen:
    def __init__(self):
        config = Orange0.read_config()
        operating_system = config[2]
        print(operating_system)
