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
pub3 = rospy.Publisher('/Processed_imag/line_edge', Int16MultiArray, queue_size=1)

pub4 = rospy.Publisher('/Processed_imag/mask_circle', Image, queue_size=1)
pub5 = rospy.Publisher('/Processed_imag/mask_line', Image, queue_size=1)



center_coordinate = Int16MultiArray()
center_coordinate.data = []
edge_coordinate = Int16MultiArray()
edge_coordinate.data = []





def process_contours(binary_image, cv_imag1, contours, type):
    global center_coordinate
    global edge_coordinate

    rgb_image = cv_imag1
    black_image = np.zeros([binary_image.shape[0], binary_image.shape[1],3],'uint8')
    (rows,cols,channels) = rgb_image.shape

    edge_coordinates_list = []

    for c in contours:

        area = cv2.contourArea(c)
        if area > 20:
            if type == "circle":
                perimeter= cv2.arcLength(c, True)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                cv2.drawContours(rgb_image, [c], -1, (226,198,85), 2)
                cv2.drawContours(black_image, [c], -1, (226,198,85), 2)
                cx, cy = get_contour_center(c)
                cv2.circle(rgb_image, (cx,cy),(int)(radius),(255,97,97),1)
                cv2.circle(black_image, (cx,cy),(int)(radius),(255,97,97),1)
                cv2.circle(black_image, (cx,cy), radius=0, color=(255,97, 97), thickness=5)
                cv2.circle(rgb_image, (cx,cy), radius=0, color=(255,97, 97), thickness=5)
                x_coordinate = math.floor(cx - cols/2)
                y_coordinate = math.floor(cy - rows/2)
                #print ("Center is in {} and {}".format(x_coordinate, y_coordinate))
                center_coordinate.data = [x_coordinate, y_coordinate]
                #center_coordinate.data = [cx, cy]
                pub2.publish(center_coordinate)
                #cv2.imshow("RGB Image Contours - Circle",rgb_image)
                #cv2.imshow("Black Image Contours - Circle",black_image)
            elif type == "line":
                perimeter= cv2.arcLength(c, True)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                cv2.drawContours(rgb_image, [c], -1, (150,250,150), 2)
                cv2.drawContours(black_image, [c], -1, (150,250,150), 2)
                #cx, cy = get_contour_center(c)
                #cv2.circle(rgb_image, (cx,cy),(int)(radius),(0,0,255),1)
                #cv2.circle(black_image, (cx,cy),(int)(radius),(0,0,255),1)
                #cv2.circle(black_image, (cx,cy), radius=0, color=(0, 150, 155), thickness=5)
                #cv2.circle(rgb_image, (cx,cy), radius=0, color=(0, 150, 155), thickness=5)
                #x_coordinate = math.floor(cx - cols/2)
                #y_coordinate = math.floor(cy - rows/2)
                #print ("Center is in {} and {}".format(x_coordinate, y_coordinate))
                #center_coordinate.data = [x_coordinate, y_coordinate]
                #center_coordinate.data = [cx, cy]
                #pub2.publish(center_coordinate)
                #cv2.imshow("RGB Image Contours - Line",rgb_image)
                #cv2.imshow("Black Image Contours - Line",black_image)
            elif type == "line_edge":
                perimeter= cv2.arcLength(c, True)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                #cv2.drawContours(rgb_image, [c], -1, (226,198,85), 1)
                #cv2.drawContours(black_image, [c], -1, (226,198,85), 1)
                cx, cy = get_contour_center(c)
                cv2.circle(rgb_image, (cx,cy),(int)(radius),(10,10,10),1)
                cv2.circle(black_image, (cx,cy),(int)(radius),(10,10,10),1)
                cv2.circle(black_image, (cx,cy), radius=0, color=(255,255, 255), thickness=5)
                cv2.circle(rgb_image, (cx,cy), radius=0, color=(255,255, 255), thickness=5)
                x_coordinate = math.floor(cx - cols/2)
                y_coordinate = math.floor(cy - rows/2)
                #print ("Line Edge is in {} and {}".format(x_coordinate, y_coordinate))
                Edges_Coor = [x_coordinate, y_coordinate]
                edge_coordinates_list.append(Edges_Coor)
                #cv2.imshow("RGB Image Contours - line edge",rgb_image)
            else:
                print('Undefined object code!')


    if type == "line_edge":
        flat_list = [item for sublist in edge_coordinates_list for item in sublist]
        edge_coordinate.data = flat_list
        pub3.publish(edge_coordinate)

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

