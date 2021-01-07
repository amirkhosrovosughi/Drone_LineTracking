#!/usr/bin/env python

from __future__ import print_function

import threading
import time

import roslib; roslib.load_manifest('teleop_twist_keyboard')
import rospy

from geometry_msgs.msg import Twist
from sensor_msgs.msg  import Range

import sys, select, termios, tty
from std_msgs.msg import Int16MultiArray
import numpy
from subprocess import call

msg = """
Reading from the keyboard  and Publishing to Twist!
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .

For Holonomic mode (strafing), hold down the shift key:
---------------------------
   U    I    O
   J    K    L
   M    <    >

t : up (+z)
b : down (-z)

anything else : stop

q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%
--------------------------------
a: Autonomous Mode
s: Manual Mode
numbers(1,2,3): Select Autonomous Mode

CTRL-C to quit
"""
center_coordinate = numpy.zeros(2)

moveBindings = {
        'i':(1,0,0,0),
        'o':(1,0,0,-1),
        'j':(0,0,0,1),
        'l':(0,0,0,-1),
        'u':(1,0,0,1),
        ',':(-1,0,0,0),
        '.':(-1,0,0,1),
        'm':(-1,0,0,-1),
        'O':(1,-1,0,0),
        'I':(1,0,0,0),
        'J':(0,1,0,0),
        'L':(0,-1,0,0),
        'U':(1,1,0,0),
        '<':(-1,0,0,0),
        '>':(-1,-1,0,0),
        'M':(-1,1,0,0),
        't':(0,0,1,0),
        'b':(0,0,-1,0),
    }

speedBindings={
        'q':(1.1,1.1),
        'z':(.9,.9),
        'w':(1.1,1),
        'x':(.9,1),
        'e':(1,1.1),
        'c':(1,.9),
    }

Autonomous_Mode={
        '1':"Go 2 Center",
        '2':"Follow the line",
        '3':"Hovering",
    }



current_twist = Twist
drone_height = 0.0

class PublishThread(threading.Thread):
    def __init__(self, rate):
        super(PublishThread, self).__init__()
        self.publisher = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.th = 0.0
        self.speed = 0.0
        self.height = 0.0
        self.turn = 0.0
        self.condition = threading.Condition()
        self.flying = False
        self.init = False
        self.done = False

        # Set timeout to None if rate is 0 (causes new_message to wait forever
        # for new data to publish)
        if rate != 0.0:
            self.timeout = 1.0 / rate
        else:
            self.timeout = None

        self.start()

    def wait_for_subscribers(self):
        i = 0
        while not rospy.is_shutdown() and self.publisher.get_num_connections() == 0:
            if i == 4:
                print("Waiting for subscriber to connect to {}".format(self.publisher.name))
            rospy.sleep(0.5)
            i += 1
            i = i % 5
        if rospy.is_shutdown():
            raise Exception("Got shutdown request before subscribers connected")

    def update(self, x, y, z, th, speed, turn):
        self.condition.acquire()
        self.x = x
        self.y = y
        self.z = z
        self.th = th
        self.speed = speed
        self.turn = turn
        # Notify publish thread that we have a new message.
        self.condition.notify()
        self.condition.release()

    def stop(self):
        self.done = True
        self.update(0, 0, 0, 0, 0, 0)
        self.join()

    def takeoff(self):
        self.flying = True
        self.init = True

    def run(self):
        twist = Twist()
        while not self.done:
            self.condition.acquire()
            # Wait for a new message or timeout.
            self.condition.wait(self.timeout)

            # Copy state into twist message.
            twist.linear.x = self.x * self.speed
            twist.linear.y = self.y * self.speed
            twist.linear.z = self.z * self.speed
            twist.angular.x = 0
            twist.angular.y = 0
            twist.angular.z = self.th * self.turn

            self.condition.release()

            # Publish.
            self.publisher.publish(twist)
            global current_twist
            current_twist = twist

        # Publish stop message when thread exits.
        twist.linear.x = 0
        twist.linear.y = 0
        twist.linear.z = 0
        twist.angular.x = 0
        twist.angular.y = 0
        twist.angular.z = 0
        self.publisher.publish(twist)

    def update_height(self, height):
        self.height = height


def getKey(key_timeout):
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], key_timeout)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def vels(speed, turn):
    return "currently:\tspeed %s\tturn %s " % (speed,turn)

def sonar_callback(data):
    global drone_height
    drone_height = data.range
    return data.range

def center_callback(data0):
    global center_coordinate
    center_coordinate = data0.data
    return data0.data

def cmdvel_pub_thread():
    loop_pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
    while(1):
        global current_twist
        loop_pub.publish(current_twist)
        time.sleep(1)


def active_auto(autonomous):
    print('Go to Autonomous Mode')
    autonomous = True
    return  autonomous

def deactive_auto(autonomous):
    print('Go to Manual Mode')
    autonomous = False
    return  autonomous


