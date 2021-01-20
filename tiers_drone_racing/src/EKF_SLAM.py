#!/usr/bin/env python
import numpy as np
import math

def My_func():
    print('It is importet correctly')



class EKF_SLAM(object):
    def __init__(self, Robot_dimention=3, process_noise = np.array([[0.01,0],[0,0.005]]),sampling_time = 0.1):
        self.R = np.zeros([Robot_dimention,1])
        self.Q = process_noise
        self.dt = sampling_time

        print(self.R)
        print(self.Q)


    def move(self,cmd_vel):
        theta = self.R[2]
        print(cmd_vel)

        dx = cmd_vel[0]
        dtheta = cmd_vel[1]

        theta_new = theta + dtheta*self.dt
        if theta_new > np.pi:
            theta_new = theta_new - 2*np.pi
        if theta_new < np.pi:
            theta_new = theta_new - 2*np.pi

        dp = np.array([[dx[0], 0]]).T*self.dt

        print("This is: ", dp)

        Position_new, TO_r, TO_bq =self.FromFram2D(dp)

        AO_a = 1
        AO_da = 1

        RO_r = np.vstack([TO_r , [0, 0, AO_a]])
        RO_n = np.array([[1, 0],[0, 0],[0, 1]])

        R_new = np.vstack([Position_new , theta_new])
        self.R = R_new

        return


    def FromFram2D(self,p_r):
        print("p_r", p_r)

        t = self.R[0:1]
        theta = self.R[2]
        R = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])

        p = np.dot(R,p_r)+ t

        px = p_r[0][0]
        py= p_r[1][0]


        P_r_1 = -py*math.cos(theta) -px*math.sin(theta)
        P_r_2 = px*math.cos(theta) -px*math.sin(theta)
        print(px, py,P_r_1, P_r_2)
        print(P_r_1)
        P_r = np.array([[1,0,P_r_1],[0,1,P_r_2]])


        P_pr = R

        print(R)

        return p , P_r, P_pr
