import configparser
import logging


class ConfigInit:
    def __init__(self):
        logging.debug('Reading config file...')
        config_parse = configparser.ConfigParser()
        try:
            config_parse.read('config.ini')
            install_location = config_parse['CONFIG']['PaperMCInstallLoc']
            server_version = config_parse['CONFIG']['MinecraftVersion']
            operating_system = config_parse['CONFIG']['OS']
            memory = config_parse['CONFIG']['Memory']
            self.config = [install_location, server_version, operating_system, memory]
            print(install_location + server_version)
        except Exception as e:
            print(e)

    def get_values(self):
        return self.config
