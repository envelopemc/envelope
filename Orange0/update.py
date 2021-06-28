import logging
import os
import shutil
import requests
import threading


class UpdateServer(threading.Thread):
    def __init__(self, config, mc_version, latest):
        # simply read the config setup by the user (or the default values)
        threading.Thread.__init__(self)
        self.mc_version = mc_version
        self.latest = latest
        self.install_location = config[0]
        self.paper_api_url = 'https://papermc.io/api/v1/paper'

    def run(self):
        try:
            # use the previous api calls to get the latest version of paper for MC version
            url = 'https://papermc.io/api/v1/paper/{MCVERSION}/{latest}/download'.format(MCVERSION=self.mc_version,
                                                                                         latest=self.latest)
            logging.debug('UPDATER: Downloading new Paper jar file...')
            download = requests.get(url)

            # make a temporary directory to download the new jar into
            if os.path.exists('./temp'):
                pass
            else:
                os.makedirs('./temp', 0o777)

            # download the new jar into the temp directory
            with open('./temp/paper.jar', 'wb') as f:
                f.write(download.content)
            logging.debug('UPDATER: Sucessfully Downloaded PaperMC jar file...')

            # remove old jar from the primary directory
            os.remove('./paper_server/paper.jar')
            logging.debug('UPDATER: Moving file in place...')
            # move new jar into primary directory
            shutil.move('./temp/paper.jar', '{INSTALL_LOC}/paper.jar'.format(INSTALL_LOC=self.install_location))
            logging.debug('UPDATER: Cleaning up...')
            os.rmdir('./temp')  # removes the temp dir

        except Exception as e:
            print(e)
