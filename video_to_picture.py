import numpy as np
from PIL import ImageGrab
import cv2
import os



oinput = input("changement de dossier ?")


video = cv2.VideoCapture("f.mp4")
c = 0
doss = 0

while(True):


    if c % 250 == 0:
        doss += 1
        os.makedirs("image6/" + str(doss))

    ret, frame = video.read()

    cv2.imwrite("image6/" + str(doss) + "/" + str(c) +".jpg", frame)
    cv2.imshow('YEUX CAPTURE', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


    c += 1



video.release()
cv2.destroyAllWindows()
