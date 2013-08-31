conkyconfig
===========

 simple python script to fetch current playing track information from clementine ,can be easily
 modified to cater any player with a dbus interface

 +artist
 +album
 +cover
 +progress
###Included Files

anowplaying.py (fetch currently playing track in amarok via dbus)
conkyrc(simple conky rc with clementine now playing and usual stuff)

TODO:   currently multiple requests are fired which may cause a high cpu usage soometimes if you are on an older processor.
        Improve perfomance by limiting the number of requests. 

