import cv2

import scipy
from scipy.io import loadmat

from picture_operation import open_picture
from picture_operation import show_picture
from picture_operation import make_rectangle

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

    detection = [[i[1] for i in coordinates[nb]],
                 [i[0] for i in coordinates[nb]]]

    points = int(min(detection[0])), int(min(detection[1])),\
             int(max(detection[0])), int(max(detection[1]))

    return points





if __name__ == "__main__":

    path_anno = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\handtracking\data\annotation\{}"
    picture = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\handtracking\data\Buffy_1.jpg"

    #ouverture fichier .mat
    points = scipy.io.loadmat(path_anno.format("Buffy_1.mat"))
    
    coordinates = recuperate_points(points)

    for nb in range(len(coordinates)):
        (x, y, w, h) = recuperate_detection(coordinates)

        make_rectangle(picture, x, y, w, h)



























