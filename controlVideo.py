#!/usr/bin/python3

"""
    Debounce and detect long press vs. short press from
    a button connected to a GPIO input. The input is 
    configured with a pullup and the external switch 
    shorts the input to ground.

    User needs membership in group 'gpio' for this to work.

    Now adding actions for the buttons. The point is to cycle
    through the videos in ~/Videos. See the README in this
    directory to see the protocol between this and the shell
    script that actually plays the videos.
"""
import RPi.GPIO as GPIO
import time
import os
import sys
import psutil

# find video names
videoFiles = os.listdir("/home/hbarta/Videos")
videoFiles = sorted(videoFiles)
print(videoFiles)
for i in range(0, len(videoFiles)):
    print(i, "/home/hbarta/Videos/"+videoFiles[i])
#sys.exit()


#GPIO.setmode(GPIO.BOARD)       # ... in the end there can be only one. ;)
GPIO.setmode(GPIO.BCM)

input=18            # GPIO18 in BCM nomenclature, Pin 12 as Board
debounce = 0.05     # debounce time
longPress = 0.5     # minimum time for long press

GPIO.setup(input, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def killProcess(procname):
    """
    Find the proggy and kill it
    """
    for proc in psutil.process_iter():
        if proc.name() == procname:
            print("killing", proc.name())
            proc.kill()

def pause():
    """
    Write the file that causes the shell script to pause
    and kill oxplayer
    """
    open( "/tmp/StopFireplace", 'a').close()
    killProcess("omxplayer.bin")
        
def unPause():
    """
    Remove the file that causes the shell script to pause
    """
    os.remove("/tmp/StopFireplace")

def play(video):
    """
    Write the video to play to /tmp/nextVideo and kill omxplayer so it
    goes to the next video
    """
    fname = "/tmp/nextVideo"
    tmpName = fname + ".tmp"
    f = open(tmpName, 'w')
    f.truncate()
    f.write(video)
    f.close()
    os.rename(tmpName, fname)
    killProcess("omxplayer.bin")

def myFallingCallback(channel):
    """
    Activate when button is pressed and debounce/wait for long press
    """
    startTime = time.time()         # start timing for long press
    time.sleep(debounce)            # wait to see if it is going to stay low
    if(GPIO.input(channel)==1):     # go high again?
        return
    loopCount = longPress-2*debounce    # how long to wait
    while loopCount > 0:            # loop for 'long press time' or until button is released
        time.sleep(debounce)        # pause a bit
        if(GPIO.input(channel)==1): # button released?
            print("play"+"/home/hbarta/Videos/"+videoFiles[myFallingCallback.nextVideo])
            play("/home/hbarta/Videos/"+videoFiles[myFallingCallback.nextVideo])
            unPause()
            killProcess("omxplayer.bin")
            myFallingCallback.nextVideo += 1
            if myFallingCallback.nextVideo >= len(videoFiles):
                myFallingCallback.nextVideo =0
            return
        loopCount -= debounce
    while(GPIO.input(channel)==0):  # loop until button released
        time.sleep(debounce)        # pause a bit
    print("pause video")
    pause()
    return

# initialze our loop index and start the first video
myFallingCallback.nextVideo=0
play("/home/hbarta/Videos/"+videoFiles[myFallingCallback.nextVideo])
myFallingCallback.nextVideo=1

GPIO.add_event_detect(input, GPIO.FALLING)
GPIO.add_event_callback(input, myFallingCallback)

try:
    while(1):
        time.sleep(5)
        #print("still sleeping", int(time.monotonic()))
except (KeyboardInterrupt, SystemExit):
    print("GPIO cleanup")
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  

