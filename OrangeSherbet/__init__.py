import requests
import json
import os
import shutil
import configparser
from datetime import datetime
import logging
from OrangeSherbet.batch_generator import BatchGen
from OrangeSherbet.update import UpdateServer
from OrangeSherbet.utils import ConfigInit

log_file = './logs/{}.log'.format(datetime.strftime(datetime.utcnow(), "%s"))

logging.basicConfig(filename=log_file, level=logging.DEBUG)

config_init = ConfigInit()
config = config_init.get_values()


def create_server(mc_version, latest):
    try:
        if os.path.exists('./paper_server') is False:
            os.makedirs('./paper_server', 0o777)
        else:
            pass

        # use the previous api calls to get the latest version of paper for MC version
        url = 'https://papermc.io/api/v1/paper/{MCVERSION}/{latest}/download'.format(MCVERSION=mc_version,
                                                                                     latest=latest)
        download = requests.get(url)
        with open('./paper_server/paper.jar', 'wb') as f:
            f.write(download.content)
        print('Sucessfully Downloaded PaperMC jar file')

        # generate the batch file for the new server using the parameters in config.ini
        batch = BatchGen()
        batch.batch_gen()
    except Exception as e:
        print(e)


# simple function that checks if paper.jar exists in the directory
def check_for_install():
    if os.path.exists('./paper_server/paper.jar'):
        return True
    else:
        return False


def check_for_vh():
    # read the current version of the server from the version history file provided by the lovely papermc team
    if os.path.exists('{}/version_history.json'.format(config[0])):
        f = open('{}/version_history.json'.format(config[0]), 'r')
        current_version = json.load(f)
        return current_version[1].strip('() MC:')
    else:
        return None


def check_version():
    current_version = check_for_vh()
    config_version = config[1]
    api_mc_req = requests.get('https://papermc.io/api/v1/paper')  # request a list of the latest mc releases of paper
    paper_mc_version = api_mc_req.json()['versions'][0]
    print('Current MC version for paper: ' + paper_mc_version)
    if current_version is not None:
        current_paper_ver = current_version['currentVersion'].strip('git-Paper-').split(" ", 1)
        print('Current MC version installed: ' + current_paper_ver[1].strip('()'))
        print('Current paper release installed: ' + current_paper_ver[0])
        version_used = 'version_history'
    else:
        current_paper_ver = config_version
        version_used = 'config'

    try:
        paper_ver_req = requests.get('https://papermc.io/api/v1/paper/{MCVERSION}/'.format(MCVERSION=config_version))
        api_paper_ver = paper_ver_req.json()['builds']['latest']
    except Exception as e:
        print(e)

    if check_for_install():
        pass
    else:
        print('Paper is not installed.')
        # function to handle setting up server
        create_server(config_version, api_paper_ver)

    if current_paper_ver != paper_mc_version:
        logging.info('Up To Date for current Minecraft release...')
        logging.warning('The Minecraft version on the newest release of Paper is newer than the installed version. '
                        'Please ensure that all plugins are up to date before continuing.')
        logging.info('Newer Minecraft Version Available...')
    else:
        if version_used == 'version_history':
            if current_paper_ver == paper_mc_version:
                logging.info('Up To Date!')
            else:
                logging.debug('Calling updater...')
                updater = UpdateServer(config_version, api_paper_ver)
                updater.start()
        elif version_used == 'config':
            logging.debug('Calling updater...')
            updater = UpdateServer(config, config_version, api_paper_ver)
            updater.start()
