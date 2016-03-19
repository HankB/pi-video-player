#!/usr/bin/python3

"""
    Debounce and detect long press vs. short press from
    a button connected to a GPIO input. The input is 
    configured with a pullup and the external switch 
    shorts the input to ground.

    User needs membership in group 'gpio' for this to work.
"""
import RPi.GPIO as GPIO
import time
#import operator

#GPIO.setmode(GPIO.BOARD)       # ... in the end there can be only one. ;)
GPIO.setmode(GPIO.BCM)

input=18            # GPIO18 in BCM nomenclature, Pin 12 as Board
debounce = 0.05     # debounce time
longPress = 0.5     # minimum time for long press

GPIO.setup(input, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("pin", input, "is now", GPIO.input(input))

def myFallingCallback(channel):
    """
    Activate when button is pressed and debounce/wait for long press
    """
    startTime = time.time()         # start timing for long press
    print("timing")
    time.sleep(debounce)            # wait to see if it is going to stay low
    if(GPIO.input(channel)==1):     # go high again?
        return
    loopCount = longPress-2*debounce    # how long to wait
    while loopCount > 0:            # loop for 'long press time' or until button is released
        time.sleep(debounce)        # pause a bit
        if(GPIO.input(channel)==1): # button released?
            print ("single press")
            return
        loopCount -= debounce
    while(GPIO.input(channel)==0):  # loop until button released
        time.sleep(debounce)        # pause a bit
    print("long press")
    return


GPIO.add_event_detect(input, GPIO.FALLING)
GPIO.add_event_callback(input, myFallingCallback)

try:
    while(1):
        time.sleep(5)
        #print("still sleeping", int(time.monotonic()))
except (KeyboardInterrupt, SystemExit):
    print("GPIO cleanup")
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  

