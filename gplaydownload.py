import sys
import getopt
import os
import os.path


from gmusicapi import Musicmanager

def usage():
    print "usage: gplaydownload.py [-d|--download-dir=dir]"

def parse_args():
    download_dir = '.'
    try :
        opts, extraparams = getopt.getopt(sys.argv[1:], 'd:h', ['download-dir=', 'help'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ['-h', '--help']:
            usage()
            sys.exit(2)
        elif opt in ['-d', '--download-dir']:
            download_dir = arg
    if not download_dir.endswith('/'):
        download_dir += '/'
    return download_dir

download_dir = parse_args()


print "Creating music manager"
mm = Musicmanager()
print "Attempting login"
if not mm.login():
    print "OAuth required:"
    mm.perform_oauth()
songs = mm.get_all_songs()
for song in songs:
    path = download_dir + song['artist'][0] + '/' + song['artist'] + '/' + song['album']
    path = path.lower().replace(' ', '_')
    track_number = str(song['track_number'])
    if len(track_number) < 2:
        track_number = '0' + track_number
    filename = track_number + ' ' + song['title'] + '.mp3'
    filename = filename.lower().replace(' ', '_')
    full_path = path + '/' + filename
    if not os.path.isfile(full_path): 
        if not os.path.isdir(path):
            print "Creating directory " + path
            os.makedirs(path)
        print "Downloading " + full_path
        suggested_filename, audio = mm.download_song(song['id'])
        with open(full_path, 'wb') as f:
            f.write(audio)


