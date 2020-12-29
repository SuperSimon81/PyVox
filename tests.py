import math
import glm 
import numpy as np


count=0
arr = np.zeros((64*64*64,3),np.uint8)

for x in range(64):
    print(x)
    for y in range(64):
        for z in range(64):
                arr[count]=[x,y,z]