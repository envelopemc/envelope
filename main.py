import time
import signal
import OrangeSherbet

orange0 = OrangeSherbet

if __name__ == '__main__':
    try:
        """
        At the moment all this script does it check, update, and verify the current version of Paper.
        Eventually this main script will spawn several subprocesses that handle the various needs of a Minecraft Server.
        """
        orange0.check_version()
        print('thread check')

        time.sleep(50)
        print('test')
        orange0.send_command('help')
    except KeyboardInterrupt:
        orange0.shutdown()
