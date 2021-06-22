import requests
import json
import os
import shutil
import configparser
from Orange0.batch_generator import BatchGen


def read_config():
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')
        install_location = config['CONFIG']['PaperMCInstallLoc']
        server_version = config['CONFIG']['MinecraftVersion']
        operating_system = config['CONFIG']['OS']
        memory = config['CONFIG']['Memory']
        print(install_location + server_version)
        return [install_location, server_version, operating_system, memory]
    except Exception as e:
        print(e)


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

        batch = BatchGen()
        batch.batch_gen()
    except Exception as e:
        print(e)


def update_server(mc_version, latest):
    try:
        # use the previous api calls to get the latest version of paper for MC version
        url = 'https://papermc.io/api/v1/paper/{MCVERSION}/{latest}/download'.format(MCVERSION=mc_version,
                                                                                     latest=latest)
        download = requests.get(url)

        # make a temporary directory to download the new jar into
        if os.path.exists('./temp'):
            pass
        else:
            os.makedirs('./temp', 0o777)

        # download the new jar into the temp directory
        with open('./temp/paper.jar', 'wb') as f:
            f.write(download.content)
        print('Sucessfully Downloaded PaperMC jar file...')

        # remove old jar from the primary directory
        os.remove('./paper_server/paper.jar')
        print('Moving file in place...')
        # move new jar into primary directory
        shutil.move('./temp/paper.jar', './paper_server/paper.jar')
        print('Cleaning up...')
        os.rmdir('./temp')  # removes the temp dir

    except Exception as e:
        print(e)


# simple function that checks if paper.jar exists in the directory
def check_for_install():
    if os.path.exists('./paper_server/paper.jar'):
        return True
    else:
        return False


def check_version():
    # read the current version of the server from the version history file provided by the lovely papermc team
    config = read_config()
    if os.path.exists('{}/version_history.json'.format(config[0])):
        f = open('{}/version_history.json'.format(config[0]), 'r')
        current_version = json.load(f)
    else:
        current_version = None

    config_version = config[1]

    api_mc_req = requests.get('https://papermc.io/api/v1/paper')  # request a list of the latest mc releases of paper
    paper_mc_version = api_mc_req.json()['versions'][0]
    print('Current MC version for paper: ' + paper_mc_version)
    if current_version is not None:
        current_paper_ver = current_version['currentVersion'].strip('git-Paper-').split(" ", 1)
        print('Current MC version installed: ' + current_paper_ver[1].strip('()'))
        print('Current paper release installed: ' + current_paper_ver[0])
    elif config_version is not None:
        current_paper_ver = config_version
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

    if current_paper_ver[1].strip('() MC:') != paper_mc_version:
        print('Up To Date for current Minecraft version...')
        with open('Old_Version.txt', 'w') as f:
            f.write('The Minecraft version on the newest release of Paper is newer than the installed version. Please '
                    'ensure that all plugins are up to date before continuing.')
        print('Newer Minecraft Version Available...')
    else:
        if os.path.exists('Old_Version.txt'):
            os.remove('Old_Version.txt')
        if int(current_paper_ver[0]) == int(api_paper_ver):
            print('Up To Date!')
        else:
            print('Updating!')
            update_server(config_version, api_paper_ver)