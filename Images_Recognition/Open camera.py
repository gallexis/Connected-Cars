import numpy as np
import cv2

# setup video capture
cap = cv2.VideoCapture(0)
ret,im = cap.read()

height, width = im.shape[:2]
print 'Height', height
print 'Width', width

while True:
    ret,im = cap.read()

    cv2.imshow('My camera',im)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
