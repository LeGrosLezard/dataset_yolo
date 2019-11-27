import cv2
import numpy as np

#detecter les mains via un hsv automatique

#supression de fond
#récupérer la chose qui bouge le plus
#faire une espece de fonction qui dit tete // main
#barre hsv de la chose qui bouge le plus
#detection des mains





def video_lecture(video_name):

    video = cv2.VideoCapture(video_name)

    _, frame1 = video.read()
    _, frame2 = video.read()

    while True:

        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if 1000 > cv2.contourArea(contour) > 200:
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow('Automatic HSV', frame1)

        frame1 = frame2
        ret, frame2 = video.read()


        if cv2.waitKey(100) & 0xFF == ord('q'):
            break


    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":

    video_name = "a.mp4"

    video_lecture(video_name)








