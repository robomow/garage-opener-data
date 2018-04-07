# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import urllib #for reading image from URL


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())
 
# define standard colors for rectangle around the object
colors = {'red':(0,0,255), 'green':(0,255,0), 'blue':(255,0,0), 'yellow':(0, 255, 217), 'orange':(0,140,255)}

pts = deque(maxlen=args["buffer"])
 
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(0)
# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])

# keep looping
imgFound = 0
posInfoFile = open("pos-info.txt","w") 
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        break
 
    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    #for each color in dictionary check object in frame
    for key, value in upper.items():
        # construct a mask for the color from dictionary`1, then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        kernel = np.ones((9,9),np.uint8)
        mask = cv2.inRange(hsv, lower[key], upper[key])
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        #mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
                
        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)

            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        
            # only proceed if the radius meets a minimum size. Correct this value for your obect's size
            if radius > 14 and len(cnts) <= 2:
                x,y,w,h = cv2.boundingRect(c)
                #cv2.drawContours(frame, c, -1, (0,255,0), 3)
                imgFound=imgFound+1
                print("found=",imgFound," cnts=",len(cnts)," x=",int(round(x)),"y=",int(round(y))," radius=",radius);

                # Lets increase the size of the box
                x=x-90
                y=y-60
                w=w+120
                h=h+90
                robomow = frame[y:y+h,x:x+w]
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                #cv2.rectangle(frame,(x, y), (x+w,y+h), colors[key], 2)
                #cv2.rectangle(frame, (int(x)-90, int(y)-60), (int(x)+90,int(y)+60), colors[key], 2)
                #cv2.circle(frame, (int(x), int(y)), int(radius), colors[key], 2)
                #cv2.putText(frame,key + " ball", (int(x-radius),int(y-radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,colors[key],2)
                #cv2.imwrite("pos-robomow/rw-%d.jpg" % imgFound, robomow) 

                # prepare the coordinates and size string for the file
                infoStr = "rw-"+str(imgFound)+".jpg 1 "+str(x)+" "+str(y)+" "+str((x+w))+" "+str((y+h))+"\n"

                # lets write it to the file
                posInfoFile.write(infoStr)
                
            #else:
                #print("invalid radius=",radius)

        else:
           print("no contour found") 
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
