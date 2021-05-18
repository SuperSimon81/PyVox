
#import multiprocessing
#from multiprocessing import Pool
import time
import numpy as np
import pyfastnoisesimd as fns
import random
import os
import matplotlib.pyplot as plt
import multiprocessing as mp
import sys 
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import World
import Chunk
import opensimplex

def foo(pos,simplex):    
    chunk_width = 64
    chunk_height = 64
    chunk_position = pos
    chunk = Chunk.Chunk(chunk_position,chunk_width,chunk_height)
    #array = np.zeros((chunk_width+2,chunk_height,chunk_width+2),dtype=np.float32)
    for x in range(-1,chunk_width+1):
            for z in range(-1,chunk_width+1):
                for y in range(chunk_height):
                    val = (simplex.noise2d((chunk_position[0]*chunk_width+x-1)/10,(chunk_position[1]*chunk_width+z-1)/10)+1)/2
                    if y > val*chunk_height:
                        col = y/chunk_height
                        chunk.array[x+1,y,z+1] = col 
    chunk.is_generated = True  
    print(str.format("made chunk {0} {1} as {2}x{2}x{3}",pos[0],pos[1],chunk.chunk_width,chunk.chunk_height))
    return chunk  

if __name__ == '__main__':
    simplex = opensimplex.OpenSimplex(seed=random.randint(0,10))
    world = World.World(1) 
    tic = time.perf_counter()
    list = []
    pool = mp.Pool(3)
    for x in range(-2,2):
        for z in range(-2,2):
            world.go([x,z])
            #list.append(pool.apply_async(foo,([x,z],simplex)))
    
    print("start!")
    
    while(len(world.proclist)>0):
        if(world.proclist[world.proclist.list()[0]].ready()):
            
            print(world.proclist[world.proclist.list()[0]]._value.chunk_position)
            print(world.proclist[world.proclist.list()[0]]._value.is_generated)
            tupp = (world.proclist[world.proclist.list()[0]]._value.chunk_position[0],world.proclist[0]._value.chunk_position[1])
            world.chunk_dict[tupp]=world.proclist[world.proclist.list()[0]]._value
            del world.proclist[world.proclist.list()[0]]
    
    pool.close()
    toc = time.perf_counter()
    print(str.format("all done in {0}",toc-tic))
    print("anything else?")
       
    
