""" - We load .mat file,
    - We recuperate points into list from the .mat file,
    - We recuperate min(x;y) max(x;y) for the detection,
    - We display it on picture ANIMATION,
    - We convert it into YOLO annotations,
    - We write it into a .txt file.
"""

#For run folder
import os

#For have a visual
import cv2

#For load .mat file
import scipy
from scipy.io import loadmat

#For have a visual
from picture_operation import open_picture
from picture_operation import show_picture
from picture_operation import make_rectangle

#Paths for folder.
from paths import path_annotation
from paths import annotations
from paths import path_picture
from paths import pictures
from paths import path_txt_annotation


def make_liste_os(path):
    """We make a list of the folder for run it"""

    #print(path)
    liste = os.listdir(path)

    #print(liste)
    return liste


def recuperate_points(points):
    """From annotation recuperate points of hands.
    One list for one hand. Ignore Right and Left informations"""

    #print(points)
    #print(points["boxes"][0])

    #Sometimes we have only one hand.
    if len(points["boxes"][0]) == 2:
        coordinates = [[j[0].tolist() for i in points["boxes"][0][0]\
                        for j in i[0] if j[0] not in ("R", "L")],
                       [j[0].tolist() for i in points["boxes"][0][1]\
                        for j in i[0] if j[0] not in ("R", "L")]]
    else:
        coordinates = [[j[0].tolist() for i in points["boxes"][0][0]\
                        for j in i[0] if j[0] not in ("R", "L")]]

    #print(coordinates)
    return coordinates


def recuperate_detection(coordinates):
    """Recuperate rectangle of detections via min and max (x; y)"""

    #print(coordinates)

    detection = [[i[1] for i in coordinates],
                 [i[0] for i in coordinates]]

    #print(detection)
    return int(min(detection[0])), int(min(detection[1])),\
           int(max(detection[0])), int(max(detection[1]))


def convert_to_yolo_annotation(size, x, y, w, h):
    """https://github.com/ManivannanMurugavel/Yolo-Annotation-Tool-New-/blob/master/main.py"""

    #print(size, x, y, w, h)

    dw = 1./size[0]
    dh = 1./size[1]
    x = (x + w)/2.0
    y = (y + h)/2.0
    w = w - x
    h = h - y
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh

    #print((x, y, w, h))
    return (x, y, w, h)


def write_into_txt_file():
    pass



if __name__ == "__main__":

    """ - We load .mat file,
        - We recuperate points into list from the .mat file,
        - We recuperate min(x;y) max(x;y) for the detection,
        - We display it on picture ANIMATION,
        - We convert it into YOLO annotations,
        - We write it into a .txt file.
    """

    #Make list of folder.
    p_annotation = make_liste_os(path_annotation)
    p_picture = make_liste_os(path_picture)

    for nb in range(len(p_annotation)):

        #Load .mat file.
        points = scipy.io.loadmat(annotations.format(p_annotation[nb]))
        #print(points)

        #Recuperate annotations from .mat.
        coordinates = recuperate_points(points)
        #print(coordinates)

        for coord in coordinates:

            #Recuperate detection.
            (x, y, w, h) = recuperate_detection(coord)
            #print(x, y, w, h)

            #Make a detection on a rectangle ANIMATION.
            img = open_picture(pictures.format(p_picture[nb]))
            #cv2.rectangle(img, (x, y), (w, h), (0, 0, 255), 3)
            #show_picture("rectangle detection", img, 0, "")

            #Recup sizes of the picture.
            size = img.shape
            #print(size)

            #Conversion into YOLO.
            (x, y, w, h) = convert_to_yolo_annotation(size, x, y, w, h)
            #print(x, y, w, h)

            #Write it in a .txt file.
            write_into_txt_file()

