# Copyright Reserved (2020).
# Donghee Lee, Univ. of Seoul
#
__author__ = 'will'

from rc_car_interface import RC_Car_Interface
import numpy as np
import time
import cv2
import serial
import math
import find_line as fl
import pickle
import copy

class SelfDriving:

    def __init__(self, ser):
        self.rc_car_cntl = RC_Car_Interface(ser)
        self.rc_car_cntl.set_left_speed(0, 150)
        self.rc_car_cntl.set_right_speed(0, 150)
    
        self.velocity = 0
        self.direction = 0
        self.image_size = 32


    def rc_car_control(self, direction):
        sensitivity = 150
        left_power = 1.0
        right_power = 1.0
        
        ## calculate left and right wheel speed with direction
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
        save_image_num = 5000
        alpha = 0.8
        list_image = []
        save_image = True
        run = True
        itr = 0

        while run:
            try:
                primitive_img = self.rc_car_cntl.get_image_from_camera(self.image_size)
                #print(primitive_img)
                
                # Image refine
                img = copy.copy(primitive_img)
                for i in range(self.image_size):
                    for j in range(self.image_size):
                        if img[i][j] < 220:
                            img[i][j] = 0
                        else:
                            img[i][j] = 255

                # Initialize
                direction = 0
                a = self.image_size - 1
                b = 0
                c = self.image_size - 1
                d = self.image_size - 1

                critical_points = fl.find_critical_points(img, self.image_size)

                # Calculate (a, b) and (c, d)
                (a, b, c, d) = fl.linepoints(critical_points, self.image_size, 7)
                if (a == c and b == d):
                    b = 0
                    d = self.image_size - 1

                # Find direction
                direction = fl.determine_direction(a, b, c, d, self.image_size)
                primitive_direction = direction

                # Phase correction with momentum
                direction = alpha * direction + (1.0 - alpha) * previous_direction

                # Update the previous direction
                previous_direction = direction
                print(primitive_direction)

                # Save image
                if save_image:
                    list_image.append([primitive_direction, 0, primitive_img])
                if len(list_image) >= save_image_num: 
                    break
                
                # Control the wheels
                self.rc_car_control(direction)

                itr = itr + 1
                if itr == 500:
                    run = False

            except KeyboardInterrupt:
                print("KeyboardInterrupt")
                break  

        self.rc_car_cntl.stop(150)
        cv2.destroyAllWindows()

        pickle.dump(list_image, open("new_32_trainingdata_3.p", "ab"))


try:
    ser =  serial.Serial('/dev/ttyACM0',9600)
except:
    ser = serial.Serial('/dev/ttyACM1',9600)

a = SelfDriving(ser)
a.drive()