# Copyright(c) Reserved 2020.
# Donghee Lee, University of Soul
#
__author__ = 'will'


import numpy as np
import cv2
import serial
import time
from picamera.array import PiRGBArray
from picamera import PiCamera


class RC_Car_Interface:

    def __init__(self,ser):
        self.ser = ser
        self.left_wheel = 0
        self.right_wheel = 0
        self.camera = PiCamera()
        self.camera.resolution = (320,320)      ## set camera resolution to (320, 320)
        self.camera.color_effects = (128,128)   ## set camera to black and white


    def set_wheel_speed(self, right_speed, left_speed, delay_time):
        #print('set right speed to ', right_speed)
        #print('set left speed to ', left_speed)
        cmd = ("R%dL%dT%d\n" % (right_speed, left_speed, delay_time)).encode('ascii')
        #print("My cmd is %s" % cmd)
        self.ser.reset_output_buffer()
        self.ser.write(cmd)


    def set_right_speed(self, speed, delay_time):
        #print('set right speed to ', speed)
        cmd = ("R%dL%dT%d\n" % (speed, 0, delay_time)).encode('ascii')
        #print("My cmd is %s" % cmd)
        self.ser.reset_output_buffer()
        self.ser.write(cmd)
        

    def set_left_speed(self, speed, delay_time):
        #print('set left speed to ', speed)
        cmd = ("R%dL%dT%d\n" % (0, speed, delay_time)).encode('ascii')
        #print("My cmd is %s" % cmd)
        self.ser.reset_output_buffer()
        self.ser.write(cmd)
        

    def stop(self, delay_time):     # robot stop
        #print('stop')
        cmd = ("R%dL%dT%d\n" % (0, 0, delay_time)).encode('ascii')
        #print("My cmd is %s" % cmd)
        self.ser.reset_output_buffer()
        self.ser.write(cmd)

        
    def get_image_from_camera(self, image_size):
        img = np.empty((320, 320, 3), dtype=np.uint8)
        self.camera.capture(img, 'bgr')
        
        ## 3 dimensions have the same value because camera is set to black and white
        ## remove two dimension data
        img = img[:,:,0]
        
        threshold = int(np.mean(img))*0.5


        ## Invert black and white with threshold
        ret, img2 = cv2.threshold(img.astype(np.uint8), threshold, 255, cv2.THRESH_BINARY_INV)
        img2 = cv2.resize(img2,(image_size, image_size), interpolation=cv2.INTER_AREA )
        # cv2.imshow("Image", img2)
        # cv2.waitKey(0)
        return img2
    




