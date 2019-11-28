import cv2
import numpy as np

from trackbarre_hsv import barre_tool
from trackbarre_hsv import parameter_ajusted
from trackbarre_hsv import nothing


#detecter les mains via un hsv automatique

#supression de fond
#récupérer la chose qui bouge le plus
#faire une espece de fonction qui dit tete // main
#barre hsv de la chose qui bouge le plus
#detection des mains


def blanck_picture(img):
    """ Create a black picture"""
    blank_image = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
    blank_image[0:, 0:] = 0, 0, 0
    return blank_image


def video_lecture(video_name):

    video = cv2.VideoCapture(video_name)

    _, frame1 = video.read()
    _, frame2 = video.read()

    frame1 = cv2.resize(frame1, (300, 200))
    frame2 = cv2.resize(frame2, (300, 200))



    while True:


        copy = frame1.copy()
        diff = cv2.absdiff(frame1, frame2)
        mask, res = parameter_ajusted(frame1)

        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(gray, 5, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


        for contour in contours:
            if cv2.contourArea(contour) < 100:
                cv2.fillPoly(thresh, pts =[contour], color=(0,0,0))

                kernel = np.ones((3,3), np.uint8)
                dilation = cv2.dilate(thresh, kernel, iterations=1)


        for x in range(dilation.shape[0]):
            for y in range(dilation.shape[1]):
                if dilation[x, y] == 0:
                    frame1[x, y] = 0


        l_b = np.array([0, 75, 130])
        u_b = np.array([255, 255, 255])

        hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, l_b, u_b)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for contour in contours:
            if cv2.contourArea(contour) > 5:
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(copy, (x, y), (x+w, y+h), (0, 255, 0), 2)


        cv2.imshow('Automatic HSV', copy)
        cv2.imshow('mask HSV', mask)


        frame1 = frame2
        _, frame2 = video.read()
        frame2 = cv2.resize(frame2, (300, 200))

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break


    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":

    video_name = "a.mp4"

    video_lecture(video_name)








