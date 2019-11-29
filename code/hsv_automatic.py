import cv2
import numpy as np
import time
import dlib


def find_head(gray, detector, out):

    faces = detector(gray)
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()
        cv2.rectangle(out, (x1, y1), (x2, y2), (0, 0, 255), 1)

    print(len(faces))

def video_lecture(video_name):

    video = cv2.VideoCapture(video_name)

    frame1 = cv2.resize(video.read()[1], (800, 600))
    frame2 = cv2.resize(video.read()[1], (800, 600))

    hiar = cv2.RETR_TREE; pts = cv2.CHAIN_APPROX_NONE
    detector = dlib.get_frontal_face_detector()

    while True:

        start_time = time.time()
        face_cap = cv2.resize(video.read()[1], (800, 500))

        #copy = frame1.copy()
        #diff = cv2.absdiff(frame1, frame2)


        faces = detector(cv2.cvtColor(face_cap, cv2.COLOR_BGR2GRAY))
        for face in faces:
            x1 = face.left()
            y1 = face.top()
            x2 = face.right()
            y2 = face.bottom()
            cv2.rectangle(face_cap, (x1, y1), (x2, y2), (0, 255, 0), 3)




##        mask = cv2.inRange(gray = cv2.cvtColor(copy, cv2.COLOR_BGR2HSV),
##                                 np.array([0, 75, 130]),
##                                 np.array([255, 255, 255]))
##
##        contours, _ = cv2.findContours(mask, hiar, pts)
##        for contour in contours:
##            (x, y, w, h) = cv2.boundingRect(contour)
##            cv2.rectangle(copy, (x, y), (x+w, y+h), (0, 255, 0), 2)


        cv2.imshow('face_cap', face_cap)
        #cv2.imshow('Automatic HSV', copy)

        #frame1 = frame2
        #frame2 = cv2.resize(video.read()[1], (800, 600))

        elapsed_time = time.time() - start_time
        print(elapsed_time)

        if cv2.waitKey(0) & 0xFF == ord('q'): break

    video.release()
    cv2.destroyAllWindows()




if __name__ == "__main__":

    video_name = "video/a.mp4"

    video_lecture(video_name)








