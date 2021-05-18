import World
import multiprocessing
#from multiprocessing import Pool
import time
import numpy as np
import pyfastnoisesimd as fns
import random
import os
import matplotlib.pyplot as plt
 
 #q = mp.Queue()

if __name__ == "__main__":
    world = World.World(1) 
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=world.foo, args=(q,[0,0]))
    p.start()
    p = multiprocessing.Process(target=world.foo, args=(q,[1,0]))
    p.start()
    p = multiprocessing.Process(target=world.foo, args=(q,[0,1]))
    p.start()
    p = multiprocessing.Process(target=world.foo, args=(q,[-1,0]))
    p.start()
    p = multiprocessing.Process(target=world.foo, args=(q,[0,-1]))
    p.start()
    
    
    
    print("yass")
    

    for i in range(20):
        time.sleep(1)
        #print(len(world.chunk_dict))
        print(i)
        if not q.empty:
            print("not empty")
            print(q.get())
        else:
            print("empty")
    
    #world.join()

    
   # world.m_generate_chunk(2,2)
   # for i in range(10):
   #     time.sleep(1)
   #     print(len(world.chunk_dict))
    
    #plt.figure()
    #plt.imshow(world.chunk_dict[0,0].noise, cmap='jet')
    #plt.colorbar()
    #plt.show()


