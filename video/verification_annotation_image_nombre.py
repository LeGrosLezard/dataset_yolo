import os


liste1 = os.listdir("annotations")
liste2 = os.listdir("image")


for i in liste2:

    for j in liste1:
        if j[:-12] == i:

            a = os.listdir("annotations" + "/" + j)
            b = os.listdir("image" + "/" + i)
            if len(a) != len(b):
                print(i, j, len(a), len(b))
                print("")
