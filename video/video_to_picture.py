import numpy as np
from PIL import ImageGrab
import cv2
import os



oinput = input("changement de dossier ?")

name = "image11"
video = cv2.VideoCapture("h.mp4")
c = 0
doss = 0

while(True):


    if c % 250 == 0:
        doss += 1
        os.makedirs(name + "/" + str(doss))

    ret, frame = video.read()

    cv2.imwrite(name + "/" +str(doss) + "/" + str(c) +".jpg", frame)
    cv2.imshow('YEUX CAPTURE', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


    c += 1



video.release()
cv2.destroyAllWindows()
