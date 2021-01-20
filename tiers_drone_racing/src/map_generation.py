#!/usr/bin/env python

import rospy
import cv2
import sys
import numpy as np
import tf
import math


from sensor_msgs.msg  import Range
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Int16MultiArray

from EKF_SLAM import My_func
from EKF_SLAM import EKF_SLAM


drone_height = 0
imag_circle = np.zeros((120, 120))
imag_line = np.zeros((120, 120))
bridge = CvBridge()

robot_x = 0
robot_y = 0

cmd_vel = np.zeros((2,1));
# subcribe from:

# 1) camera/mask, 2) /sonar_height, 3)tf/tfMessage ==> get time of receiveig (
# see time timem tag can be defined from original data from gazebo, or needed to work with the time that we get the data0

# go to while(1) loop, repead it every 1 sec


#What left

# subscribe to tf
# pubilsih map
# define mapping function
# a lot of functions, move them to av class later


def sonar_callback(data):
    global drone_height
    drone_height = data.range
    #print('drone_height')
    return data.range


def circle_callback(data):
    global bridge
    global imag_circle
    #print('I got a mask')
    #convert ros_image into an opencv-compatible image
    try:
      imag_circle = bridge.imgmsg_to_cv2(data, "mono8")
    except CvBridgeError as e:
        print(e)

    #cv2.imshow("Circle in MapG", imag_circle)
    #cv2.waitKey(3)


def line_callback(data):
    global bridge
    global imag_line
    #print('I got a mask 2')
    #convert ros_image into an opencv-compatible image
    try:
      imag_line = bridge.imgmsg_to_cv2(data, "mono8")
    except CvBridgeError as e:
        print(e)
    #cv2.imshow("Line in MapG", imag_line)
    #cv2.waitKey(3)

def image_callback(data):
    print("I got an image")

###################### Below Functions Must to into a class ####################

def compile_map(MAP_info):
    pass
    # get the MAP_info data and produce associated MAP/ or publish it to RVIZ

def map_update(MAP_info,robot_x,robot_y,robot_yaw,drone_height):
    # find the corespond pixel to center of robot based on robot_x, robot_y #==> Extend for connsidering pitch, roll
    # based on heigh and field of view, find required resolution of the map, width = 90/2, hight = 73.74/2
    # imapge proccesing using opencv
    # map_update map
    # compile map
    pass
    #include radian disturtion effects later



def init_map(map_range, map_resolution):
    object_num = 2 #==> for now, we have only line and circle

    x_dimention = int((map_range[0][1]-map_range[0][0])/map_resolution)
    y_dimention = int((map_range[0][1]-map_range[0][0])/map_resolution)
    MAP_info = np.zeros((x_dimention,y_dimention,object_num*2+1))
    print("Map dimention is: ", MAP_info.shape)
    return MAP_info

    # Map_info is data structure to store imag from observation of different sample
    # each pixel of map has its own array MAP_info[i,j,:]
    # first element ==> Frequency of seeing a map pixel
    # second element ==> how much empty have seen
    # thried element ==> hhow much element G has seen

################################################################################


def main(args):
    global drone_height

    rospy.init_node('map_generator')
    rospy.Subscriber("/sonar_height", Range, sonar_callback)
    rospy.Subscriber("/Processed_imag/mask_circle", Image, circle_callback)
    rospy.Subscriber("/Processed_imag/mask_line", Image, line_callback)


    listener = tf.TransformListener()

    map_resolution = 0.1
    map_range = [[-10, 10],[-10, 10]]
    MAP_info = init_map(map_range, map_resolution) #==> initialize MAP Data Strcuture

    sampling_time = 2.0

    My_func()
    slam=EKF_SLAM(sampling_time = 2.0)

    sampling_time = 2.0
    r = rospy.Rate(1/sampling_time) # 10hz

    while not rospy.is_shutdown():
        print(drone_height)

        slam.move(cmd_vel) #==> move the robot,prediction
        # Next ==> read the features from the rostopic ==> How we will do association?

        # Real position of the robot, is not used in the algorithm
        now = rospy.Time.now()
        listener.waitForTransform('world', 'base_footprint', now, rospy.Duration(2.0))
        (trans,rot) = listener.lookupTransform('world', 'base_footprint', now)
        # tf to be replace later with Pose estimator using IMU, GPS and ...
        robot_x = trans[0]
        robot_y = trans[1]
        rpy = tf.transformations.euler_from_quaternion(rot)
        #print(rpy)
        robot_yaw = rpy[2]


        cv2.imshow("Line in MapG", imag_line)
        cv2.imshow("Circle in MapG", imag_circle)
        cv2.waitKey(3)
        r.sleep()


if __name__ == '__main__':
    print("Hi!")
    main(sys.argv)
