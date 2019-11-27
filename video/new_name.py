import os

liste = os.listdir()

c = 2987

for i in liste:
    os.rename(i, str(c) + ".jpg")

    c += 1
