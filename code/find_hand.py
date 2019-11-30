import cv2
import numpy as np
import time
import dlib


def find_head(face_cap, out, detector, frame1, frame2):

    #Make difference of background
    diff = cv2.absdiff(frame1, frame2)

    #Collect points of face
    points = [[face.left(), face.top(), face.right(), face.bottom()] for
              face in detector(cv2.cvtColor(face_cap, cv2.COLOR_BGR2GRAY))]

    contours = np.array([ [points[0][0] - 10, points[0][1] - 50],
                          [points[0][2] + 10, points[0][1] - 50],
                          [points[0][2] + 10, points[0][3] + 10],
                          [points[0][0] - 10, points[0][3] + 10] ])

    cv2.fillPoly(diff, pts=[contours], color=(0, 0, 0))

    return diff


def find_hand(copy, diff):

    imageYCrCb = cv2.cvtColor(diff, cv2.COLOR_BGR2YCR_CB)
    skinRegionYCrCb = cv2.inRange(imageYCrCb, np.array([0,133,77]),
                                            np.array([235,173,127]))

    skinYCrCb = cv2.bitwise_and(diff, diff, mask = skinRegionYCrCb)

    gray = cv2.cvtColor(skinYCrCb,cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 5, 255, 1)[1]


    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_NONE)

    #cv2.rectangle(copy, (x, y), (x+w, y+h), (0, 255, 0), 2)


    liste = [[cv2.boundingRect(contour)] for contour in contours if 5000 > cv2.contourArea(contour) > 100]

    liste1 = [i for i in liste if i[0][0] < 200]
    liste2 = [i for i in liste if i[0][0] > 200]


    def maxi(liste):
        rectangle = [min([i[0][0] for i in liste]),
                     min([i[0][1] for i in liste]),
                     max([i[0][0] for i in liste]),
                     max([i[0][1] for i in liste]),
                     max([i[0][2] for i in liste]),
                     max([i[0][3] for i in liste])]
        return rectangle

    pts = [maxi(liste1), maxi(liste2)]

    for pt in pts:
        print(pt)
        cv2.rectangle(copy, (pt[0], pt[1]), (pt[2] + pt[4], pt[3] + pt[5]), (0, 255, 0), 2)


def video_lecture(video_name):

    video = cv2.VideoCapture(video_name)

    frame1 = cv2.resize(video.read()[1], (400, 300))
    frame2 = cv2.resize(video.read()[1], (400, 300))
    detector = dlib.get_frontal_face_detector()

    while True:

        start_time = time.time()

        face_cap = cv2.resize(video.read()[1], (400, 300))
        copy = frame1.copy()

        try:
            diff = find_head(face_cap, copy, detector, frame1, frame2)
            find_hand(copy, diff)
        except: pass

        cv2.imshow('Automatic HSV', copy)

        frame1 = frame2
        frame2 = cv2.resize(video.read()[1], (400, 300))

        elapsed_time = time.time() - start_time
        print(elapsed_time)

        if cv2.waitKey(0) & 0xFF == ord('q'):
            cv2.imwrite('ici.jpg', face_cap)
            break

    video.release()
    cv2.destroyAllWindows()




if __name__ == "__main__":

    video_name = "video/a.mp4"

    video_lecture(video_name)








