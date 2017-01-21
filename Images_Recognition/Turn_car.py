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

    compteur_NG = 0
    compteur_BG = 0
    compteurG = 0
    compteur_ND = 0
    compteur_BD = 0
    compteurD = 0
    pixels = np.asarray(th, np.uint8)

    for i in range(height):
       im[i][40] = [0, 0, 255]
       im[i][600] = [0, 0, 255]

    for y in range(40, width-40):
        im[400][y] = [0, 0, 255]
        
    
    for x in range(height):

        compteurG +=1
        
        if th[x][40] == 0 :
            compteur_NG +=1
        if th[x][40] == 255 :
            compteur_BG +=1
            

    for x in range(height):

        compteurD +=1
        
        if th[x][440] == 0 :
            compteur_ND +=1
        if th[x][440] == 255 :
            compteur_BD +=1
            

    if compteur_NG > 50 :
        print 'Tourner à droite'

    if compteur_ND > 50 :
        print 'Tourner à Gauche'

    if compteur_NG <= 50 & compteur_ND <= 50 :
        print 'Forward'

    cv2.imshow('My camera',im)
    cv2.imshow('Binary camera', th)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
