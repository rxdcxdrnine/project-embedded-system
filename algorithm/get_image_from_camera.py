from picamera.array import PiRGBArray
from picamera import PiCamera

import numpy as np
import cv2

def get_image_from_camera():
    camera = PiCamera()
    camera.resolution = (320,320)
    camera.color_effects = (128,128)

    img = np.empty((320, 320, 3), dtype=np.uint8)
    camera.capture(img, 'bgr')
    
    img = img[:,:,0]           ## 3 dimensions have the same value because camera is set to black and white
                               ## remove two dimension data
    print(img)
    
    threshold = int(np.mean(img))*0.5
    print(threshold)

    ## Invert black and white with threshold
    ret, img2 = cv2.threshold(img.astype(np.uint8), threshold, 255, cv2.THRESH_BINARY_INV)

    img2 = cv2.resize(img2,(16,16), interpolation=cv2.INTER_AREA)
    cv2.imshow("Image", img2)
    cv2.waitKey(0)
    return img2

if __name__ == "__main__":
    get_image_from_camera()