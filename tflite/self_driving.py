# Copyright Reserved (2020).
# Donghee Lee, Univ. of Seoul
#
__author__ = 'will'

from rc_car_interface import RC_Car_Interface
from tf_learn import DNN_Driver
import numpy as np
import time
import cv2
import serial
import math

class SelfDriving:

    def __init__(self, ser):
        self.rc_car_cntl = RC_Car_Interface(ser)
        self.dnn_driver = DNN_Driver()

        self.rc_car_cntl.set_left_speed(0, 150)
        self.rc_car_cntl.set_right_speed(0, 150)
    
        self.velocity = 0
        self.direction = 0
        self.image_size = 32

        self.dnn_driver.tf_load("model.tflite")
        
        
    def rc_car_control(self, direction):
        sensitivity = 150
        left_power = 0.95
        right_power = 0.95
        
        ## Calculate left and right wheel speed with direction
        if direction < -1.0:
            direction = -1.0
        if direction > 1.0:
            direction = 1.0

        #print("direction: ", direction)
        if (direction <= 0.0):
            right_speed = int(((255 - sensitivity) + int((1.0)*sensitivity))*right_power)
            left_speed = int(((255 - sensitivity) + int((1.0 + direction)*sensitivity))*left_power)
        else:
            right_speed = int(((255 - sensitivity) + int((1.0 - direction)*sensitivity))*right_power)
            left_speed = int(((255 - sensitivity) + int((1.0)*sensitivity))*left_power)

        self.rc_car_cntl.set_wheel_speed(right_speed, left_speed, 150)
        
        
    def drive(self):
        previous_direction = 0
        alpha = 0.85
        while True:
            img = self.rc_car_cntl.get_image_from_camera(self.image_size)
            
            # Image formatting
            img = img[..., np.newaxis].astype(np.float32)

            # Predict with single image
            direction = self.dnn_driver.predict_direction(img)
            
            # Linear transformation from [0,180] to [1,-1]
            direction = ((-1)/90)*direction + 1
            
            # Phase correction with momentum
            direction = alpha*direction + (1-alpha)*previous_direction

            # Update the previous direction
            previous_direction = direction

            # Control the wheels
            self.rc_car_control(direction)
            
        self.rc_car_cntl.stop(150)
        cv2.destroyAllWindows()


try:
    ser =  serial.Serial('/dev/ttyACM0',9600)
except:
    ser = serial.Serial('/dev/ttyACM1',9600)

a = SelfDriving(ser)
a.drive()