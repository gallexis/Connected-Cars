import numpy as np
import cv2

# setup video capture
cap = cv2.VideoCapture(0)
ret,im = cap.read()


gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)


height, width = im.shape[:2]
print height
print width

while True:
    ret,im = cap.read()
    
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    th = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)

    compteur_N = 0
    compteur_B = 0
    pixels = np.asarray(th, np.uint8)

    for i in range(height):
       im[i][40] = [0, 0, 255]
       im[i][600] = [0, 0, 255]
       
    for y in range(40, width-40):
        im[350][y] = [0, 0, 255]

        if th[350][y] == 0 :
            compteur_N +=1
        if th[350][y] == 255 :
            compteur_B +=1

    if compteur_N <= 100 :
        print 'Forward'
    if compteur_N > 100 :
        print 'Obstacle'

    cv2.imshow('video test',im)
    cv2.imshow('video test 2', th)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
