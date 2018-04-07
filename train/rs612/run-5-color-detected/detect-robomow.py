#python color_tracking.py

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import urllib #for reading image from URL


rm_cascade = cv2.CascadeClassifier('model/cascade.xml')


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())
 
# define the lower and upper boundaries of the colors in the HSV color space
#lower = {'red':(166, 84, 141), 'green':(66, 122, 129), 'blue':(97, 100, 117), 'yellow':(23, 59, 119), 'orange':(0, 50, 80)} 
lower = {'red':(0, 0, 30),'green':(0,0,47),'blue':(0,0,37)} 
#assign new item lower['blue'] = (93, 10, 0)
#upper = {'red':(186,255,255), 'green':(86,255,255), 'blue':(117,255,255), 'yellow':(54,255,255), 'orange':(20,255,255)}
upper = {'red':(255,97,66),'green':(156,141,126),'blue':(255,255,27)}

# define standard colors for circle around the object
colors = {'red':(0,0,255), 'green':(0,255,0), 'blue':(255,0,0), 'yellow':(0, 255, 217), 'orange':(0,140,255)}

def drawDriveway(frame):
    # bottom line
    cv2.line(frame,(00,500),(70,470),(0,255,0),2)
    cv2.line(frame,(70,470),(70,600),(0,255,0),2)

    # top upper line
    cv2.line(frame,(0,250),(250,200),(0,255,0),2)

    # top connect line
    cv2.line(frame,(250,200),(400,300),(0,255,0),2)

    # right outer line
    cv2.line(frame,(400,300),(550,500),(0,255,0),2)

    # right outer line
    cv2.line(frame,(550,500),(550,600),(0,255,0),2)

    # Message
    posStr = "Time to"
    cv2.putText(frame,posStr, (200,325), cv2.FONT_HERSHEY_SIMPLEX, 0.6,colors['blue'],2)
    posStr = "Open Garage Door"
    cv2.putText(frame,posStr, (150,350), cv2.FONT_HERSHEY_SIMPLEX, 0.6,colors['blue'],2)
    print("Drawing Driveway")

pts = deque(maxlen=args["buffer"])
 
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(0)
else:
    camera = cv2.VideoCapture(args["video"])
frame_width=800
frame_height=600
#out = cv2.VideoWriter('detect-robomow.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

# keep looping
imgFound = 0
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        break

    #IP webcam image stream 
    #URL = 'http://10.254.254.102:8080/shot.jpg'
    #urllib.urlretrieve(URL, 'shot1.jpg')
#    frame = cv2.imread('pos-800x600/frame2552.jpg')


    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=800)

    drawDriveway(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    watches = rm_cascade.detectMultiScale(gray,minNeighbors=10,minSize=(100,100),maxSize=(150,150))
    i = 1
    for (x,y,w,h) in watches:
        if i == 1:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)
            posStr = "i=" + str(i)
            cv2.putText(frame,posStr, (int(x),int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,colors['blue'],2)
        i=i+1
		
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    #out.write(frame)
    
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
 
# cleanup the camera and close any open windows
#out.release()
camera.release()
cv2.destroyAllWindows()
