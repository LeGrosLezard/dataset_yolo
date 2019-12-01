import cv2
import numpy as np
import time
import dlib
from starter import *

def find_head(face_cap, out, detector, frame1, frame2):
    """We find the head and draw a white mask on it. We
    can recuperate only the hands"""

    #Make difference of background.
    diff = cv2.absdiff(frame1, frame2)

    #Collect points of face.
    points = [[face.left(), face.top(), face.right(), face.bottom()] for
              face in detector(cv2.cvtColor(face_cap, cv2.COLOR_BGR2GRAY))]

    #Display head for only have hands.
    cv2.fillPoly(diff, pts=[np.array([ [points[0][0] - 10, points[0][1] - 50],
                                       [points[0][2] + 10, points[0][1] - 50],
                                       [points[0][2] + 10, points[0][3] + 50],
                                       [points[0][0] - 10, points[0][3] + 50]  ])],
                 color=(0, 0, 0))

    return diff


def skin_detection(picture):

    #Convert BGR to YCR_CB, define mask.
    skinRegionYCrCb = cv2.inRange(cv2.cvtColor(picture, cv2.COLOR_BGR2YCR_CB),
                                  np.array([0, 50, 77]), np.array([235, 235, 127]))
    #Make mask.
    skinYCrCb = cv2.bitwise_and(picture, picture, mask = skinRegionYCrCb)

    return skinYCrCb


def find_hand(diff):
    """We recuperate global detection of hands by:
    filter of colors. And analysis of contours."""

    #Recuperate skin detector
    skinYCrCb = skin_detection(diff)

    #Add threshold filter.
    thresh = cv2.threshold(cv2.cvtColor(skinYCrCb, cv2.COLOR_BGR2GRAY), 5, 255, 1)[1]

    #Search contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    #Recuperate 100 < contour < 5000.
    detection = [[cv2.boundingRect(contour)] for contour in contours if
                 5000 > cv2.contourArea(contour) > 100]

    #Recuperate all right and left hands detections. mid width frame is 200.
    hands = [[i for i in detection if i[0][0] < 200], [i for i in detection if i[0][0] > 200]]

    return hands



def extraction_hands(hands, diff, copy):

    def including_detection(liste):
        """Recuperate extremum points of detections"""

        rectangle = [min([i[0][0] for i in liste]), min([i[0][1] for i in liste]),
                     max([i[0][2] for i in liste]), max([i[0][3] for i in liste])]

        return rectangle



    def make_line(thresh, adding):
        """We make line for detect more than one area
        with border, on eyelashes is paste to the border"""

        cv2.line(thresh, (0, 0), (0, thresh.shape[0]), (255, 255, 255), adding)
        cv2.line(thresh, (0, 0), (thresh.shape[1], 0), (255, 255, 255), adding)
        cv2.line(thresh, (thresh.shape[1], 0), (thresh.shape[1], thresh.shape[0]), (255, 255, 255), adding)
        cv2.line(thresh, (0,  thresh.shape[0]), (thresh.shape[1], thresh.shape[0]), (255, 255, 255), adding)

        return thresh






    #Draw the global includes detections.
    for hand, pt in enumerate([including_detection(hands[0]), including_detection(hands[1])]):

        crop_detection = copy[pt[1]: pt[1] + pt[3], pt[0] : pt[0] + pt[2] ]

        skin_mask = skin_detection(crop_detection)

        thresh = cv2.threshold(cv2.cvtColor(skin_mask, cv2.COLOR_BGR2GRAY), 5, 255, 1)[1]
        thresh = make_line(thresh, 1)


        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        maxi = 0; maxi1 = 0
        for cnts in contours:
            if cv2.contourArea(cnts) > maxi:
                maxi = cv2.contourArea(cnts)
            if cv2.contourArea(cnts) < maxi and cv2.contourArea(cnts) > maxi1:
                maxi1 = cv2.contourArea(cnts)

        for cnts in contours:
            if cv2.contourArea(cnts) == maxi1 and cv2.contourArea(cnts) > 2000:
                x, y, w, h = cv2.boundingRect(cnts)

            elif cv2.contourArea(cnts) == maxi:
                x, y, w, h = cv2.boundingRect(cnts)


        crop = crop_detection[y:y+h, x:x+w]

        #show_picture("crop", crop, 0, "")


        ok = skin_detection(crop)
        thresh = cv2.threshold(cv2.cvtColor(ok, cv2.COLOR_BGR2GRAY), 1, 255, 1)[1]

        thresh = make_line(thresh, 5)

        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        maxi = 0; maxi1 = 0
        for cnts in contours:
            if cv2.contourArea(cnts) > maxi:
                maxi = cv2.contourArea(cnts)
            if cv2.contourArea(cnts) < maxi and cv2.contourArea(cnts) > maxi1:
                maxi1 = cv2.contourArea(cnts)

        for cnts in contours:
            if cv2.contourArea(cnts) == maxi1:
                cv2.drawContours(crop_detection, [cnts], -1, (0,255,0), 3)











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
            hands = find_hand(diff)
            extraction_hands(hands, diff, copy)
        except: pass #no hands or no head

        cv2.imshow('Automatic HSV', copy)

        frame1 = frame2
        frame2 = cv2.resize(video.read()[1], (400, 300))

        elapsed_time = time.time() - start_time
        print(elapsed_time)

        if cv2.waitKey(1) & 0xFF == ord('q'): break

    video.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":

    video_name = "video/a.mp4"

    video_lecture(video_name)








