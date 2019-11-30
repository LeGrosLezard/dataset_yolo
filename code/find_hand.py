import cv2
import numpy as np
import time
import dlib


def find_head(face_cap, out, detector):

    faces = detector(cv2.cvtColor(face_cap, cv2.COLOR_BGR2GRAY))
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()
        cv2.rectangle(out, (x1, y1), (x2, y2), (0, 0, 255), 1)


    return (x1, y1, x2, y2)



def delete_area_face(head, frame1, frame2):
    diff = cv2.absdiff(frame1, frame2)


def find_hand(frame1, frame2, copy):

    diff = cv2.absdiff(frame1, frame2)

    mask = cv2.inRange(cv2.cvtColor(diff, cv2.COLOR_BGR2HSV),
                        np.array([0, 32, 10]),
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

        #try: head = find_head(face_cap, face_cap, detector)
        #except: pass

        find_hand(frame1, frame2, copy)


        #cv2.imshow('face_cap', face_cap)
        cv2.imshow('Automatic HSV', copy)


        frame1 = frame2
        frame2 = cv2.resize(video.read()[1], (800, 500))

        elapsed_time = time.time() - start_time
        print(elapsed_time)

        if cv2.waitKey(0) & 0xFF == ord('q'): break

    video.release()
    cv2.destroyAllWindows()




if __name__ == "__main__":

    video_name = "video/a.mp4"

    video_lecture(video_name)








