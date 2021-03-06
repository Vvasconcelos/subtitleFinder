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
    #if len(sys.argv) < 1 :
    #    print "Missing Arguments"
    #    quit()

    folder = "/home/Downloads/torrents"
    #print sys.argv[1]
    for root, dirs, files in os.walk(folder):
        path = root.split('/')
        #print root
        for file in files:
            if(file.endswith(".mp4") or file.endswith(".avi") or file.endswith(".mkv") ):
                print os.path.join(root,file)
                pathList.append(os.path.join(root,file))

    print "Found %d files" % len(pathList)

    if len(pathList) >= 1:
        ops = OpenSubtitles()

        token = ops.login("","")
        print token
        for subToFind in pathList:
            f =  File(subToFind)
            dirname = os.path.normpath(subToFind)

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