def Fill_the_center(mask,width):
    (rows,cols) = mask.shape
    #print ("Center is in {} , {} ".format(rows,cols))
    img2	=	cv2.rectangle(mask, (width,width), (cols-width, rows- width), (0,0,0), -1)
    return img2


def find_circle(cv_imag,lower_band,upper_band):
    # convert to hsv
    hsv = cv2.cvtColor(cv_imag, cv2.COLOR_BGR2HSV)
    #cv2.imshow("hsv image",hsv)
    # masking
    mask = cv2.inRange(hsv, lower_band, upper_band)
    #mask_ros = bridge.cv2_to_imgmsg(mask, encoding="bgr8")
    mask_ros = bridge.cv2_to_imgmsg(mask, encoding="mono8")
    pub4.publish(mask_ros)
    #cv2.imshow("mask image", mask);
    # countor
    contours = getContours(mask)
    #draw_contours(cv_imag, contours,"RGB Contours")
    #cv_imag0 = cv_imag
    #cv2.imshow("CV image 1",cv_imag)
    rgb_image, black_image = process_contours(mask, cv_imag, contours,type="circle")

    #cv2.imshow("CV image 2",cv_imag)#===> something wired happening here, abouve functino change the content cv_imag although does not recieve it
    return rgb_image


def find_line(cv_imag,processed_imag,lower_band,upper_band,type="line"):
    # convert to hsv
    hsv = cv2.cvtColor(cv_imag, cv2.COLOR_BGR2HSV)
    #cv2.imshow("CV image 2",cv_imag)
    # masking
    mask = cv2.inRange(hsv, lower_band, upper_band)
    mask_ros = bridge.cv2_to_imgmsg(mask, encoding="mono8")
    pub5.publish(mask_ros)

    mask2 = cv2.inRange(hsv, lower_band, upper_band)
    mask2 = Fill_the_center(mask2,width=25)
    #cv2.imshow("mask original after feeling",mask)
    # countor
    contours = getContours(mask)
    contours2 = getContours(mask2)
    #draw_contours(cv_imag, contours,"RGB Contours")
    rgb_image, black_image = process_contours(mask, processed_imag, contours,type="line")
    rgb_image, black_image = process_contours(mask2, rgb_image, contours2,type="line_edge")
    return rgb_image


def image_callback(ros_image):
  #print 'got an image'
  global bridge
  global edited_imag
  #convert ros_image into an opencv-compatible image
  try:
    cv_image = bridge.imgmsg_to_cv2(ros_image, "bgr8")
    cv_image2 = bridge.imgmsg_to_cv2(ros_image, "bgr8") #==> Add it becuase the orginal picture change when it pass to a function
    cv_image3 = bridge.imgmsg_to_cv2(ros_image, "bgr8") #==> cv_image, cv_image2, cv_image3 are same copies
  except CvBridgeError as e:
      print(e)
  #show the image
  cv2.imshow("Raw Camera", cv_image)
  cv2.waitKey(3)
  # Dectecting the objects in the world
  #finding circle
  lower_band =(60, 150, 100)
  upper_band = (90, 255, 255)
  processed_imag=find_circle(cv_image,lower_band,upper_band)
  # the center of circle, is published inside the above function
  # finding the line
  lower_band =(0, 80, 100)
  upper_band = (30, 255, 255)
  #cv2.imshow("Raw Camera 2", cv_image2)
  processed_imag=find_line(cv_image2, processed_imag,lower_band,upper_band)
  # the line ends are published inside the above function
  # Publishing as a topic ==> find out best practice for publishing
  cv2.imshow("Final Processed Imag", processed_imag)
  edited_imag = bridge.cv2_to_imgmsg(processed_imag, encoding="bgr8")
  #pub = rospy.Publisher('edited_imag/imag_with_text', Image, queue_size=1)
  pub.publish(edited_imag)



def main(args):
  rospy.init_node('camera_processing', anonymous=True)
  sub_imag = rospy.Subscriber("/downward_cam/camera/image",Image, image_callback)

  pub3.publish(edge_coordinate)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
