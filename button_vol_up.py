#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
import sys
import time
import RPi.GPIO as GPIO
import alsaaudio


GPIO.setmode(GPIO.BOARD)
GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_UP)   #Key 2 is play

#Wait until key press and increase volume if possible
while True:
    try:
        GPIO.setmode(GPIO.BOARD)
        GPIO.wait_for_edge(35, GPIO.FALLING)

        m = alsaaudio.Mixer('Headphone')
        current_volume = m.getvolume() # Get the current Volume
        nvol=int(current_volume[0]) + 2
        if(nvol<=100):
            m.setvolume(nvol) # Set the new volume
            print("Volume : %d" % nvol)

        time.sleep(0.2) # Debounce
    except KeyboardInterrupt:
        GPIO.cleanup()       # clean up GPIO on CTRL+C exit

client.disconnect()
GPIO.cleanup()

