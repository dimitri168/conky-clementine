#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#
# anowplaying.py
#
#  Connects to dbus and retrieves
#  information about the currently
#  playing track in clementine.
#

import dbus, optparse, shutil, subprocess

if __name__ == '__main__':
    '''Check if clementine is running'''
    output = subprocess.getoutput('ps -A')
    if 'clementine' not in output:
        raise SystemExit

    '''Get system bus'''
    bus = dbus.SessionBus()
    player = bus.get_object('org.mpris.MediaPlayer2.clementine', '/org/mpris/MediaPlayer2')
    playerdict = player.Get('org.mpris.MediaPlayer2.Player', 'Metadata', dbus_interface='org.freedesktop.DBus.Properties')
    trackposition = player.Get('org.mpris.MediaPlayer2.Player', 'Position', dbus_interface='org.freedesktop.DBus.Properties')

    '''Set up the command line parser'''
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-a',  '--artist',  action='store_true', help='artist name')
    parser.add_option('-t',  '--title',   action='store_true', help='title of the track')
    parser.add_option('-l',  '--album',   action='store_true', help='album name')
    parser.add_option('-g',  '--genre',   action='store_true', help='genre of the current track')
    parser.add_option('-y',  '--year',    action='store_true', help='year of the track')
    parser.add_option('-m',  '--length',    action='store_true', help='time of the track')
    parser.add_option('-r',  '--rtime',    action='store_true', help='remaining time for the track')
    parser.add_option('-e',  '--etime',    action='store_true', help='elapsed time for the track')
    parser.add_option('-p',  '--position',    action='store_true', help='progress of the track')
    parser.add_option('-n',  '--trackNumber',   action='store_true', help='track number')
    parser.add_option('-b',  '--bitrate', action='store_true', help='bitrate of the track')
    parser.add_option('-s',  '--sample',  action='store_true', help='sample rate of the track')
    parser.add_option('-c',  '--cover',   metavar='filename',  help='copy cover art to destination file')
    
    '''Get the parser options printed'''
    (opts, args) = parser.parse_args()
    if opts.artist and 'xesam:artist' in playerdict:
        print(playerdict['xesam:artist'][0])
    if opts.title and 'xesam:title' in playerdict:
        print(playerdict['xesam:title'])
    if opts.album and 'xesam:album' in playerdict:
        print(playerdict['xesam:album'])
    if opts.genre and 'xesam:genre' in playerdict:
        print(playerdict['xesam:genre'][0])
    if opts.year and 'year' in playerdict:
        print(playerdict['year'])
    if opts.trackNumber and 'xesam:trackNumber' in playerdict:
        print(playerdict['trackNumber'])
    if opts.bitrate and 'bitrate' in playerdict:
        print(playerdict['bitrate'])
    if opts.length and 'mpris:length' in playerdict:
        print(playerdict['mpris:length'])
    if opts.position:
        print(trackposition)
    if opts.etime:
        pos = trackposition / playerdict['mpris:length'] * 100
        print(pos)
        
    if opts.cover:
        if 'mpris:artUrl' in playerdict:
            cover = playerdict['mpris:artUrl']
            try:
                shutil.copyfile(cover.replace('file://', ''), opts.cover)
            except KeyError:
                print()
        else:
            shutil.copyfile('/usr/share/icons/Adwaita/512x512/emblems/emblem-unreadable.png', opts.cover)
