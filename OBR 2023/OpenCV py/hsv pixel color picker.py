
import cv2
import numpy as np

video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    (h, s, v) = hsvImage[400, 400]

    h, s, v = str(h), str(s), str(v)

    cv2.putText(frame,"Hue: " + h,(10,30),cv2.QT_FONT_NORMAL,1,255)
    cv2.putText(frame,"Sat: " + s,(10,60),cv2.QT_FONT_NORMAL,1,255)
    cv2.putText(frame,"Val: " + v,(10,90),cv2.QT_FONT_NORMAL,1,255)
    cv2.circle(frame, (400,400), 3, (255,255,255), 10)





    cv2.imshow("webcam", frame)
    
    if cv2.waitKey(1) & 0xff == ord("q"):
        break

video.release()
cv2.destroyAllWindows