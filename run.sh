#!/bin/sh
# START
cd /root/P09A/
# SHOW  the SCREEN
screen -list
# STOP  the SCREEN
screen -S   P09A -X quit
# START the SCREEN
screen -dmS P09A /usr/bin/python3 /root/P09A/start.py
# SHOW  the SCREEN
screen -list

# END
