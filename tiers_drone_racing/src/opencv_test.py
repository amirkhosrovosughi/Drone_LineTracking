#!/usr/bin/env python

import numpy as np
import cv2

print 'read the image'
image_name = "/home/amir/modified_drone_ws/src/drone_racing/tiers_drone_racing/images/tree2.png"
img = cv2.imread(image_name)

cv2.namedWindow("Remote", cv2.WINDOW_NORMAL)


cv2.imshow("Remote",img)


blue, green, red = cv2.split(img)
cv2.namedWindow("BLUE", cv2.WINDOW_NORMAL)
cv2.imshow("BLUE",blue)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.namedWindow("HSV", cv2.WINDOW_NORMAL)
h, s, v = cv2.split(hsv)
hsv_imag = np.concatenate((h,s,v),axis=1)
cv2.imshow("HSV",hsv_imag)


gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.waitKey(0)
