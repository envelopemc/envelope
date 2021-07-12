import configparser
import logging


class ConfigInit:
    def __init__(self):
        logging.debug('Reading config file...')
        config_parse = configparser.ConfigParser()
        try:
            config_parse.read('config.ini')
            install_location = config_parse['CONFIG']['INSTALL_LOCATION']
            server_version = config_parse['CONFIG']['MINECRAFT_VERSION']
            operating_system = config_parse['CONFIG']['OS']
            memory = config_parse['CONFIG']['SERVER_MEMORY']
            endpoint_port = config_parse['CONFIG']['ENDPOINT_PORT']
            self.config = [install_location, server_version, operating_system, memory, endpoint_port]
        except Exception as e:
            print(e)

    def get_values(self):
        return self.config

