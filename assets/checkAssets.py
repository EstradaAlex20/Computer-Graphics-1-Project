from os import listdir
from os.path import isfile, join
arr = listdir()


f = open("about.txt","w")
for i in arr:
    f.write(i + " = \n")
