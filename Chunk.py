
import bgfx
from bgfx import * 
import numpy as np
from ctypes import Structure, c_float, c_uint32, sizeof
import VoxelData
import time

class Chunk():
    def __init__(self,chunk_position,world,chunk_width,chunk_height):
        self.world_position = chunk_position * chunk_width + [chunk_width/2, chunk_width/2]
        self.chunk_width = chunk_width
        self.chunk_height = chunk_height
        self.chunk_position = chunk_position
        self.world = world
        self.data_texture = 0
        self.is_visible = False
        self.is_generated = False
        self.vertices = []
        
        
        #self.process = multiprocessing.Process(target=self.m_generate_chunk,args=(noise,)) 
        
    def load_chunk(self,filename):
        chunk_arr = np.load(filename,allow_pickle=True)
        self.array = chunk_arr[0]
        self.chunk_position =  chunk_arr[1]
        print(str.format("loaded chunk {0}",chunk_arr[1]))
        self.is_generated = True

    def m_gen(self):
        if not self.process.is_alive() and not self.is_generated:
            self.process.start()

    

    #def generate_chunk(self):
        #self.populate_chunk()
        #asyncio.run(self.populate_chunk())
        #self.is_generated=True

    def populate_chunk(self):
        self.array = np.zeros((self.chunk_width+2,self.chunk_height,self.chunk_width+2),dtype=np.float32)
        cp = self.chunk_position
        tic = time.perf_counter()
        
        
        for x in range(-1,self.chunk_width+1):
            for z in range(-1,self.chunk_width+1):
                for y in range(self.chunk_height):
                    #val = self.noise[x,z]
                    
                    val = (self.world.simplex.noise2d((self.chunk_position[0]*self.chunk_width+x-1)/10,(self.chunk_position[1]*self.chunk_width+z-1)/10)+1)/2
                    #val += (self.world.simplex2.noise2d((self.chunk_position[0]*self.chunk_width+x)/5,(self.chunk_position[1]*self.chunk_width+z)/5)+1)/4
                    
                    
                    if y > val*self.chunk_height:
                        col = y/self.chunk_height
                        self.array[x+1,y,z+1] = self.rgb_to_float((0,1,1),256) - self.rgb_to_float((0,col,col),256)
                        #print(col)
                    #if self.world.generate_voxel([x+cp[0]*self.chunk_width,y,z+cp[1]*self.chunk_width])==0:
        toc = time.perf_counter()
        self.is_generated=True
        print(str.format("made chunk {0} {1} as {2}x{2}x{3} in {4:0.4f} s",cp[0],cp[1],self.chunk_width,self.chunk_height,toc-tic))
        #self.data_uniform = bgfx.create_uniform("s_data",  bgfx.UniformType.SAMPLER)

    def bgfx_init(self):
        self.vertex_layout = bgfx.VertexLayout()
        self.vertex_layout.begin().add(
              bgfx.Attrib.POSITION, 3, bgfx.AttribType.FLOAT
        ).add(bgfx.Attrib.COLOR0, 1, bgfx.AttribType.FLOAT).end()
        self.counter_buffer = bgfx.create_dynamic_index_buffer(1, BGFX_BUFFER_INDEX32 | BGFX_BUFFER_COMPUTE_READ_WRITE);
        self.vertex_buffer = bgfx.create_dynamic_vertex_buffer(1000000, self.vertex_layout ,BGFX_BUFFER_COMPUTE_READ_WRITE | BGFX_BUFFER_ALLOW_RESIZE)
        test_memory = bgfx.copy(as_void_ptr(self.array.tobytes()), len(self.array.tobytes()))
        self.data_texture = bgfx.create_texture3d(self.chunk_width+2,self.chunk_height,self.chunk_width+2,False,bgfx.TextureFormat.R32F,BGFX_SAMPLER_POINT ,test_memory)

    def get_vertices(self):
        self.clear_mesh()
        for x in range(self.chunk_width):
            for z in range(self.chunk_width):
                for y in range(self.chunk_height):
                    self.update_mesh(np.array([x,y,z]))
        return np.asarray(self.vertices).flatten().flatten()

    def clear_mesh(self):
        self.vertices = []

    def update_mesh(self,pos):
        for i,face in enumerate(VoxelData.facechecks):
            col = self.array[pos[0],pos[1],pos[2]]
            #print(col)
            
            if col>0:
                #print(col)
                if not self.check_voxel(pos + face):
                    
                    #vertex = np.array(pos + VoxelData.vertices[VoxelData.triangles[i,0]],np.float32)

                    po = pos + VoxelData.vertices[VoxelData.triangles[i,0]]
                    arr = np.array([po[0],po[1],po[2],col],np.float32) 
                    self.vertices.append(arr)

                    po = pos + VoxelData.vertices[VoxelData.triangles[i,1]]
                    arr = np.array([po[0],po[1],po[2],col],np.float32) 
                    self.vertices.append(arr)

                    po = pos + VoxelData.vertices[VoxelData.triangles[i,2]]
                    arr = np.array([po[0],po[1],po[2],col],np.float32) 
                    self.vertices.append(arr)

                    po = pos + VoxelData.vertices[VoxelData.triangles[i,2]]
                    arr = np.array([po[0],po[1],po[2],col],np.float32) 
                    self.vertices.append(arr)

                    po = pos + VoxelData.vertices[VoxelData.triangles[i,1]]
                    arr = np.array([po[0],po[1],po[2],col],np.float32) 
                    self.vertices.append(arr)

                    po = pos + VoxelData.vertices[VoxelData.triangles[i,3]]
                    arr = np.array([po[0],po[1],po[2],col],np.float32) 
                    self.vertices.append(arr)

    def check_voxel(self,pos):
        if self.array[pos[0],pos[1],pos[2]]>0:
            return True
        else:
            return False
   
    def rgb_to_float(self,rgb,scale):
        return rgb[0] + (rgb[1]/scale)+ (rgb[2]/(scale*scale))
