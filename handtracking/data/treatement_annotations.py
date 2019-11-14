import os

import cv2

import scipy
from scipy.io import loadmat

from picture_operation import open_picture
from picture_operation import show_picture
from picture_operation import make_rectangle

from paths import path_annotation
from paths import annotations
from paths import path_picture
from paths import pictures


def make_liste_os(path):
    liste = os.listdir(path)

    return liste


def recuperate_points(points):
    """From annotation recuperate points of hands.
    One list for one hand. Ignore Right and Left informations"""

    #Sometimes we have only one hand.
    if len(points["boxes"][0]) == 2:
        coordinates = [[j[0].tolist() for i in points["boxes"][0][0] for j in i[0] if j[0] not in ("R", "L")],
                       [j[0].tolist() for i in points["boxes"][0][1] for j in i[0] if j[0] not in ("R", "L")]]
    else:
        coordinates = [[j[0].tolist() for i in points["boxes"][0][0] for j in i[0] if j[0] not in ("R", "L")]]


    return coordinates


def recuperate_detection(coordinates):
    """Recuperate rectangle of detections via min and max (x; y)"""

    detection = [[i[1] for i in coordinates],
                 [i[0] for i in coordinates]]

    return int(min(detection[0])), int(min(detection[1])),\
           int(max(detection[0])), int(max(detection[1]))




if __name__ == "__main__":

    #Make list of folder.
    p_annotation = make_liste_os(path_annotation)
    p_picture = make_liste_os(path_picture)

    for nb in range(len(p_annotation)):

        #Load .mat file.
        points = scipy.io.loadmat(annotations.format(p_annotation[nb]))

        #Recuperate annotations from .mat.
        coordinates = recuperate_points(points)

        for coord in coordinates:

            #Recuperate detection.
            (x, y, w, h) = recuperate_detection(coord)

            #Make a detection on a rectangle.
            make_rectangle(pictures.format(p_picture[nb]), x, y, w, h)



























