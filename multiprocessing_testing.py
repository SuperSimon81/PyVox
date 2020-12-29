import World
#import multiprocessing
#from multiprocessing import Pool
import time
import numpy as np
import pyfastnoisesimd as fns
import random
import os
import matplotlib.pyplot as plt

if __name__ == "__main__":
    world = World.World() 
    world.m_generate_world(1)
    print("yass")
    time.sleep(10000)
    #plt.figure()
    #plt.imshow(world.chunk_dict[0,0].noise, cmap='jet')
    #plt.colorbar()
    #plt.show()


