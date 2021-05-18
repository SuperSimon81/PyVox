import os
from ctypes import Structure, c_float, c_uint32, sizeof
from pathlib import Path
#from PIL import Image 
import numpy as np
import glm 
import glfw
import bgfx as bgfx
from bgfx import * 
from bgfx import ImGuiExtra, ImGui
import sys 
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from example_window import ExampleWindow
import opensimplex
import random
import math
import Chunk
import World
import VoxelData
root_path = Path(__file__).parent

class Circxels(ExampleWindow):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.elapsed_time = 0
        self.text = ""
        self.light_info_text=""
        self.init_conf = bgfx.Init()
        self.init_conf.debug = True
        self.init_conf.resolution.width = self.width
        self.init_conf.resolution.height = self.height
        
        self.init_conf.type = bgfx.RendererType.METAL

        self.init_conf.resolution.reset = BGFX_RESET_VSYNC
        self.lastX = self.width/2
        self.lastY = self.height/2
        self.yaw = 0
        self.pitch = 0
        self.number = 0
        
        self.mouse_enabled = False

    def init(self, platform_data):
        float_size = np.dtype(np.float32).itemsize
        self.init_conf.platform_data = platform_data
        bgfx.render_frame()
        bgfx.init(self.init_conf)
        bgfx.reset(
            self.width, self.height, BGFX_RESET_VSYNC, self.init_conf.resolution.format,
        )
        glfw.set_input_mode(self.window,glfw.CURSOR,glfw.CURSOR_DISABLED)
        
        self.lastX, self.lastY, buttons_states = self.get_mouse_state()
        
      
        bgfx.set_view_clear(0, BGFX_CLEAR_COLOR | BGFX_CLEAR_DEPTH, 0x00000000, 1.0, 0)

        self.vertex_layout = bgfx.VertexLayout()
        self.vertex_layout.begin().add(bgfx.Attrib.POSITION, 3, bgfx.AttribType.FLOAT).add(bgfx.Attrib.COLOR0, 1, bgfx.AttribType.FLOAT).end() #.add(bgfx.Attrib.NORMAL, 3, bgfx.AttribType.FLOAT).add(bgfx.Attrib.COLOR1, 1, bgfx.AttribType.FLOAT).end()
        
        self.vertex_buffer = bgfx.create_dynamic_vertex_buffer(10,self.vertex_layout,BGFX_BUFFER_ALLOW_RESIZE)
        
        self.simplex = opensimplex.OpenSimplex(seed=random.randint(0,10))
        
        self.circxels = self.make_3d_case(10,0)
        for i in range(11,25):
        
            self.circxels = np.append(self.circxels,self.make_3d_case(i,i/30))
        
        vb_memory = bgfx.copy(
            as_void_ptr(self.circxels), float_size * len(self.circxels)
            )

        self.vertex_buffer2 = bgfx.create_dynamic_vertex_buffer(vb_memory, self.vertex_layout)

        
        
        
        
        # Create program from shaders.
        self.main_program = bgfx.create_program(
            load_shader(
                "circxels.VertexShader.vert", ShaderType.VERTEX, root_path=root_path
            ),
            load_shader(
                "circxels.FragmentShader.frag", ShaderType.FRAGMENT, root_path=root_path
            ),
            True,
        )
        
      
        
        ImGuiExtra.imgui_create()

        glfw.set_key_callback(self.window,self.key_event)
        
        
        self.eye_glm = glm.vec3(0,0,0)
        self.move = 0
        self.move_side = 0
        #self.make_3d_case()

    def make_2d_case(self):
        edges =4
        shapes = 4
        final = np.array([],np.float32)
        count=1
        radius=1
        counter=0
        divisions=[1,2,8,16,16,32,32,32,32,64,64,64,64,64,64,64,64,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256]

        #divisions.append(int(edges/2))
        for poly in range(1,shapes):
            points=[]
            radius = 1*count/edges
            circ=2*math.pi*radius
            segment = circ/edges
            if segment > math.pi/2:
                edges *=2
                counter +=1
            
            for edge in range(edges):
                a = (radius-1)*math.cos(math.pi/(edges/2))
                
                points.append([radius*math.sin(2*math.pi*edge/edges),radius*math.cos(2*math.pi*edge/edges),0,1])
                points.append([radius*math.sin(2*math.pi*(edge+1)/edges),radius*math.cos(2*math.pi*(edge+1)/edges),0,1])
                if count==1:
                    points.append([radius*math.sin(2*math.pi*1/edges),radius*math.cos(2*math.pi*1/edges),0,1])
                    points.append([radius*math.sin(2*math.pi),radius*math.cos(2*math.pi),0,1])
                
                #plt.plot([(a)*math.sin(2*math.pi*edge/edges),(radius)*math.sin(2*math.pi*edge/edges)],[(a)*math.cos(2*math.pi*edge/edges),(radius)*math.cos(2*math.pi*edge/edges)], 'k-', lw=0.5)
            final = np.append(final,np.asarray(points,np.float32).flatten(),0)
            count += 1
        output = np.array(final,np.float32).flatten()
        output = output.flatten()
        return output


    def make_3d_case(self,level,cutoff):
        points = []
        final = np.array([],np.float32)
        edges = 4
        divisions = [4, 8, 16, 16, 32, 32, 32, 32, 64, 64, 64, 64, 64, 64, 64, 64, 128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128]
        radiii = []
        points=[]
        
        #circ=2*math.pi*radius
        #segment = circ/edges
        #if segment > math.pi/4:
        #    edges *=2
        edges = divisions[level]
        #radius = level
        r= level
        r2= level-1
        #divs.append(edges)
        
        a = 2
        b = 2
        for theta in range(int(edges/2)):
            for rho in range(int(edges)):
                val = (self.simplex.noise2d(theta/edges/2,rho/edges/2)+1)*(level-1)
                val = random.uniform(0,1)
                if val>cutoff:
                    col = random.uniform(0.2,1)
                    #[0,0,0]
                    p0 = [r*math.sin(a*math.pi*theta/edges)*math.cos(rho/edges*b*math.pi),
                        r*math.sin(a*math.pi*theta/edges)*math.sin(rho/edges*b*math.pi),
                        r*math.cos(a*math.pi*theta/edges),col]
                    #[1,0,0]
                    p1 = [r*math.sin(a*math.pi*(theta+1)/edges)*math.cos(rho/edges*b*math.pi),
                        r*math.sin(a*math.pi*(theta+1)/edges)*math.sin(rho/edges*b*math.pi),
                        r*math.cos(a*math.pi*(theta+1)/edges),col]
                    #[1,1,0]
                    p2 = [r*math.sin(a*math.pi*(theta+1)/edges)*math.cos((rho+1)/edges*b*math.pi),
                        r*math.sin(a*math.pi*(theta+1)/edges)*math.sin((rho+1)/edges*b*math.pi),
                        r*math.cos(a*math.pi*(theta+1)/edges),col]
                    #[0,1,0]
                    p3 = [r*math.sin(a*math.pi*theta/edges)*math.cos((rho+1)/edges*b*math.pi),
                        r*math.sin(a*math.pi*theta/edges)*math.sin((rho+1)/edges*b*math.pi),
                        r*math.cos(a*math.pi*theta/edges),col]
                    #[0,0,1]
                    p4 = [r2*math.sin(a*math.pi*theta/edges)*math.cos(rho/edges*b*math.pi),
                        r2*math.sin(a*math.pi*theta/edges)*math.sin(rho/edges*b*math.pi),
                        r2*math.cos(a*math.pi*theta/edges),col]
                    #[1,0,1]
                    p5 = [r2*math.sin(a*math.pi*(theta+1)/edges)*math.cos(rho/edges*b*math.pi),
                        r2*math.sin(a*math.pi*(theta+1)/edges)*math.sin(rho/edges*b*math.pi),
                        r2*math.cos(a*math.pi*(theta+1)/edges),col]
                    #[1,1,1]
                    p6 = [r2*math.sin(a*math.pi*(theta+1)/edges)*math.cos((rho+1)/edges*b*math.pi),
                        r2*math.sin(a*math.pi*(theta+1)/edges)*math.sin((rho+1)/edges*b*math.pi),
                        r2*math.cos(a*math.pi*(theta+1)/edges),col]
                    #[0,1,1]
                    p7 = [r2*math.sin(a*math.pi*theta/edges)*math.cos((rho+1)/edges*b*math.pi),
                        r2*math.sin(a*math.pi*theta/edges)*math.sin((rho+1)/edges*b*math.pi),
                        r2*math.cos(a*math.pi*theta/edges),col]
                    
                    vertices = [p0,p1,p2,p3,p4,p5,p6,p7]
                    
                    #top 
                    for p in range(6):
                    
                        points.append(vertices[VoxelData.triangles[p,0]])
                        points.append(vertices[VoxelData.triangles[p,1]])
                        points.append(vertices[VoxelData.triangles[p,2]])

                        points.append(vertices[VoxelData.triangles[p,2]])
                        points.append(vertices[VoxelData.triangles[p,1]])
                        points.append(vertices[VoxelData.triangles[p,3]])
                        #print(len(points))
                
                lines = """
                points.append(p0)    
                points.append(p1)

                points.append(p1)
                points.append(p2)

                points.append(p2)
                points.append(p3)
                
                points.append(p3)
                points.append(p0)


                points.append(p4)    
                points.append(p5)

                points.append(p5)
                points.append(p6)

                points.append(p6)
                points.append(p7)
                
                points.append(p7)
                points.append(p4)

                points.append(p4)    
                points.append(p0)

                points.append(p5)
                points.append(p1)

                points.append(p6)
                points.append(p2)
                
                points.append(p7)
                points.append(p3)"""

                

        #divisions.append(int(edges/2))
            final = np.append(final,np.asarray(points,np.float32).flatten(),0)
           
        output = np.array(final,np.float32).flatten()
        output = output.flatten()
        #print(divs)
        return output
          
    def key_event(self,window,key,scancode,action,mods):
        self.key=key
        
        if key == glfw.KEY_W:
            if action == glfw.PRESS:
                self.move = 0.01
            if action == glfw.RELEASE:
                self.move = 0
                
        if key == glfw.KEY_S:
            if action == glfw.PRESS:
                self.move = -0.01
            if action == glfw.RELEASE:
                self.move = 0
       
        if key == glfw.KEY_D:
            if action == glfw.PRESS:
                self.move_side  = 1
            if action == glfw.RELEASE:
                self.move_side  = 0
        if key == glfw.KEY_A:
            if action == glfw.PRESS:
                self.move_side  = -1
            if action == glfw.RELEASE:
                self.move_side  = 0

        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            if(self.mouse_enabled):
                self.lastX =self.width / 2
                self.lastY =self.height / 2
                glfw.set_cursor_pos(self.window, self.width / 2, self.height / 2)
                glfw.set_input_mode(self.window,glfw.CURSOR,glfw.CURSOR_DISABLED)
                self.mouse_enabled = False
            else:
                glfw.set_cursor_pos(self.window, self.width / 2, self.height / 2)
                glfw.set_input_mode(self.window,glfw.CURSOR,glfw.CURSOR_NORMAL)
                self.mouse_enabled = True
                
        

    def shutdown(self):
        ImGuiExtra.imgui_destroy()
        
        bgfx.shutdown()

    def update(self, dt):
        float_size = np.dtype(np.float32).itemsize
        #glfw.set_cursor_pos(self.window, self.width / 2, self.height / 2);
        self.elapsed_time += dt
        self.mouse_x, self.mouse_y, buttons_states = self.get_mouse_state()
        ImGuiExtra.imgui_begin_frame(
            int(self.mouse_x), int(self.mouse_y), buttons_states, 0, self.width, self.height
        )
        #last_x = self.mouse_x
        #last_y = self.mouse_y
        self._imgui_panel()
        
        ImGuiExtra.imgui_end_frame()
        up_glm = (0,-1,0)  
        
        if(not self.mouse_enabled):
            xoffset = self.mouse_x - self.lastX
            yoffset = self.lastY - self.mouse_y
            self.lastX = self.mouse_x
            self.lastY = self.mouse_y

            self.yaw   += xoffset*0.5
            self.pitch += yoffset*0.5
            if self.pitch > 89:
                self.pitch =  89.0
            if self.pitch < -89:
                self.pitch = -89
        
        self.direction = glm.vec3(0,0,0)
        self.direction.x = math.cos(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch));
        self.direction.y = math.sin(glm.radians(self.pitch));
        self.direction.z = math.sin(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch));
        self.direction = glm.normalize(self.direction)
        self.eye_glm += self.move*self.direction
        self.eye_glm += self.move_side*(glm.cross(self.direction,up_glm)) 
        

        self.text = str.format("y:{0} p:{1} x:{2} y:{3} z:{4}",round(self.yaw),round(self.pitch),round(self.eye_glm.x),round(self.eye_glm.y),round(self.eye_glm.z))
        #view_glmlh = glm.lookAtRH(glm.vec3(self.eye_glm),glm.vec3(self.eye_glm+self.direction),glm.vec3(up_glm))
        view_glmlh = glm.lookAtRH(glm.vec3(self.eye_glm),glm.vec3(0,0,0),glm.vec3(up_glm))
        
        proj_glmlh = glm.perspectiveRH(20, self.width / self.height, 1, 100.0)
        
        bgfx.set_view_transform(0, as_void_ptr(glm.value_ptr(view_glmlh)), as_void_ptr(glm.value_ptr(proj_glmlh)))
        bgfx.set_view_rect(0, 0, 0, self.width, self.height)
        
        model_matrix = glm.rotate(glm.mat4x4(),math.pi/2,glm.vec3(1,0,0))
        
        model_matrix = glm.rotate(model_matrix,self.elapsed_time/2,glm.vec3(0,0,1))
        
        #model_matrix = glm.rotate(glm.mat4x4(),self.elapsed_time,glm.vec3(self.elapsed_time/2,self.elapsed_time/3,self.elapsed_time/2))
        self.model_matrix = model_matrix
        bgfx.set_transform(as_void_ptr(glm.value_ptr(model_matrix)), 1)
        
         #bgfx.update(self.vertex_buffer,0,vb_memory)

        # Set vertex and index buffer.
        bgfx.set_state(0
            #| BGFX_STATE_PT_LINES
            | BGFX_STATE_WRITE_RGB 
            #| BGFX_STATE_WRITE_A 
            | BGFX_STATE_WRITE_Z
            | BGFX_STATE_DEPTH_TEST_LESS
            | 0,
        )
    
        bgfx.set_vertex_buffer(0, self.vertex_buffer2, 0, 10000000)
        self.number += 1
        bgfx.submit(0, self.main_program, 0, False)

        bgfx.frame()

    def resize(self, width, height):
        bgfx.reset(
            self.width, self.height, BGFX_RESET_VSYNC, self.init_conf.resolution.format
        )

    def _imgui_panel(self):
        ImGui.set_next_window_pos(
            ImGui.Vec2(self.width - self.width / 5.0 - 10.0, 10.0), 1 << 2
        )
        ImGui.set_next_window_size(
            ImGui.Vec2(self.width / 5.0, self.height / 3.5), 1 << 2
        )
        ImGui.begin("Info panel")

        ImGui.text(self.text)
        
        ImGui.end()

    def color2float(self,color): 
        c_precision = 128.0
        c_precisionp1 = c_precision + 1.0
        
        return math.floor(color[0] * c_precision + 0.5) + math.floor(color[1] * c_precision + 0.5) * c_precisionp1 + math.floor(color[2] * c_precision + 0.5) * c_precisionp1 * c_precisionp1

if __name__ == "__main__":
    textures = Circxels(1280, 1280, "Circxels")
    textures.run()
