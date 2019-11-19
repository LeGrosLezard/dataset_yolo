import numpy as np
from PIL import ImageGrab
import cv2

oinput = input("changement de dossier ?")


video = cv2.VideoCapture("e.mp4")
c = 0
while(True):

    ret, frame = video.read()

    cv2.imwrite("image5/" + str(c) +".jpg", frame)
    cv2.imshow('YEUX CAPTURE', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


    c += 1



video.release()
cv2.destroyAllWindows()
