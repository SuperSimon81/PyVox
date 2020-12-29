import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
import time
import numpy as np 
import pyfastnoisesimd as fns
from matplotlib import cm
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

noise = PerlinNoise()

tic = time.perf_counter()
       
chunk_width = 64
chunk_height = chunk_width
arr = np.zeros((chunk_width,chunk_height,chunk_width),dtype=np.float32)

shape = [64,64]
seed = np.random.randint(2**31)
N_threads = 4
perlin = fns.Noise(seed=seed, numWorkers=N_threads)
perlin.frequency = 0.05
perlin.noiseType = fns.NoiseType.Perlin
perlin.fractal.octaves = 4
perlin.fractal.lacunarity = 2.1
perlin.fractal.gain = 1
#perlin.perturb.perturbType = fns.PerturbType.NoPertrub
result = perlin.genAsGrid(shape)

for x in range(chunk_width):
    for z in range(chunk_width):
        for y in range(chunk_height):
            terrain = chunk_height * (result[x,z]+1) #(noise([x/chunk_width,z/chunk_width])+1)/2
            if terrain < y:
                arr[x,y,z] = 2146688-(y/chunk_height)*2146688
            #if self.world.generate_voxel([x+cp[0]*self.chunk_width,y,z+cp[1]*self.chunk_width])==0:
            #    

toc = time.perf_counter()
#test_memory = bgfx.copy(as_void_ptr(self.array.tobytes()), len(self.array.tobytes()))
#self.data_texture = bgfx.create_texture3d(self.chunk_width,self.chunk_height,self.chunk_width,False,bgfx.TextureFormat.R32F,BGFX_SAMPLER_POINT ,test_memory)
#print(f" {toc - tic:0.4f} seconds")
print(str.format("made chunk in {0:0.4f} s",toc-tic))
X, Y = np.meshgrid(range(64), range(64))
surf = ax.plot_surface(X,Y,result, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

#fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()
