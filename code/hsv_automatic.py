import cv2
import numpy as np
import time



def video_lecture(video_name):

    video = cv2.VideoCapture(video_name)

    frame1 = cv2.resize(video.read()[1], (250, 150))
    frame2 = cv2.resize(video.read()[1], (250, 150))

    hiar = cv2.RETR_TREE; pts = cv2.CHAIN_APPROX_NONE

    while True:

        start_time = time.time()

        copy = frame1.copy()
        diff = cv2.absdiff(frame1, frame2)

        mask = cv2.inRange(cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV),
                           np.array([0, 75, 130]),
                           np.array([255, 255, 255]))

        contours, _ = cv2.findContours(mask, hiar, pts)
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(copy, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow('Automatic HSV', copy)

        frame1 = frame2
        frame2 = cv2.resize(video.read()[1], (250, 150))

        elapsed_time = time.time() - start_time
        print(elapsed_time)

        if cv2.waitKey(0) & 0xFF == ord('q'): break

    video.release()
    cv2.destroyAllWindows()




if __name__ == "__main__":

    video_name = "video/a.mp4"

    video_lecture(video_name)








