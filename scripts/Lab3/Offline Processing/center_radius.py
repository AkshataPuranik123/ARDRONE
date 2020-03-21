# import the necessary packages
from collections import deque
import numpy as np
import argparse
import cv2
import imutils
import time

import os
import glob

def find_center(filename):
    found=[0,0,0]
    # define the lower and upper boundaries of the "green"
    # ball in the HSV color space, then initialize the
    # list of tracked points
    greenLower = (35,85,25) #45, 50, 15
    greenUpper = (100,245,100) #100, 245, 70

    frame = cv2.imread(filename)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
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
        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
        """
        print(int(x)) 
        print(int(y))
        print(int(radius))
        """
        found=[int(x), int(y), radius]
    
    #cv2.imshow("Frame", frame)
    #key = cv2.waitKey() & 0xFF
    return found

image_directory = '/home/ubuntu16/Desktop/Nudes/edf/images'
files = [f for f in glob.glob(image_directory + "/*.png",)]
sorted_files=sorted(files)
#image_directory = '/home/ubuntu16/Desktop/Nudes/Images'
save_directory = '/home/ubuntu16/Desktop/Nudes/edf/images'
save_file= "values_ball.csv"
save_pathname=save_directory+"/"+save_file
for image_filename in sorted_files:
    if image_filename.endswith(".png"):
        print(image_filename)
        image_pathname=image_directory+"/"+image_filename
        [x,y,radius]=find_center(image_filename)
        #if(radius!=0):
        f= open(save_pathname,"a+")
        f.write(str(x)+","+str(y)+","+str(radius)+"\n")
        f.close()
            

