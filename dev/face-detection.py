# import the necessary packages
from picamera import PiCamera
from picamera.array import PiRGBArray

import picamera.array
import time
import cv2


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)

face_cascade = cv2.CascadeClassifier("nodeopencv/node_modules/opencv/data/haarcascade_frontalface_default.xml")

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
        print ("found {0} faces".format(len(faces)))
        rawCapture.truncate(0)
  





