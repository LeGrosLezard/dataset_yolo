import numpy as np
import cv2
import os



liste = os.listdir()

for i in liste:
    img = cv2.imread(i)
    cv2.imshow("image", img)
    

    if cv2.waitKey(0) & 0xFF == ord('a'):
        os.remove(i)
    else:
        pass
