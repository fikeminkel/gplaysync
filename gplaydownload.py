import sys
import getopt
import os
import os.path
import time
import requests

from gmusicapi import Musicmanager

def usage():
    print "usage: gplaydownload.py [-d|--download-dir=dir]"

def parse_args():
    download_dir = '.'
    notify_plex = False
    try :
        opts, extraparams = getopt.getopt(sys.argv[1:], 'nd:h', ['notify-plex', 'download-dir=', 'help'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ['-h', '--help']:
            usage()
            sys.exit(2)
        elif opt in ['-d', '--download-dir']:
            download_dir = arg
        elif opt in ['-n', '--notify-plex']:
            notify_plex = True
    if not download_dir.endswith('/'):
        download_dir += '/'
    return download_dir, notify_plex

def log(msg): 
    print time.asctime(time.localtime(time.time())) + ": " + msg

def get_songs():
    log("Checking for updates")
    songs = mm.get_all_songs()
    downloaded_songs = False
    for song in songs:
        path = song['artist'][0] + '/' + song['artist'] + '/' + song['album']
        path = path.lower().replace(' ', '_')
        path = download_dir + path
        track_number = str(song['track_number'])
        if len(track_number) < 2:
            track_number = '0' + track_number
        filename = track_number + ' ' + song['title'] + '.mp3'
        filename = filename.lower().replace(' ', '_')
        full_path = path + '/' + filename
        if not os.path.isfile(full_path): 
            if not os.path.isdir(path):
                log("Creating directory " + path)
                os.makedirs(path)
            log("Downloading " + full_path)
            suggested_filename, audio = mm.download_song(song['id'])
            with open(full_path, 'wb') as f:
                f.write(audio)
            downloaded_songs = True
    if downloaded_songs and notify_plex:
        log("Notifying local Plex Media Server to refresh")
        r = requests.get('http://localhost:32400/library/sections/3/refresh?force=1')
        r.raise_for_status()

def run():
    global download_dir, notify_plex, mm
    download_dir, notify_plex = parse_args()
    log("Creating music manager")
    mm = Musicmanager()
    log("Attempting login")
    if not mm.login():
        print "OAuth required:"
        mm.perform_oauth()

    get_songs()

if __name__ == "__main__": 
    run()

