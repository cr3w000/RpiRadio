#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
import sys
import time
import RPi.GPIO as GPIO

import pydbus

from mpd import (MPDClient, CommandError)
from socket import error as SocketError

GPIO.cleanup() 

#GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(33, GPIO.IN, pull_up_down=GPIO.PUD_UP)   #Key 1 is play

#definitions
client = MPDClient()
client.connect('localhost', 6600)
wait_for_stop = 0  #stop after some time when paused, streams cannot be paused too long

#init bluetooth control
bus_name = 'org.bluez'
sys_bus = pydbus.SystemBus()

dongle = sys_bus.get(bus_name, '/org/bluez/hci0')

print(dongle.Alias, dongle.Name)
print(dongle.Powered)


# Poll the playstate and set GPIO.output accordingly

while True:
    try:
        GPIO.setmode(GPIO.BOARD)
        channel = GPIO.wait_for_edge(33,GPIO.FALLING, timeout=5000)
        status=client.status()   #ask for status each 5s to not lose connection to mpd

        if channel is None:
            print('Timeout occurred')
            if status['state']=='pause':
                wait_for_stop = wait_for_stop + 1
                if(wait_for_stop > 4):    #wait approx 20s then stop.
                    client.stop()
                    dongle.Powered = True
            else:
                wait_for_stop = 0
        else:
            print('Edge detected on channel', channel)
            if status['state']=='play':
                client.pause()
                print ("\n MPD paused")
                dongle.Powered = True
                print ("Bluetooth ON")
            else:
                client.play()
                print ("\n MPD play")
                dongle.Powered = False
                print ("Bluetooth OFF")


        time.sleep(0.2) # Delay loop for 1 second.
    except KeyboardInterrupt:
        GPIO.cleanup()       # clean up GPIO on CTRL+C exit

client.disconnect()
GPIO.cleanup()

