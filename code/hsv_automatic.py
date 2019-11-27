import cv2
import numpy as np

#detecter les mains via un hsv automatique

#récupérer la chose qui bouge le plus
#faire une espece de fonction qui dit tete // main
#barre hsv de la chose qui bouge le plus
#detection des mains


def nothing(x):
    pass


def video_lecture(video_name):

    video = cv2.VideoCapture(video_name)

    while True:

        _, frame = video.read()
        frame = cv2.resize(frame, (800, 600))

##        cv2.imshow("mask", mask)
##        cv2.imshow("res", res)
        cv2.imshow('Automatic HSV', frame)

        if cv2.waitKey(50) & 0xFF == ord('q'):
            break


    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":

    video_name = "a.mp4"

    video_lecture(video_name)
