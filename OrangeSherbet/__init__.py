"""
'__init__' file for the main OrangeSherbet package.
"""
# python packages import
import atexit
import json
import logging
import os
import requests
from datetime import datetime
from collections import OrderedDict
# orange sherbet imports
from OrangeSherbet.batch_generator import BatchGen
from OrangeSherbet.server_handler import ServerHandler
from OrangeSherbet.update import UpdateServer
from OrangeSherbet.utils import ConfigInit
from OrangeSherbet.flask_server import FlaskServer

# check if logging folder exists
if os.path.exists('./logs'):
    log_file = f'./logs/{datetime.strftime(datetime.utcnow(), "%s")}.log'
else:
    os.makedirs('./logs', 0o777)
    log_file = f'./logs/{datetime.strftime(datetime.utcnow(), "%s")}.log'

logging.basicConfig(filename=log_file, level=logging.DEBUG)

config_init = ConfigInit()
config = config_init.get_values()

# Create the server folder as specified in the config
if os.path.exists(f'.{config[0]}') is False:
    os.makedirs(f'.{config[0]}', 0o777)
else:
    pass

server = ServerHandler(config)
flask = FlaskServer(server)


def create_server(mc_version, latest):
    try:
        # use the previous api calls to get the latest version of paper for MC version
        url = 'https://papermc.io/api/v1/paper/{MCVERSION}/{latest}/download'.format(MCVERSION=mc_version,
                                                                                     latest=latest)
        download = requests.get(url)
        with open('./paper_server/paper.jar', 'wb') as f:
            f.write(download.content)
        print('Sucessfully Downloaded PaperMC jar file')

        # generate the batch file for the new server using the parameters in config.ini
        batch = BatchGen(config)
        batch.batch_gen()
    except Exception as e:
        print(e)


# simple function that checks if paper.jar exists in the directory
def check_for_install():
    if os.path.exists('./paper_server/paper.jar') & os.path.exists('./paper_server/start.sh'):
        return True
    else:
        return False


def check_for_vh():
    # read the current version of the server from the version history file provided by the lovely papermc team
    if os.path.exists(f'{config[0]}/version_history.json'):
        f = open(f'{config[0]}/version_history.json', 'r')
        current_version = json.load(f)
        return current_version['currentVersion'].strip('() MC:')
    else:
        return None


def check_version():
    current_version = check_for_vh()
    config_version = config[1]
    api_mc_req = requests.get('https://papermc.io/api/v1/paper')  # request a list of the latest mc releases of paper
    paper_mc_version = api_mc_req.json()['versions'][0]
    print('Current MC version for paper: ' + paper_mc_version)
    if current_version is not None:
        current_paper_ver = current_version.strip('git-Paper-').split(" ", 1)
        print('Current MC version installed: ' + current_paper_ver[1].strip('()'))
        print('Current paper release installed: ' + current_paper_ver[0])
        version_used = 'vh'
    else:
        current_paper_ver = config_version
        version_used = 'config'

    try:
        paper_ver_req = requests.get('https://papermc.io/api/v1/paper/{MCVERSION}/'.format(MCVERSION=config_version))
        api_paper_ver = paper_ver_req.json()['builds']['latest']
        print(f'API VERSION: {api_paper_ver}')
    except Exception as e:
        print(e)

    minecraft_server_version = current_paper_ver[1].strip('()').strip('MC: ')

    if check_for_install():
        if check_for_vh() is None:
            server.start()
            flask.start()
        else:
            if minecraft_server_version != paper_mc_version and config_version != paper_mc_version:
                logging.info('Up To Date for current Minecraft release...')
                logging.warning('The Minecraft version on the newest release of Paper is newer than the installed '
                                'version. '
                                'Please ensure that all plugins are up to date before continuing.')
                logging.info('Newer Minecraft Version Available...')
                server.start()
                flask.start()
            elif config_version == paper_mc_version:
                logging.debug('Calling updater...')
                updater = UpdateServer(config, config_version, api_paper_ver)
                updater.start()
                updater.join()
                server.start()
                flask.start()
            else:
                if version_used == 'vh':
                    logging.info('Up To Date!')
                    server.start()
                    flask.start()
                elif version_used == 'config':
                    logging.debug('Calling updater...')
                    updater = UpdateServer(config, config_version, api_paper_ver)
                    updater.start()
                else:
                    logging.debug('Calling updater...')
                    updater = UpdateServer(config, config_version, api_paper_ver)
                    updater.start()
                    updater.join()
                    server.start()
                    flask.start()
    else:
        print('Paper is not installed.')
        # function to handle setting up server
        create_server(config_version, api_paper_ver)


def send_command(command):
    server.command(command=command)


def send_console_update():
    flask.socket_console()


def shutdown():
    server.join()
    flask.join()
