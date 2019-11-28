import os
import shutil





direction_image = "1"
direction = "1_annotations"
liste = os.listdir(direction)

for i in liste:

    c = 0
    with open(direction + "/" + i, "r") as file:
        for f in file:
            c += 1

    if c == 10:
        shutil.move(direction + "/" + i, "ici/" + i)
        shutil.move(direction_image + "/" + i[:-4] + ".jpg", "ici/" + i[:-4] + ".jpg")

        print("moved")
