#!/usr/bin/env python

import numpy as np
import cv2
import sys


def getContours(binary_image):
    _ ,contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def process_contours(mask, img, contours):
    rgb_image = img
    binary_image = mask
    black_image = np.zeros([binary_image.shape[0], binary_image.shape[1],3],'uint8')
    (rows,cols,channels) = rgb_image.shape

    #contours_poly = [None]*len(contours)
    #boundRect = [None]*len(contours)
    #centers = [None]*len(contours)


    for c in contours:
        global center_coordinate
        area = cv2.contourArea(c)
        if area > 20:
            if True:
                perimeter= cv2.arcLength(c, True)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                cv2.drawContours(rgb_image, [c], -1, (226,198,85), 3)
                cv2.drawContours(black_image, [c], -1, (226,198,85), 3)

                #contours_poly[c] = cv2.approxPolyDP(c, 3, True)
                #boundRect[c] = cv2.boundingRect(contours_poly[c])
                #centers[c], radius[c] = cv2.minEnclosingCircle(contours_poly[c])


                #cv2.imshow("RGB Image Contours - Circle",rgb_image)
                #cv2.imshow("Black Image Contours - Circle",black_image)
            else:
                print('Undefined object code!')

    return rgb_image, black_image


def Fill_the_center(mask,width):
    (rows,cols) = mask.shape
    print ("Center is in {} , {} ".format(rows,cols))
    img2	=	cv2.rectangle(mask, (width,width), (cols-width, rows- width), (255,255,255), -1)
    return img2



import cv2

def rotate_image(mat, angle):
    """
    Rotates an image (angle in degrees) and expands image to avoid cropping
    """

    height, width = mat.shape[:2] # image shape has 3 dimensions
    image_center = (width/2, height/2) # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape

    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)

    # rotation calculates the cos and sin, taking absolutes of those.
    abs_cos = abs(rotation_mat[0,0])
    abs_sin = abs(rotation_mat[0,1])

    # find the new width and height bounds
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    # subtract old image center (bringing image back to origo) and adding the new image center coordinates
    rotation_mat[0, 2] += bound_w/2 - image_center[0]
    rotation_mat[1, 2] += bound_h/2 - image_center[1]

    # rotate image with the new bounds and translated rotation matrix
    rotated_mat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))
    return rotated_mat





def main(args):
    image_name = "/home/amir/modified_drone_ws/src/drone_racing/tiers_drone_racing/images/shapes2.jpg"
    img = cv2.imread(image_name)
    img2 = cv2.imread(image_name)
    cv2.imshow("original",img)





    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #cv2.namedWindow("HSV", cv2.WINDOW_NORMAL)
    h, s, v = cv2.split(hsv)
    hsv_imag = np.concatenate((h,s,v),axis=1)
#cv2.imshow("HSV",hsv_imag)

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Mask
    lower_band =(45, 100, 100)
    upper_band = (90, 255, 255)
    mask = cv2.inRange(hsv, lower_band, upper_band)
    #cv2.imshow("Mask",mask)

    #get contour
    contours = getContours(mask)

    rgb_image, black_image =process_contours(mask, img, contours)
    #cv2.imshow("Edited_Photo",rgb_image)
    #cv2.imshow("Black Photo",black_image)

    yaw = 35
    h = 3
    c_x = 0
    c_y = 0


    backtorgb = cv2.cvtColor(mask,cv2.COLOR_GRAY2RGB)
    height, width = backtorgb.shape[:2]
    backtorgb[:,:,0]=np.ones((height, width))*255
    backtorgb[np.where((backtorgb==[255,255,255]).all(axis=2))] = [0,0,255]
    cv2.imshow("not compressed",backtorgb)


    rotated_img=rotate_image(backtorgb, yaw)

    percent = 20
    dim = (int(rotated_img.shape[1]*percent/100), int(rotated_img.shape[0]*percent/100))
    resized=cv2.resize(rotated_img, dsize=dim, interpolation =cv2.INTER_LINEAR)

    cv2.imshow("Compressed",resized)




    #cv2.imwrite('resized.png', resized)

    #rotated_img=rotate_image(resized, 15)

    #cv2.imshow("Original After",rotated_img)

    # Add Rectangular in middle
    #width = 50;
    #(rows,cols) = mask.shape
    #print ("Center is in {} , {} ".format(rows,cols))
    #img2	=	cv2.rectangle(mask, (width,width), (cols-width, rows- width), (255,255,255), -1)
    #img2 = Fill_the_center(mask,width=50)
    #cv2.imshow("Mask with rectangular",img2)

    # Done!
    cv2.waitKey(0)




if __name__ == '__main__':
    main(sys.argv)
