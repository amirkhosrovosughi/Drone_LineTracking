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


def main(args):
    image_name = "/home/amir/modified_drone_ws/src/drone_racing/tiers_drone_racing/images/shapes2.jpg"
    img = cv2.imread(image_name)
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
    cv2.imshow("Mask",mask)

    #get contour
    contours = getContours(mask)

    rgb_image, black_image =process_contours(mask, img, contours)
    cv2.imshow("Edited_Photo",rgb_image)
    #cv2.imshow("Black Photo",black_image)


    cv2.imshow("Original After",img)

    # Add Rectangular in middle
    #width = 50;
    #(rows,cols) = mask.shape
    #print ("Center is in {} , {} ".format(rows,cols))
    #img2	=	cv2.rectangle(mask, (width,width), (cols-width, rows- width), (255,255,255), -1)
    img2 = Fill_the_center(mask,width=50)
    cv2.imshow("Mask with rectangular",img2)

    # Done!
    cv2.waitKey(0)




if __name__ == '__main__':
    main(sys.argv)
