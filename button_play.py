#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
import sys
import time
import RPi.GPIO as GPIO

from mpd import (MPDClient, CommandError)
from socket import error as SocketError

GPIO.cleanup() 

#GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_UP)   #Key 2 is play

#definitions
client = MPDClient()
client.connect('localhost', 6600)

# Poll the playstate and set GPIO.output accordingly

while True:
    try:
        GPIO.setmode(GPIO.BOARD)
        GPIO.wait_for_edge(31, GPIO.FALLING)
        status=client.status()
        if status['state']=='play':
            client.pause()
            print ("\n MPD paused")
        else:
           client.play()
           print ("\n MPD play")


        time.sleep(0.1) # Delay loop for 1 second.
    except KeyboardInterrupt:  
        GPIO.cleanup()       # clean up GPIO on CTRL+C exit

client.disconnect()
GPIO.cleanup()

