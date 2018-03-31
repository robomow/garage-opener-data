
import atexit

import argparse
import cv2
import numpy as np


ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the video file")
ap.add_argument("-d", "--dest",
    help="destination directory")
ap.add_argument("-s", "--skip",
    help="Number of frames to skip")
args = vars(ap.parse_args())

def extractImages(videoFile,destDir,skipCnt):
    vidcap = cv2.VideoCapture(videoFile)
    success,image = vidcap.read()
    cnt = 0
    success = True
    while success:
        success,image = vidcap.read()
        skip = cnt % int(skipCnt)
        if (skipCnt == 0 or skip == 0):
            cv2.imwrite(destDir+"/frame-%d.jpg" % cnt, image)     # save frame as JPEG file
            print("writing frame-"+str(cnt))
        else:
            print("   skipping frame-"+str(cnt))
        cnt += 1

def main():
    videoFile = None
    destDir = None
    skipCnt = 0
    if args.get("video", True):
       videoFile = args["video"]
    if args.get("dest", True):
       destDir = args["dest"]
    if args.get("skip", True):
       skipCnt = args["skip"]
       
    if videoFile != None and destDir != None:
        extractImages(videoFile,destDir,skipCnt)

if __name__ == '__main__':
    main()

