import os
import shutil

liste = os.listdir()
doss = 0

for nb, i in enumerate(liste):
    if nb % 250 == 0:
        doss += 1
        os.makedirs(str(doss))

    shutil.move(i, str(doss) + "/" + i)
