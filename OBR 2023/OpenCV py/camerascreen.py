
import cv2
import numpy as np

video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()

    cv2.imshow("webcam", frame)
    
    if cv2.waitKey(1) & 0xff == ord("q"):
        break

video.release()
cv2.destroyAllWindows