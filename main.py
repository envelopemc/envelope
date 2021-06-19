import Orange0
import os


if __name__ == '__main__':
    if os.path.exists('./orange0config.ini'):
        Orange0.read_config()

    else:
        pass
    Orange0.check_version()
