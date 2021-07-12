#!/usr/bin

main() {
    # Use colors, for the terminal, unless they are not supported
    if which tput >/dev/null 2>&1; then
        ncolors=$(tput colors)
    fi
    if [ -t 1 ] && [ -n "$ncolors" ] && [ "$ncolors" -ge 8 ]; then
        RED="$(tput setaf 1)"
        GREEN="$(tput setaf 2)"
        YELLOW="$(tput setaf 3)"
        BLUE="$(tput setaf 4)"
        BOLD="$(tput bold)"
        NORMAL="$(tput sgr0)"
    else
        RED=""
        GREEN=""
        YELLOW=""
        BLUE=""
        BOLD=""
        NORMAL=""
    fi

    # Check python version installed
    printf "${BLUE}Checking python install...${NORMAL}\n"
    req=`python3 -c 'import sys; exit(1) if sys.version_info.major < 3 and sys.version_info.minor < 8 else exit(0)'`
    if [[ $req = 0 ]]; then
        printf "Python version 3.8 or higher is required."
    else
        printf "${GREEN}Python installed...${NORMAL}\n"
    fi

    printf "${YELLOW}Cloning Orange Sherbet${NORMAL}\n"
    hash git >/dev/null 2>&1 || {
        echo "ERROR: Please install git to use this utility\n"
        exit 1
    }

    git clone https://github.com/lennibot/orange-sherbet.git || {
        printf "ERROR: Cloning of the repository failed...\n"
        exit 1
    }

    printf "${BLUE}Creating Python virtual-enviroment${NORMAL}\n"
    cd envelope/ || {
    }
    python3 -m venv venv || {
        printf "Creating of virtual-environment failed...\n"
        exit 1
    }

    printf "${BLUE}Installing required packages..${NORMAL}\n"
    source venv/bin/activate
    pip install -r requirements.txt || {
        printf "installation of python packages failed...\n"
    }

    printf "${YELLOW}${BOLD}Orange Sherbet sucessfully installed!${NORMAL}\n"

} 

main