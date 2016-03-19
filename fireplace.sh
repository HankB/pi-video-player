#!/bin/sh

# script to play videos based on files/semaphores placed in
# /tmp. See the README... Heck from the README:
#
# fireplace.sh
#    reads video name from /tmp/nextVideo and deletes the file
#    If the file does not exist on startup it will loop until it is
#    does not display if /tmp/StopFireplace exists
#    If /tmp/StopFireplace and /tmp/nextVideo does not exist, it will loop the same video
#    if /tmp/nextVideo is found it will start playing the contents.


while(:)        # outer loop, do forever
do
    # wait until 'blocking' file is removed
    while( [ -e /tmp/StopFireplace ] )
    do
        echo "waiting on  /tmp/StopFireplace"
        sleep 3
    done

    while(! [ -e /tmp/nextVideo ] )
    do
        echo "waiting for  /tmp/nextVideo"
        sleep 3
    done
    # fetch video name
    if (! [ -e /tmp/StopFireplace ] )
    then
        VIDEO=`cat  /tmp/nextVideo`
        rm  /tmp/nextVideo
        echo "playing " $VIDEO
        sleep 5
    fi
done
