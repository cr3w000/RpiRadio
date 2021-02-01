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

GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
pwm_b = GPIO.PWM(13, 50)


#definitions
client = MPDClient()
client.connect('localhost', 6600)

#init LED
GPIO.output(15,GPIO.LOW)
GPIO.output(11,GPIO.HIGH)
pwm_b.stop()
time.sleep(1)


#init mpd
#client.add('radioplaylist.m3u')
client.repeat(1)
client.play()

# Poll the playstate and set GPIO.output accordingly

while True:
    status=client.status()
    if status['state']=='play':
        GPIO.output(15,GPIO.HIGH)
        GPIO.output(11,GPIO.LOW) 
        pwm_b.start(0)
    else:
        if status['state']=='pause':
            GPIO.output(15,GPIO.HIGH)
            GPIO.output(11,GPIO.HIGH)
            pwm_b.stop()
        else:
            GPIO.output(15,GPIO.LOW)
            GPIO.output(11,GPIO.HIGH)
            pwm_b.stop()

    for dc in range(0, 101, 5):   # Increase duty cycle: 0~100
        pwm_b.ChangeDutyCycle(dc)     # Change duty cycle
        time.sleep(0.05)

    status=client.status()
    if status['state']=='play':
        GPIO.output(15,GPIO.HIGH)
        GPIO.output(11,GPIO.LOW)
        pwm_b.start(0)
    else:
        GPIO.output(15,GPIO.LOW)
        GPIO.output(11,GPIO.HIGH)
        pwm_b.stop()

    for dc in range(100, -1, -5): # Decrease duty cycle: 100~0
        pwm_b.ChangeDutyCycle(dc)
        time.sleep(0.05)

   # time.sleep(0.1) # Delay loop for 1 second.

client.disconnect()
GPIO.cleanup()

