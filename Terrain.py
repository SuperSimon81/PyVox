import multiprocessing
import numpy as np

class Terrain():
    def __init__(self,noise,chunk_position,world,chunk_width,chunk_height):
        self.chunk_width = chunk_width
        self.chunk_height = chunk_height
        self.chunk_position = chunk_position
        self.world = world
        self.is_generated = False
        self.p1 = multiprocessing.Process(target = self.generate)
        self.array = np.zeros((self.chunk_width,self.chunk_height,self.chunk_width),dtype=np.float32)
        self.noise = noise

    def start_generating(self):
        if not self.is_generated and not self.p1.is_alive():
            self.p1.start()
        
    def generate(self):
        cp = self.chunk_position
        
        for x in range(self.chunk_width):
            for z in range(self.chunk_width):
                for y in range(self.chunk_height):
                    val = (self.noise[x,z]+1)/2
                    if y > val*self.chunk_height:
                        self.array[x,y,z] = 2146688-y/self.chunk_height*2146688 
        
        self.is_generated=True
