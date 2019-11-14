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

    coordinates = [[], []]

    for nb, i in enumerate(points["boxes"][0]):
        for j in i[0][0]:
            if j[0] not in ("R", "L"):
                coordinates[nb].append(j[0].tolist())

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

            #Sometimes we have only one hand.
            if coord != []:

                #Recuperate detection.
                (x, y, w, h) = recuperate_detection(coord)

                #Make a detection on a rectangle.
                make_rectangle(pictures.format(p_picture[nb]), x, y, w, h)



























