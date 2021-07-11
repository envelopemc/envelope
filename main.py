import time
import signal
import OrangeSherbet

orange = OrangeSherbet

if __name__ == '__main__':
    try:
        """
        At the moment all this script does it check, update, and verify the current version of Paper.
        Eventually this main script will spawn several subprocesses that handle the various needs of a Minecraft Server.
        """
        orange.check_version()

    except KeyboardInterrupt:
        orange.shutdown()
