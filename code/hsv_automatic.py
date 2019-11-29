import cv2
import numpy as np

from trackbarre_hsv import parameter_ajusted




def video_lecture(video_name):

    video = cv2.VideoCapture(video_name)

    frame1 = cv2.resize(video.read()[1], (250, 150))
    frame2 = cv2.resize(video.read()[1], (250, 150))

    hiear = cv2.RETR_TREE; pts = cv2.CHAIN_APPROX_NONE

    while True:


        copy = frame1.copy()
        diff = cv2.absdiff(frame1, frame2)
        mask, res = parameter_ajusted(frame1)

        _, thresh = cv2.threshold(cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY),
                                  5, 255, cv2.THRESH_BINARY)
 
        contours, _ = cv2.findContours(thresh, hiear, pts)

        for contour in contours:
            if 10 > cv2.contourArea(contour) < 100:
                cv2.fillPoly(thresh, pts =[contour], color=(0,0,0))

                kernel = np.ones((3,3), np.uint8)
                dilation = cv2.dilate(thresh, kernel, iterations=1)


        for x in range(dilation.shape[0]):
            for y in range(dilation.shape[1]):
                if dilation[x, y] == 0:
                    frame1[x, y] = 0


        hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, np.array([0, 75, 130]),
                           np.array([255, 255, 255]))

        contours, _ = cv2.findContours(mask, hiear, pts)
 
        for contour in contours:
            if cv2.contourArea(contour) > 5:
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(copy, (x, y), (x+w, y+h), (0, 255, 0), 2)


        cv2.imshow('Automatic HSV', copy)


        frame1 = frame2
        frame2 = cv2.resize(video.read()[1], (250, 150))

        if cv2.waitKey(0) & 0xFF == ord('q'): break

    video.release()
    cv2.destroyAllWindows()




if __name__ == "__main__":

    video_name = "video/a.mp4"

    video_lecture(video_name)
