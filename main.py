import Orange0
from Orange0.batch_generator import BatchGen
import os

if __name__ == '__main__':
    if os.path.exists('./config.ini'):
        Orange0.read_config()

    else:
        pass
    Orange0.check_version()

    BatchGen()
