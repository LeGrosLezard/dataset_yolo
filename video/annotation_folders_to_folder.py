import shutil
import os

liste = os.listdir()
for i in liste:
    print(i)
    if i in ("main.py", "generate_xml.py", "make_annotation.py"):
        pass
    else:
        liste_i = os.listdir(i)
        for j in liste_i:
            print(j)
            shutil.move(i + "/" + j, r"C:\Users\jeanbaptiste\Desktop\darkflow-master\hand_model\image\{}".format(j))

