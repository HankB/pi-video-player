#!/bin/sh

# script to play videos based on files/semaphores placed in
# /tmp. See the README... Heck from the README:
#
# fireplace.sh
#    Reads video name from /tmp/nextVideo and then deletes the file.
#    If the file does not exist on startup it will loop until it is.
#    It does not play the video if /tmp/StopFireplace exists.
#    If both /tmp/StopFireplace and /tmp/nextVideo do not exist, 
#    it will loop the same video (if a video name has already been
#    read in.)


while(:)        # outer loop, do forever
do

    while [ -e /tmp/StopFireplace ]       # wait until 'blocking' file is removed
    do
        echo "waiting on /tmp/StopFireplace"
        sleep 3
    done

    if [ -z ${VIDEO+x} ]                    # if there is no video name yet
    then
        while ! [ -e /tmp/nextVideo ]       # wait for the video file
        do
            echo "waiting for /tmp/nextVideo"
            sleep 3
        done
    fi

    if [ -e /tmp/nextVideo ]                # fetch video name if file exists
    then
        VIDEO=`cat  /tmp/nextVideo`
        rm  /tmp/nextVideo
    fi

    echo "playing " $VIDEO
    omxplayer "$VIDEO" >/dev/null 2>&1
done
