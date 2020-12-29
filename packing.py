import numpy as np
from PIL import Image
import math
import glm
import VoxelData
def vec3_to_float(arr):
    packedColor = (arr[0] << 16) | (arr[1] << 8) | arr[2]
    return packedColor


#UnPack 3 values from 1 float
def float_to_vec3(src):
    ## Unpack to the 0-255 range
    r = math.floor(src/65536);
    g = math.floor(math.fmod(src, 65536)/256);
    b = math.fmod(src, 256);

    return np.array([r,g,b])


vec = np.array(VoxelData.facechecks[1]+[1,1,1],np.uint8)
flot = vec3_to_float(vec)
back = float_to_vec3(flot)
print(vec)
print(back)

