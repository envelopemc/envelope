<img src="https://raw.githubusercontent.com/lennibot/envelope/dev/tools/logo.svg" align="right" height="250" width="250">

# Envelope

![GitHub](https://img.shields.io/github/license/metares/findomatic?style=flat-square)

Application for managing and updating PaperMC servers.

*Currently only planning releases for Unix based platforms (Linux & MacOS). Considering most VPS services utilize Unix-like operating systems, this is the natural choice. However, if demand for a Windows version is high, I will work on a Windows release.*

### Installation
_"main" branch contains the most updated stable release; "dev" branch contains the latest (not stable) build_
#### using curl

```shell
bash -c "$(curl -fsSL https://raw.githubusercontent.com/lennibot/envelope/main/tools/install.sh)"
```

#### using wget

```shell
bash -c "$(wget https://raw.githubusercontent.com/lennibot/envelope/main/tools/install.sh -O -)"
```

## Wiki
[View the Wiki here!](https://github.com/lennibot/envelope/wiki) This will contain the most up to date information on this project as well as help you understand the inner workings of Envelope.


## Required Python Packages
* requests
* Flask
* Flask-SocketIO
* Gevent

## Planned Features
* Web UI for managing server remotely.
* Automatic version control for PaperMC

## Contributing
Contributions are more than welcomed. 
Please for the time being, create a pull request and describe what you would like to add. I will write a CONTRIBUTING.md document when I feel it's required.

## License
[GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/)