def Autonomous_Mode_Execution(mode,key_timeout_1,autonomous):
    print('Starting the Autonomous mode '+Autonomous_Mode[mode])

    while not rospy.is_shutdown():
        try:
            # Based on mode (old key) and using if, elif else statement, call the approperiate function and find it
            #print('Hey, I am here in Autonomous while loop ...')
            if mode == '1':
                Go_2_center(mode)
            elif mode == '2':
                Follow_the_line(mode)
            else:
                print('Error! Unknown Autonomous mode is selected')
            key = getKey(key_timeout_1)
            print ('I recive '+key)
            if key in moveBindings:
                print('You are in Autonomous Mode, press s to enable manual control')
            if key in Autonomous_Mode:
                mode = key
                print('Autonomous mode is changed!')
            elif key == 's':
                autonomous = False
                print('Manual mode is activated')
                break
            #rospy.sleep(0.5)
        except KeyboardInterrupt:
            break
    return autonomous
        # Get interrupt if some key is processed
        # based on mode (old key) do right action, break, change mode or write switch to online mode
        # Based on mode (old key) and using if, elif else statement, call the approperiate function and find it



def Go_2_center(key):
    # check if updated sample is avialabe
    print('I am going to center')
    # write the code over here
    x = center_coordinate[0]/240
    y = center_coordinate[1]/240
    print ("Center is in {} and {}".format(center_coordinate[0], center_coordinate[1]))
    z = 0
    th = 0
    speed = 0.1
    turn = 0.1
    # This is not working, need to understand how .update works exactly, and also ...
    # make sure that /cmd_vel accept simataneouos linear command in x and y axis
    pub_thread.update(x, y, z, th, speed, turn)
    #return x, y, z, th, speed, turn

def Follow_the_line(key):
    # check if updated sample is avialabe
    print('I am following the line')
    # write the code over here
    x = center_coordinate[0]/240
    y = center_coordinate[1]/240
    z = 0
    th = 0
    speed = 0.05
    turn = 0.05
    pub_thread.update(x, y, z, th, speed, turn)
    #return x, y, z, th, speed, turn

if __name__=="__main__":

    autonomous = False


    settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('hydrid_drone_controller')


    speed = rospy.get_param("~speed", 0.5)
    turn = rospy.get_param("~turn", 1.0)
    repeat = rospy.get_param("~repeat_rate", 0.0)
    key_timeout = rospy.get_param("~key_timeout", 0.0)
    key_timeout_1 = rospy.get_param("~key_timeout", 0.1)
    if key_timeout == 0.0:
        key_timeout = None

    pub_thread = PublishThread(repeat)

    x = 0
    y = 0
    z = 0
    th = 0
    status = 0

    rospy.Subscriber("/sonar_height", Range, sonar_callback)
    rospy.Subscriber("/Processed_imag/center", Int16MultiArray, center_callback)

    try:
        pub_thread.wait_for_subscribers()
        pub_thread.update(x, y, z, th, speed, turn)

        t1 = threading.Thread(target = cmdvel_pub_thread)
        t1.setDaemon(True)
        t1.start()

        print(msg)
        print(vels(speed,turn))
        while(1):
            key = getKey(key_timeout)
            print('I found a key, for me')
            if key in ['t'] and not pub_thread.init:
                pub_thread.takeoff()
                print("===>>> Taking off ...")

            if key in ['d'] and pub_thread.flying:
                pub_thread.flying = False
                print("===>>> Landing ... ")

            if not pub_thread.init and key in ['u','i','o', 'j','k','l', 'm','.']:
                print("[Warning]: Please press 't' to take off first")
                continue

            pub_thread.update_height(drone_height)

            if key in moveBindings.keys():
                x = moveBindings[key][0]
                y = moveBindings[key][1]
                z = moveBindings[key][2]
                th = moveBindings[key][3]

            elif key in speedBindings.keys():
                speed = speed * speedBindings[key][0]
                turn = turn * speedBindings[key][1]

                print(vels(speed,turn))
                if (status == 14):
                    print(msg)
                status = (status + 1) % 15

            # Added by Amir
            elif key == 'a':
                autonomous=active_auto(autonomous)
            elif key == 's':
                autonomous=deactive_auto(autonomous)
            elif key in Autonomous_Mode and autonomous:
                autonomous =Autonomous_Mode_Execution(key,key_timeout_1,autonomous)
            #elif Mode_Selection_Status['1']==True:
            #    x, y, z, th, speed, turn =Go_2_center(key);
            else:
                # Skip updating cmd_vel if key timeout and robot already
                # stopped.
                if key == '' and x == 0 and y == 0 and z == 0 and th == 0:
                    print("Go here, nothing happen")
                    continue
                x = 0
                y = 0
                z = 0
                th = 0

                if (key == '\x03'):
                    print('Here here!')
                    break
            pub_thread.update(x, y, z, th, speed, turn)

    except Exception as e:
        print('something wrong happens')
        print(e)

    finally:
        pub_thread.stop()
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
