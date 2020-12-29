import noise
import math
import Chunk
#import perlin_noise
import numpy as np
#import pyfastnoisesimd as fns
import os 

import random
import opensimplex
import time
class World():
    def __init__(self):
        self.chunk_width =64
        self.chunk_height = 64
        self.chunk_dict = {}
        #self.noise = perlin_noise.PerlinNoise()
       
        self.view_distance = 1
       # self.pool = Pool(1)
     
        self.simplex = opensimplex.OpenSimplex(seed=random.randint(0,10))
        #self.simplex2 = opensimplex.OpenSimplex(seed=random.randint(0,10))

    
    def generate_world(self,size):
        for i in range(-size,size):
            for j in range(-size,size):
                chunk = Chunk.Chunk([i,j],self,self.chunk_width,self.chunk_height)
                chunk.populate_chunk()
                self.chunk_dict[(i,j)]=chunk


    def generate_chunk(self,i,j):
        chunk = Chunk.Chunk([i,j],self,self.chunk_width,self.chunk_height)
        chunk.populate_chunk()
        self.chunk_dict[(i,j)]=chunk


    def m_generate_world(self,size):
        for i in range(-size,size):
            for j in range(-size,size):
                chunk = Chunk.Chunk([i,j],self,self.chunk_width,self.chunk_height)
                self.pool.map(self.m_populate_chunk,(chunk,))
                self.chunk_dict[(i,j)]=chunk


    def m_populate_chunk(self,chunk):
        chunk.array = np.zeros((chunk.chunk_width+2,chunk.chunk_height,chunk.chunk_width+2),dtype=np.float32)
        cp = chunk.chunk_position
        tic = time.perf_counter()

        for x in range(-1,chunk.chunk_width+1):
            for z in range(-1,chunk.chunk_width+1):
                for y in range(chunk.chunk_height):
                    #val = self.noise[x,z]
                    
                    val = (self.simplex.noise2d((chunk.chunk_position[0]*chunk.chunk_width+x-1)/10,(chunk.chunk_position[1]*chunk.chunk_width+z-1)/10)+1)/2
                    #val += (self.world.simplex2.noise2d((self.chunk_position[0]*self.chunk_width+x)/5,(self.chunk_position[1]*self.chunk_width+z)/5)+1)/4
                    
                    
                    if y > val*chunk.chunk_height:
                        col = y/chunk.chunk_height
                        chunk.array[x+1,y,z+1] = chunk.rgb_to_float((0,1,0),256) - chunk.rgb_to_float((0,col,0),256)
                        #print(col)
                    #if self.world.generate_voxel([x+cp[0]*self.chunk_width,y,z+cp[1]*self.chunk_width])==0:
        toc = time.perf_counter()
        chunk.is_generated=True
        print(str.format("made chunk {0} {1} as {2}x{2}x{3} in {4:0.4f} s",cp[0],cp[1],chunk.chunk_width,chunk.chunk_height,toc-tic))
        #self.data_uniform = bgfx.create_uniform("s_data",  bgfx.UniformType.SAMPLER)
