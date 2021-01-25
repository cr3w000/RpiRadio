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

GPIO.setup(33, GPIO.IN, pull_up_down=GPIO.PUD_UP)   #Key 2 is play

#definitions
client = MPDClient()
client.connect('localhost', 6600)

# Poll the playstate and set GPIO.output accordingly

while True:
    try:
        GPIO.setmode(GPIO.BOARD)
        channel = GPIO.wait_for_edge(33,GPIO.FALLING, timeout=5000)
        status=client.status()   #ask for status each 5s to not lose connection to mpd

        if channel is None:
            print('Timeout occurred')
        else:
            print('Edge detected on channel', channel)
            if status['state']=='play':
                client.next()
                print ("\n MPD paused")


        time.sleep(0.2) # Delay loop for 1 second.
    except KeyboardInterrupt:  
        GPIO.cleanup()       # clean up GPIO on CTRL+C exit

client.disconnect()
GPIO.cleanup()

