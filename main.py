import time
import signal
import Envelope

if __name__ == '__main__':
    envelope = Envelope

    try:
        """
        At the moment all this script does it check, update, and verify the current version of Paper.
        Eventually this main script will spawn several subprocesses that handle the various needs of a Minecraft Server.
        """

        envelope.check_version()

    except KeyboardInterrupt:
        envelope.shutdown()
