
import cv2
import numpy as np
import math

video = cv2.VideoCapture(0)

Trackbar =  "trackbar window"
cv2.namedWindow(Trackbar)

true = 102


def onChange(val):
    return

cv2.createTrackbar("Min Hue", Trackbar, 0, 255, onChange)
cv2.createTrackbar("Max Hue", Trackbar, 0, 255, onChange)
cv2.createTrackbar("Min Sat", Trackbar, 0, 255, onChange)
cv2.createTrackbar("Max Sat", Trackbar, 0, 255, onChange)
cv2.createTrackbar("Min Val", Trackbar, 0, 255, onChange)
cv2.createTrackbar("Max Val", Trackbar, 0, 255, onChange)


while True:
    ret, frame = video.read()
    #frame = cv2.flip(frame, 1)
    
    if not ret:
        video = cv2.VideoCapture(0)
        continue

    
    hue_min = cv2.getTrackbarPos("Min Hue", Trackbar)
    hue_max = cv2.getTrackbarPos("Max Hue", Trackbar)

    
    sat_min = cv2.getTrackbarPos("Min Sat", Trackbar)
    sat_max = cv2.getTrackbarPos("Max Sat", Trackbar)

    
    val_min = cv2.getTrackbarPos("Min Val", Trackbar)
    val_max = cv2.getTrackbarPos("Max Val", Trackbar)

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    kernel = np.ones((3,3), np.uint8)
    lowerColor = np.array([hue_min, sat_min, val_min])
    upperColor = np.array([hue_max, sat_max, val_max])
    mask = cv2.inRange(hsvImage, lowerColor, upperColor)
    
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        maxArea = cv2.contourArea(contours[0])
        contourMaxAreaId = 0
        i = 0

        for cnt in contours:
            if maxArea < cv2.contourArea(cnt):
                maxArea = cv2.contourArea(cnt)
                contourMaxAreaId = i
            i += 1

        cntMaxArea = contours[contourMaxAreaId]

        x, y, w, h = cv2.boundingRect(cntMaxArea)

        cv2.rectangle(frame, (x,y), (x+w,y+h),(0,0,255),2)
        contax = x + w / 2  
        contay = y + h / 2
        testey = round(contay)
        testex = round(contax)
        
        cv2.line(frame, (320, 240), (testex, testey), (0, 255, 100), 2)
        cv2.circle(frame, (testex,testey), 3, (0,0,255), 5)
        
        error = 320 - testex
        error2 = str(error)
        cv2.putText(frame,"erro = " + error2,(10,30),cv2.QT_FONT_NORMAL,1,255)
        
        
        
        
        #cv2.rectangle(frame, (x/2,y/2), (x/2+w/2,y/2+h/2),(0,0,255),2)
    

   
    cv2.circle(frame, (320,240), 3, (0,0,255), 5)
    maskedFrame = cv2.bitwise_and(frame, frame, mask = mask)

    cv2.imshow("mascara", maskedFrame)
    cv2.imshow("webcam", frame)
    #print(hue_max)
    
    if cv2.waitKey(1) & 0xff == ord("q"):
        break

video.release()
cv2.destroyAllWindows