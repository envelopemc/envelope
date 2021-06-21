"""
This class is for generating the proper batch file used to start the server in ./paper_server.

Class will read config for OS
"""

import Orange0
import os


class BatchGen:
    def __init__(self):
        config = Orange0.read_config()
        operating_system = os.name
        self.memory = config[3]
        self.operating_system = operating_system
        print(operating_system)
        self.start_flags = 'java -Xms{MEMORY}G -Xmx{MEMORY}G ' \
                           '-XX:+UseG1GC-XX:+ParallelRefProcEnabled-XX:MaxGCPauseMillis=200-XX' \
                           ':+UnlockExperimentalVMOptions-XX:+DisableExplicitGC-XX:+AlwaysPreTouch-XX' \
                           ':G1HeapWastePercent=5-XX:G1MixedGCCountTarget=4-XX:G1MixedGCLiveThresholdPercent=90-XX' \
                           ':G1RSetUpdatingPauseTimePercent=5-XX:SurvivorRatio=32-XX:+PerfDisableSharedMem-XX' \
                           ':MaxTenuringThreshold=1-XX:G1NewSizePercent=30-XX:G1MaxNewSizePercent=40-XX' \
                           ':G1HeapRegionSize=8M-XX:G1ReservePercent=20-XX:InitiatingHeapOccupancyPercent=15-Dusing' \
                           '.aikars.flags=https://mcflags.emc.gs-Daikars.new.flags=true -jar paper.jar nogui'

    def batch_gen(self):
        if self.operating_system == 'posix':
            with open('start.sh', 'w') as f:
                f.write(self.start_flags.format(MEMORY=self.memory))
