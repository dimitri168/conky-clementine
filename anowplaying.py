#!/usr/bin/env python2
#-*- coding: utf-8 -*-
#
# anowplaying.py
#
#  Connects to dbus and retrieves
#  information about the currently
#  playing track in amarok.
#

import dbus, optparse, shutil

class Nowplaying():
    def __init__(self):
        ''' Connect to dbus and retrieve the amarok dictionary containg
            all the information about the currently playing track 
        '''
        bus = dbus.SessionBus()
        amarok = bus.get_object('org.mpris.clementine', '/Player')
        amarokdict = amarok.GetMetadata()
        cpos=amarok.PositionGet()/1000
        self.artist = self.title = self.album = self.genre = self.year = \
        self.etime = self.ttime = self.rtime = self.progress=\
        self.track = self.bitrate = self.sample = self.cover = ""
        if amarokdict :
            if amarokdict.has_key('artist') :
                self.artist  = amarokdict['artist']
            if amarokdict.has_key('title') : 
                self.title   = amarokdict['title']
            if amarokdict.has_key('album') :
                self.album   = amarokdict['album']
            if amarokdict.has_key('genre') :            
                self.genre   = amarokdict['genre']
            if amarokdict.has_key('year') :            
                self.year    = amarokdict['year']
            if amarokdict.has_key('tracknumber') :
                self.track   = amarokdict['tracknumber']
            if amarokdict.has_key('audio-bitrate') :
                self.bitrate = amarokdict['audio-bitrate']
            if amarokdict.has_key('audio-samplerate') :
                self.sample  = amarokdict['audio-samplerate']
            if amarokdict.has_key('arturl') :
                self.cover   = amarokdict['arturl']
            if amarokdict.has_key('mtime') :
                mt           = amarokdict['mtime']/1000
                self.mtime   = str(mt/60)+":"+str(mt%60) if mt%60>9 else str(mt/60)+":0"+str(mt%60)
                self.etime   = str(cpos/60)+":"+str(cpos%60) if cpos%60>9 else  str(cpos/60)+":0"+str(cpos%60)
                self.rtime   = str((mt-cpos)/60)+":"+str((mt-cpos)%60) if (mt-cpos)%60>9 else str((mt-cpos)/60)+":0"+str((mt-cpos)%60)
                self.progress= float(cpos)/float(mt)*100
 
    def getArtist(self):
        return self.artist.encode('utf-8')
    def getTitle(self):
        return self.title.encode('utf-8')
    def getAlbum(self):
        return self.album.encode('utf-8')
    def getGenre(self):
        return self.genre.encode('utf-8')
    def getYear(self):
        return self.year
    def getTrack(self):
        return self.track
    def getBitrate(self):
        return self.bitrate
    def getSample(self):
        return self.sample
    def getMtime(self):
        return self.mtime
    def getRtime(self):
        return self.rtime
    def getEtime(self):
        return self.etime
    def getProgress(self):
        return self.progress
    def getCover(self, destination):
        ''' Copy amaroks cache cover art to a static location so it can be used in conky'''
        if self.cover != "" :
            try :
                shutil.copyfile(self.cover.replace('file://', ''), destination)
                return ""
            except Exception, e:
                print e
                return ""
        else :
            return ""
if __name__ == '__main__':
    '''Set up the command line parser'''
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-a',  '--artist',  action='store_true', help='artist name')
    parser.add_option('-t',  '--title',   action='store_true', help='title of the track')
    parser.add_option('-l',  '--album',   action='store_true', help='album name')
    parser.add_option('-g',  '--genre',   action='store_true', help='genre of the current track')
    parser.add_option('-y',  '--year',    action='store_true', help='year of the track')
    parser.add_option('-m',  '--mtime',    action='store_true', help='time of the track')
    parser.add_option('-r',  '--rtime',    action='store_true', help='remaining time for the track')
    parser.add_option('-e',  '--etime',    action='store_true', help='elapsed time for the track')
    parser.add_option('-p',  '--progress',    action='store_true', help='progress of the track')
    parser.add_option('-n',  '--track',   action='store_true', help='track number')
    parser.add_option('-b',  '--bitrate', action='store_true', help='bitrate of the track')
    parser.add_option('-s',  '--sample',  action='store_true', help='sample rate of the track')
    parser.add_option('-c',  '--cover',   metavar='filename',  help='copy cover art to destination file')
    
    '''Get the parser options passed to the program'''
    (opts, args) = parser.parse_args()
    now = Nowplaying()
    if opts.artist :
        print now.getArtist()
    if opts.title :
        print now.getTitle()
    if opts.album :
        print now.getAlbum()
    if opts.genre :
        print now.getGenre()
    if opts.year :
        print now.getYear()
    if opts.track :
        print now.getTrack()
    if opts.bitrate :
        print now.getBitrate()
    if opts.sample :
        print now.getSample()
    if opts.etime :
        print now.getEtime()
    if opts.rtime :
        print now.getRtime()
    if opts.mtime :
        print now.getMtime()
    if opts.progress:
        print now.getProgress()
    if opts.cover :
        print now.getCover(opts.cover)
    
