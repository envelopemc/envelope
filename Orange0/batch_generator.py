"""
This class is for generating the proper batch file used to start the server in ./paper_server.

Class will read config for OS and generate batch file based on the needs of the OS.

Using the awesome flags provided by Aikar.
https://aikar.co/2018/07/02/tuning-the-jvm-g1gc-garbage-collector-flags-for-minecraft/
"""

import Orange0
import os


class BatchGen:
    def __init__(self):
        # simply read the config setup by the user (or the default values)
        config = Orange0.read_config()
        # gets the operating system
        operating_system = os.name
        # set instance variables
        self.install_location = config[0]
        self.memory = config[3]
        self.operating_system = operating_system
        print(operating_system) # debug stuff
        # Aikar's Flags
        self.start_flags = 'java -Xms{MEMORY}G -Xmx{MEMORY}G ' \
                           '-XX:+UseG1GC-XX:+ParallelRefProcEnabled-XX:MaxGCPauseMillis=200-XX' \
                           ':+UnlockExperimentalVMOptions-XX:+DisableExplicitGC-XX:+AlwaysPreTouch-XX' \
                           ':G1HeapWastePercent=5-XX:G1MixedGCCountTarget=4-XX:G1MixedGCLiveThresholdPercent=90-XX' \
                           ':G1RSetUpdatingPauseTimePercent=5-XX:SurvivorRatio=32-XX:+PerfDisableSharedMem-XX' \
                           ':MaxTenuringThreshold=1-XX:G1NewSizePercent={G1NewSizePercent}-XX:G1MaxNewSizePercent={' \
                           'G1MaxNewSizePercent}-XX' \
                           ':G1HeapRegionSize={G1HeapRegionSize}-XX:G1ReservePercent={' \
                           'G1ReservePercent}-XX:InitiatingHeapOccupancyPercent={InitiatingHeapOccupancyPercent}-Dusing' \
                           '.aikars.flags=https://mcflags.emc.gs-Daikars.new.flags=true -jar paper.jar nogui'

    def batch_gen(self):
        # start unix-based generation
        if self.operating_system == 'posix':
            with open('{INSTALL_LOCATION}/start.sh'.format(INSTALL_LOCATION=self.install_location), 'w') as f:
                # check memory size for server
                if self.memory > '12':
                    G1NewSizePercent = '30'
                    G1MaxNewSizePercent = '40'
                    G1HeapRegionSize = '8M'
                    G1ReservePercent = '20'
                    InitiatingHeapOccupancyPercent = '15'
                    f.write(self.start_flags.format(MEMORY=self.memory, G1NewSizePercent=G1NewSizePercent,
                                                    G1MaxNewSizePercent=G1MaxNewSizePercent,
                                                    G1HeapRegionSize=G1HeapRegionSize,
                                                    G1ReservePercent=G1ReservePercent,
                                                    InitiatingHeapOccupancyPercent=InitiatingHeapOccupancyPercent))
                else:
                    G1NewSizePercent = '40'
                    G1MaxNewSizePercent = '50'
                    G1HeapRegionSize = '16M'
                    G1ReservePercent = '15'
                    InitiatingHeapOccupancyPercent = '20'
                    f.write(self.start_flags.format(MEMORY=self.memory, G1NewSizePercent=G1NewSizePercent,
                                                    G1MaxNewSizePercent=G1MaxNewSizePercent,
                                                    G1HeapRegionSize=G1HeapRegionSize,
                                                    G1ReservePercent=G1ReservePercent,
                                                    InitiatingHeapOccupancyPercent=InitiatingHeapOccupancyPercent))
        # start nt(windows)-based generation
        elif self.operating_system == 'nt':
            # TO-DO: write the windows batch gen script
            pass
