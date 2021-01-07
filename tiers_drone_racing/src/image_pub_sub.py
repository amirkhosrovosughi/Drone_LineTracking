#!/usr/bin/env python

import numpy as np
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import sys
import math
from std_msgs.msg import Int16MultiArray

bridge = CvBridge()
pub = rospy.Publisher('/Processed_imag/rgb_image', Image, queue_size=1)
edited_imag = np.zeros((2, 2, 2))
pub2 = rospy.Publisher('/Processed_imag/center', Int16MultiArray, queue_size=1)
center_coordinate = Int16MultiArray()
center_coordinate.data = []

def process_contours(binary_image, rgb_image, contours):
    black_image = np.zeros([binary_image.shape[0], binary_image.shape[1],3],'uint8')
    (rows,cols,channels) = rgb_image.shape

    for c in contours:
        global center_coordinate
        area = cv2.contourArea(c)
        perimeter= cv2.arcLength(c, True)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        cv2.drawContours(rgb_image, [c], -1, (150,250,150), 1)
        cv2.drawContours(black_image, [c], -1, (150,250,150), 1)
        cx, cy = get_contour_center(c)
        cv2.circle(rgb_image, (cx,cy),(int)(radius),(0,0,255),1)
        cv2.circle(black_image, (cx,cy),(int)(radius),(0,0,255),1)
        cv2.circle(black_image, (cx,cy), radius=0, color=(0, 150, 155), thickness=5)
        cv2.circle(rgb_image, (cx,cy), radius=0, color=(0, 150, 155), thickness=5)
        x_coordinate = math.floor(cx - cols/2)
        y_coordinate = math.floor(cy - rows/2)
        print ("Center is in {} and {}".format(x_coordinate, y_coordinate))
        center_coordinate.data = [x_coordinate, y_coordinate]
        #center_coordinate.data = [cx, cy]
        pub2.publish(center_coordinate)
        #print ("Area: {}, Perimeter: {}".format(area, perimeter))
    #print ("number of contours: {}".format(len(contours)))
    cv2.imshow("RGB Image Contours",rgb_image)
    cv2.imshow("Black Image Contours",black_image)
    return rgb_image, black_image

def get_contour_center(contour):
    M = cv2.moments(contour)
    cx=-1
    cy=-1
    if (M['m00']!=0):
        cx= int(M['m10']/M['m00'])
        cy= int(M['m01']/M['m00'])
    return cx, cy

def getContours(binary_image):
    _ ,contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def draw_contours(image, contours, image_name):
    index = -1 #means all contours
    thickness = 2 #thinkess of the contour line
    color = (255, 0, 255) #color of the contour line
    cv2.drawContours(image, contours, index, color, thickness)
    cv2.imshow(image_name,image)



def find_circle(cv_imag,lower_band,upper_band):
    # convert to hsv
    hsv = cv2.cvtColor(cv_imag, cv2.COLOR_BGR2HSV)
    #cv2.imshow("hsv image",hsv)
    # masking
    mask = cv2.inRange(hsv, lower_band, upper_band)
    #cv2.imshow("mask image", mask);
    # countor
    contours = getContours(mask)
    #draw_contours(cv_imag, contours,"RGB Contours")
    rgb_image, black_image = process_contours(mask, cv_imag, contours)
    return rgb_image





def image_callback(ros_image):
  print 'got an image'
  global bridge
  global edited_imag
  #convert ros_image into an opencv-compatible image
  try:
    cv_image = bridge.imgmsg_to_cv2(ros_image, "bgr8")
  except CvBridgeError as e:
      print(e)
  #from now on, you can work exactly like with opencv
  #(rows,cols,channels) = cv_image.shape
  #if cols > 200 and rows > 200 :
  #  cv2.circle(cv_image, (100,100),90, 255)
  #font = cv2.FONT_HERSHEY_SIMPLEX
  #cv2.putText(cv_image,'Webcam Activated with ROS & OpenCV!',(10,350), font, 1,(255,255,255),2,cv2.LINE_AA)
  cv2.imshow("Carema view", cv_image)
  cv2.waitKey(3)
  # Added by Amir
  #finding circle
  lower_band =(60, 150, 100)
  upper_band = (90, 255, 255)
  processed_imag=find_circle(cv_image,lower_band,upper_band)
  # Publishing as a topic ==> find out best practice for publishing
  edited_imag = bridge.cv2_to_imgmsg(processed_imag, encoding="bgr8")
  #pub = rospy.Publisher('edited_imag/imag_with_text', Image, queue_size=1)
  pub.publish(edited_imag)
  #return ros_image


def main(args):
  rospy.init_node('camera_processing', anonymous=True)
  #for turtlebot3 waffle
  #image_topic="/camera/rgb/image_raw/compressed"
  #for usb cam
  #image_topic="/usb_cam/image_raw"
  sub_imag = rospy.Subscriber("/downward_cam/camera/image",Image, image_callback)
  # Addded by Amir
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
