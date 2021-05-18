import noise
import math
import Chunk
#import perlin_noise
import numpy as np
#import pyfastnoisesimd as fns
import os 
import multiprocessing
from multiprocessing import Manager
import random
import opensimplex
import time
class World():
    def __init__(self,size):
        self.chunk_width =64
        self.chunk_height = 64
        #self.chunk_dict = {}
        #self.noise = perlin_noise.PerlinNoise()
        #manager = multiprocessing.Manager()
        self.chunk_dict = {}
        self.view_distance = 2
        self.pool=multiprocessing.Pool(3)
        self.size = size
        self.simplex = opensimplex.OpenSimplex(seed=random.randint(0,10))
        self.proclist = []
        self.process_dictionary = {}

    def go(self,pos):
        #self.proclist.append(self.pool.apply_async(self.foo,(pos,self.simplex)))
         
        self.process_dictionary[(pos[0],pos[1])]=self.pool.apply_async(self.foo,(pos,self.simplex))
    
    
    def harvest(self):
       
        if len(self.process_dictionary)>0:
            first_key = next(iter(self.process_dictionary.keys()))
            if self.process_dictionary[first_key].ready():
                tupp = (self.process_dictionary[first_key]._value.chunk_position[0],self.process_dictionary[first_key]._value.chunk_position[1])
                self.chunk_dict[tupp]=self.process_dictionary[first_key]._value
                del self.process_dictionary[first_key]


    @staticmethod
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
        #print(str.format("made chunk {0} {1} as {2}x{2}x{3}",pos[0],pos[1],chunk.chunk_width,chunk.chunk_height))
        return chunk  

    