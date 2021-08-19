"""
'__init__' file for the main Envelope package.
"""
# python packages import
import json
import logging
import os
from datetime import datetime
import requests

# orange sherbet imports
from Envelope.batch_generator import BatchGen
from Envelope.flask_server import FlaskServer
from Envelope.server_handler import ServerHandler
from Envelope.update import UpdateServer
from Envelope.utils import ConfigInit

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
if os.path.exists(f'{config[0]}') is False:
    os.makedirs(f'{config[0]}', 0o777)
else:
    pass

server = ServerHandler(config)
flask = FlaskServer(server)


def create_server(mc_version, latest):
    # primary function for creating the server
    try:
        # use the previous api calls to get the latest version of paper for MC version
        url = 'https://papermc.io/api/v1/paper/{MCVERSION}/{latest}/download'.format(MCVERSION=mc_version,
                                                                                     latest=latest)
        download = requests.get(url)
        with open(f'{config[0]}/paper.jar', 'wb') as f:
            f.write(download.content)
        print('Sucessfully Downloaded PaperMC jar file')

        # generate the batch file for the new server using the parameters in config.ini
        batch = BatchGen(config)
        batch.batch_gen()
    except Exception as e:
        print(e)


# simple function that checks if paper.jar exists in the directory
def check_for_install():
    if os.path.exists(f'{config[0]}/paper.jar') & os.path.exists(f'{config[0]}/start.sh'):
        return True
    else:
        return False


# checks for the version history file and uses it to tell the version, if not found return None
def check_for_vh():
    # read the current version of the server from the version history file provided by the lovely papermc team
    if os.path.exists(f'{config[0]}/version_history.json'):
        f = open(f'{config[0]}/version_history.json', 'r')
        current_version = json.load(f)
        return current_version['currentVersion'].strip('() MC:')
    else:
        return config[1]


def check_version():
    # local paper version
    local_version = check_for_vh()

    api_mc_req = requests.get('https://papermc.io/api/v1/paper')  # request a list of the latest mc releases of paper
    # latest minecraft release supported by paper
    latest_version = api_mc_req.json()['versions'][0]

    print('Current MC version for paper: ' + latest_version)
    current_local_paper_ver = local_version.strip('git-Paper-').split(" ", 1)
    print('Current MC version installed: ' + current_local_paper_ver[1].strip('()'))
    print('Current paper release installed: ' + current_local_paper_ver[0])

    local_minecraft_server_version = current_local_paper_ver[1].strip('()').strip('MC: ')

    print(local_minecraft_server_version)

    paper_ver_req = requests.get(f'https://papermc.io/api/v1/paper/{local_minecraft_server_version}/')
    api_paper_ver = paper_ver_req.json()['builds']['latest']
    print(f'API VERSION: {api_paper_ver}')

    if check_for_install():
        # Simplified version check function, simply compares the current paper version (ie like 89) and then checks the
        # the paper version of minecraft

        if local_minecraft_server_version != latest_version and current_local_paper_ver[0] != paper_ver_req:
            logging.info('Up To Date for current Minecraft release...')
            logging.warning('The Minecraft version on the newest release of Paper is newer than the installed '
                            'version. '
                            'Please ensure that all plugins are up to date before continuing.')
            logging.info('Newer Minecraft Version Available...')
            server.start()
            flask.start()
        elif int(current_local_paper_ver[0]) != int(api_paper_ver):
            logging.debug('Calling updater...')
            updater = UpdateServer(config, local_minecraft_server_version, api_paper_ver)
            updater.start()
            updater.join()
            server.start()
            flask.start()
        elif int(current_local_paper_ver[0]) == int(api_paper_ver):
            server.start()
            flask.start()
    else:
        print('Paper is not installed.')
        # function to handle setting up server
        create_server(config[1], api_paper_ver)


def send_command(command):
    server.command(command=command)


def send_console_update():
    flask.socket_console()


def shutdown():
    server.join()
    flask.join()
