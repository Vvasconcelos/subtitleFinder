import os
import json
import sys
import urllib2
import gzip
import StringIO
import time
from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File
from os import path


def main():
    pathList = []
    downloadList = []
    if len(sys.argv) < 1 :
        print "Missing Arguments"
        quit()

    folder = sys.argv[1]
    print sys.argv[1]
    #folder = "C:\\Users\\viiva\\Downloads\\Torrent\\The.Walking.Dead.S06E10.PROPER.HDTV.x264-KILLERS[ettv]"
    for root, dirs, files in os.walk(folder):
        path = root.split('/')
        for file in files:
            if(file.endswith(".mp4") or file.endswith(".avi") or file.endswith(".mkv") ):
                pathList.append(os.path.join(path[0],file))

    print "Found %d files" % len(pathList)

    if len(pathList) >= 1:
        ops = OpenSubtitles()

        token = ops.login("","")

        for subToFind in pathList:
            f = File(subToFind)
            dirname = os.path.normpath(subToFind)
            #print dirname

            subData = ops.search_subtitles([{'sublanguageid': 'pob','moviehash': f.get_hash() , 'moviebytesize': f.size }])

            if not subData:
                print "Sub not found for %s " % f.path
            else:
                filename = ''
                if f.path.endswith(".mp4"):
                    filename = dirname.replace('.mp4', '.srt')
                elif f.path.endswith('.mkv'):
                    filename = dirname.replace('.mkv', '.srt')
                elif f.path.endswith('.avi'):
                    filename = dirname.replace('.avi', '.srt')


                response = urllib2.urlopen(subData[0]['SubDownloadLink'])
                compressedFile = StringIO.StringIO()
                compressedFile.write(response.read())
                response.close()
                compressedFile.seek(0)
                decompressedFile = gzip.GzipFile(fileobj=compressedFile,mode='rb')

                with open(filename ,'w') as outfile:
                    outfile.write(decompressedFile.read())

                time.sleep(1)

        ops.logout()

if __name__ == '__main__':
    main()






'''

f =  File(path.join("C:\\Users\\viiva\\Downloads\\Limitless.S01E15.HDTV.x264-LOL[ettv]","limitless.115.hdtv-lol[ettv].mp4"))

data =

if not data:
    print "Not found any sub for: %s" % f.path()
'''
