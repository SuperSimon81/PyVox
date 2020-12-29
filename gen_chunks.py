import World
import numpy as np
import datetime

world = World.World() 
world.generate_world(25,5)
world_arr = np.array([world.chunk_width,world.chunk_height,world.seed,world.perlin.frequency,world.perlin.fractal.octaves, world.perlin.fractal.gain])
np.save(str.format("./voxels on GPU/world/world.{0}.npy",datetime.datetime.now()),world_arr) 
for chunk in world.chunk_list:
   # with open( as f: 
    
    np.save(str.format("./voxels on GPU/world/chunk.{0}.{1}.npy",chunk.chunk_position[0],chunk.chunk_position[1]),np.array([chunk.array,chunk.chunk_position],np.object),allow_pickle=True)


print("i did it ")

