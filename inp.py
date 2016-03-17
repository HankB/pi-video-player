#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import operator

#GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)
input=18
debounce = 0.10     # debonce time
longPress = 1.0     # minimum time for long press
doublePress = 0.35  # maximum time between presses for double press

GPIO.setup(input, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("pin", input, "is", GPIO.input(input))
startTime = 0

def myFallingCallback(channel):
    print("timing")
    time.sleep(debounce)             # wait to see if it is going to stay low
    if(GPIO.input(channel)==1): # go high again?
        return
    loopCount = longPress-2*debounce
    while loopCount > 0:         # loop to see how long user holds button
        time.sleep(debounce)             # time short press
        if(GPIO.input(channel)==1): # button released?
            if(time.time()-startTime < doublePress):
                print("double pres")
                #startTime = time.time()
                return
            print ("single press")
            startTime = time.time()
            return
        loopCount -= debounce
    while(GPIO.input(channel)==0):  # button still pressed?
        time.sleep(debounce)             # wait to see if it is going to stay low
    print("long press")
    return


GPIO.add_event_detect(input, GPIO.FALLING)
GPIO.add_event_callback(input, myFallingCallback)

while(1):
    time.sleep(5)
    #print("still sleeping", int(time.monotonic()))

