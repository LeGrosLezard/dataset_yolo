import cv2
import numpy as np
import time
import dlib


def find_head(face_cap, out, detector, frame1, frame2):

    #Make difference of background
    diff = cv2.absdiff(frame1, frame2)

    #Collect points of face



    contours = [np.array([ [face.left() - 10, face.top() - 50],
                [face.right() + 10, face.top() - 50],
                [face.right() + 10, face.bottom() + 10],
                [face.left() - 10, face.bottom() + 10] ])
                for face in
                detector(cv2.cvtColor(face_cap, cv2.COLOR_BGR2GRAY))]

    cv2.fillPoly(diff, pts=[contours][0], color=(255,255,255))

    return diff



def find_hand(copy, diff):

    mask = cv2.inRange(cv2.cvtColor(diff, cv2.COLOR_BGR2HSV),
                        np.array([0, 32, 30]),
                        np.array([255, 255, 255]))

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        if cv2.contourArea(contour) > 100:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(copy, (x, y), (x+w, y+h), (0, 255, 0), 2)




def video_lecture(video_name):

    video = cv2.VideoCapture(video_name)

    frame1 = cv2.resize(video.read()[1], (800, 500))
    frame2 = cv2.resize(video.read()[1], (800, 500))
    detector = dlib.get_frontal_face_detector()

    while True:

        start_time = time.time()

        face_cap = cv2.resize(video.read()[1], (800, 500))
        copy = frame1.copy()

 
        diff = find_head(face_cap, copy, detector, frame1, frame2)

        find_hand(copy, diff)

        cv2.imshow('Automatic HSV', copy)



        frame1 = frame2
        frame2 = cv2.resize(video.read()[1], (800, 500))

        elapsed_time = time.time() - start_time
        print(elapsed_time)

        if cv2.waitKey(2) & 0xFF == ord('q'): break

    video.release()
    cv2.destroyAllWindows()




if __name__ == "__main__":

    video_name = "video/a.mp4"

    video_lecture(video_name)








