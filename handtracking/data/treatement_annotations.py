""" We load .mat file, we recuperate points into list from the .mat file,
we recuperate min(x;y) max(x;y) for the detection,  we display it on picture ANIMATION,
we convert it into YOLO annotations, we write it into a .txt file."""

#For run folder
import os
#For have a visual
import cv2
#For load .mat file
import scipy
from scipy.io import loadmat
#For have a visual
from picture_operation import open_picture, show_picture
#Paths for folder.
from paths import path_annotation, annotations, path_picture,\
                  pictures, path_txt_annotation


def recuperate_points(points):
    """From annotation recuperate points of hands.
    One list for one hand. Ignore Right and Left informations"""

    #Sometimes we have only one hand.
    if len(points["boxes"][0]) >= 2:
        coordinates = [[j[0].tolist() for i in points["boxes"][0][0]\
                        for j in i[0] if j.tolist() not in (["R"], ["L"], [])],
                       [j[0].tolist() for i in points["boxes"][0][1]\
                        for j in i[0] if j.tolist() not in (["R"], ["L"], [])]]
    else:
        coordinates = [[j[0].tolist() for i in points["boxes"][0][0]\
                        for j in i[0] if j.tolist() not in (["R"], ["L"], [])]]

    return coordinates


def recuperate_detection(coordinates):
    """Recuperate rectangle of detections via min and max (x; y)"""

    detection = [[i[1] for i in coordinates],
                 [i[0] for i in coordinates]]

    return int(min(detection[0])), int(min(detection[1])),\
           int(max(detection[0])), int(max(detection[1]))


def convert_to_yolo_annotation(size, x, y, w, h):
    """https://github.com/ManivannanMurugavel/Yolo-Annotation-Tool-New-/blob/master/main.py"""

    x = (x + w)/2.0; y = (y + h)/2.0
    w = w - x; h = h - y
    x = x*1./size[0]; w = w*1./size[0]
    y = y*1./size[1]; h = h*1./size[1]

    return x, y, w, h


def write_into_txt_file(coordinate, picture, path_txt):
    """Writte data into txt. if coordinate is the second add \n
    if it's the last position don't add space"""

    with open(path_txt.format(picture[:-4]), "a") as file:
        for nb, coords in enumerate(coordinate):
            if nb >= 1:file.write("\n")
            for pos, coord in enumerate(coords):
                if pos in (0, 1, 2):file.write(str(coord) + " ")
                else:file.write(str(coord))


if __name__ == "__main__":

    #Make list of folder.
    p_annotation = os.listdir(path_annotation)
    p_picture = os.listdir(path_picture)

    for nb in range(len(p_annotation)):

        #Load .mat file.
        points = scipy.io.loadmat(annotations.format(p_annotation[nb]))

        #Recuperate annotations from .mat.
        coordinates = recuperate_points(points)

        coords = []
        for coord in coordinates:

            #Recuperate detection.
            x, y, w, h = recuperate_detection(coord)

            #Make a detection on a rectangle ANIMATION.
            img = open_picture(pictures.format(p_picture[nb]))
            cv2.rectangle(img, (x, y), (w, h), (0, 0, 255), 3)
            show_picture("detection", img, 0, "")

            #Conversion into YOLO and add it to a list.
            coords.append([convert_to_yolo_annotation(img.shape, x, y, w, h)][0])

        #Write it in a .txt file.
        write_into_txt_file(coords, p_picture[nb], path_txt_annotation)
