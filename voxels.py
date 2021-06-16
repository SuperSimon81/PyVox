import os
from ctypes import Structure, c_float, c_uint32, sizeof
from pathlib import Path
import numpy as np
import glm 
import glfw
import bgfx as bgfx
from bgfx import * 
from bgfx import ImGuiExtra, ImGui

from example_window import ExampleWindow

import random
import math
import Chunk
import World


root_path = Path(__file__).parent
class Textures(ExampleWindow):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.elapsed_time = 0
        self.text = ""
        self.light_info_text=""
        self.init_conf = bgfx.Init()
        self.init_conf.debug = True
        self.init_conf.resolution.width = self.width
        self.init_conf.resolution.height = self.height
        self.visible_chunks = {}
        self.init_conf.type = bgfx.RendererType.METAL

        self.init_conf.resolution.reset = BGFX_RESET_VSYNC
        self.lastX = self.width/2
        self.lastY = self.height/2
        self.yaw = 0
        self.pitch = 60
        self.light_x = ImGui.Float()  
        self.light_y = ImGui.Float()  
        self.light_z = ImGui.Float() 
        self.light_x.value = 0
        self.light_y.value = 50
        self.light_z.value = 0
        
        self.mouse_enabled = False

    def init(self, platform_data):
        float_size = np.dtype(np.float32).itemsize
        self.init_conf.platform_data = platform_data
        bgfx.render_frame()
        bgfx.init(self.init_conf)
        bgfx.reset(
            self.width, self.height, BGFX_RESET_VSYNC, self.init_conf.resolution.format,
        )

        caps = bgfx.Caps()

        glfw.set_input_mode(self.window,glfw.CURSOR,glfw.CURSOR_DISABLED)
        
        self.lastX, self.lastY, buttons_states = self.get_mouse_state()
        
        bgfx.set_view_clear(0, BGFX_CLEAR_COLOR | BGFX_CLEAR_DEPTH, 0x00000000, 1.0, 0)

        self.vertex_layout = bgfx.VertexLayout()
        self.vertex_layout.begin().add(bgfx.Attrib.POSITION, 3, bgfx.AttribType.FLOAT).add(bgfx.Attrib.COLOR0, 1, bgfx.AttribType.FLOAT).end() #.add(bgfx.Attrib.NORMAL, 3, bgfx.AttribType.FLOAT).add(bgfx.Attrib.COLOR1, 1, bgfx.AttribType.FLOAT).end()
        
        # Create program from shaders.
        self.main_program = bgfx.create_program(
            load_shader(
                "voxels.VertexShader.vert", ShaderType.VERTEX, root_path=root_path
            ),
            load_shader(
                "voxels.FragmentShader.frag", ShaderType.FRAGMENT, root_path=root_path
            ),
            True,
        )
        
        self.cs_program = bgfx.create_program(
            load_shader(
                "meshmaker.comp", ShaderType.COMPUTE, root_path=root_path
            ),True)

        #This is needed for the atomic counter making sure the meshmaker writes properly to the vertex buffers
        self.reset_counter = bgfx.create_program(
            load_shader(
                "reset_counter.comp",ShaderType.COMPUTE, root_path=root_path
            ),True)
        
        ImGuiExtra.imgui_create()

        glfw.set_key_callback(self.window,self.key_event)
        
        self.world = World.World(1) 
        
        #Offset stores chunkposition for the meshing compute shader
        self.offset_uniform = bgfx.create_uniform("_offset",bgfx.UniformType.VEC4)
        #Data is the 3D texture sent to compute shader for meshing
        self.data_uniform = bgfx.create_uniform("s_data",  bgfx.UniformType.SAMPLER)
        
        #fog uniforms for fragment shader
        self.fog_color_uniform = bgfx.create_uniform("_fog_color",bgfx.UniformType.VEC4)
        self.eye_pos_uniform = bgfx.create_uniform("_eye_pos",bgfx.UniformType.VEC4)
        self.light_uniform = bgfx.create_uniform("_light",bgfx.UniformType.VEC4)
        
        bgfx.set_uniform(self.light_uniform,as_void_ptr((c_float * 4)(self.light_x.value, self.light_y.value,self.light_z.value,1)))
   
        bgfx.set_uniform(self.fog_color_uniform,as_void_ptr((c_float * 4)(0.01, 0.1,0.01,1)))
   
        for chunk in self.world.chunk_dict.values():
            self.generate_mesh(chunk)
        
        self.eye_glm = glm.vec3(0,-50,0)
        self.move = 0
        self.move_side = 0
        
        self.chunk_pos_x=0
        self.chunk_pos_z=0
        

    def check_viewdistance(self):
        view_distance = self.world.view_distance
        new_pos_x = math.floor(self.eye_glm.z/self.world.chunk_width)
        new_pos_z = math.floor(self.eye_glm.x/self.world.chunk_width)
        self.chunk_pos_x=new_pos_x
        self.chunk_pos_z=new_pos_z

        self.world.harvest()
        for x in range(new_pos_x-view_distance,new_pos_x+view_distance):
            for z in range(new_pos_z-view_distance,new_pos_z+view_distance):
                if not (x,z) in self.world.chunk_dict.keys(): 
                    if not (x,z) in self.world.process_dictionary.keys():
                        self.text = str.format("gonna make: {0} {1} you are at: {2} {3}",x,z,new_pos_x,new_pos_z)
                       
                        #print(str.format("gonna make chunk {0} {1}",x,z))
                        #print(str.format("enqueing: {0} {1}",x,z))
                        self.world.go([x,z])
                else: 
                    if not (x,z) in self.visible_chunks and self.world.chunk_dict[(x,z)].is_generated:
                        #print(str.format("gonna make mesh: {0} {1}",x,z))
                        self.generate_mesh(self.world.chunk_dict[(x,z)])
        
        for x in range(new_pos_x-view_distance,new_pos_x+view_distance):
            self.visible_chunks.pop((x,new_pos_z-view_distance-1), None)
            self.visible_chunks.pop((x,new_pos_z+view_distance+1), None)
            self.visible_chunks.pop((x,new_pos_z-view_distance-2), None)
            self.visible_chunks.pop((x,new_pos_z+view_distance+2), None)
        
        for z in range(new_pos_z-view_distance,new_pos_z+view_distance):
            self.visible_chunks.pop((new_pos_x-view_distance-1,z), None)
            self.visible_chunks.pop((new_pos_x+view_distance+1,z), None)
            self.visible_chunks.pop((new_pos_x-view_distance-2,z), None)
            self.visible_chunks.pop((new_pos_x+view_distance+2,z), None)
            
    def generate_mesh(self,chunk):
        if(chunk.is_generated):
            chunk.bgfx_init()
            cp = chunk.chunk_position
            #Reset counter 
            bgfx.set_buffer(0,chunk.counter_buffer,bgfx.Access.READ_WRITE)
            bgfx.dispatch(0, self.reset_counter, 1,1)
            test = np.array([cp[1]*chunk.chunk_width,0,cp[0]*chunk.chunk_width,0],np.float32)
            bgfx.set_uniform(self.offset_uniform,as_void_ptr((c_float * 4)(test[0], test[1],test[2],test[3])))
            bgfx.set_buffer(0,chunk.vertex_buffer,bgfx.Access.WRITE)
            bgfx.set_buffer(1,chunk.counter_buffer,bgfx.Access.READ_WRITE)
            bgfx.set_texture(2,self.data_uniform,chunk.data_texture)
            bgfx.dispatch(0, self.cs_program, chunk.chunk_width,chunk.chunk_height,chunk.chunk_width)
            self.visible_chunks[(chunk.chunk_position[0],chunk.chunk_position[1])] = chunk
            chunk.is_visible = True
            

    def key_event(self,window,key,scancode,action,mods):
        self.key=key
        
        if key == glfw.KEY_W:
            if action == glfw.PRESS:
                self.move = 0.5
            if action == glfw.RELEASE:
                self.move = 0
                
        if key == glfw.KEY_S:
            if action == glfw.PRESS:
                self.move = -0.5
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
        self.elapsed_time += dt
        self.mouse_x, self.mouse_y, buttons_states = self.get_mouse_state()
        ImGuiExtra.imgui_begin_frame(
            int(self.mouse_x), int(self.mouse_y), buttons_states, 0, self.width, self.height
        )
       
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
        self.check_viewdistance()

        #self.text = str.format("y:{0} p:{1} x:{2} y:{3} z:{4} c:{5} {6} {7}",round(self.yaw),round(self.pitch),round(self.eye_glm.x),round(self.eye_glm.y),round(self.eye_glm.z),self.chunk_pos_x,self.chunk_pos_z,len(self.visible_chunks))
        view_glmlh = glm.lookAtRH(glm.vec3(self.eye_glm),glm.vec3(self.eye_glm+self.direction),glm.vec3(up_glm))
        proj_glmlh = glm.perspectiveRH(20, self.width / self.height, 0.1, 100000.0)
        
        bgfx.set_view_transform(0, as_void_ptr(glm.value_ptr(view_glmlh)), as_void_ptr(glm.value_ptr(proj_glmlh)))
        bgfx.set_view_rect(0, 0, 0, self.width, self.height)
        

        model_matrix = glm.rotate(glm.mat4x4(),self.elapsed_time/2,glm.vec3(self.elapsed_time/5,self.elapsed_time/30,self.elapsed_time/20))
        
       #bgfx.set_transform(as_void_ptr(glm.value_ptr(model_matrix)), 1)
        bgfx.set_uniform(self.eye_pos_uniform,as_void_ptr(glm.value_ptr(self.eye_glm)))
        #bgfx.set_texture(0,self.texture_lookup_uniform,self.texture_lookup)
        bgfx.set_uniform(self.light_uniform,as_void_ptr((c_float * 4)(self.light_x.value, self.light_y.value,self.light_z.value,1)))
   
         #bgfx.update(self.vertex_buffer,0,vb_memory)

        # Set vertex and index buffer.
        for chunk in self.visible_chunks.values():
            bgfx.set_state(0
                # BGFX_STATE_PT_LINES
                | BGFX_STATE_WRITE_RGB 
                | BGFX_STATE_WRITE_A 
                | BGFX_STATE_WRITE_Z
                | BGFX_STATE_DEPTH_TEST_LESS 
                |
                0,
            )
            test = np.array([chunk.chunk_position[1]*chunk.chunk_width,0,chunk.chunk_position[0]*chunk.chunk_width,0],np.float32)
            bgfx.set_uniform(self.offset_uniform,as_void_ptr((c_float * 4)(test[0], test[1],test[2],test[3])))
           
            bgfx.set_vertex_buffer(0, chunk.vertex_buffer, 0, 200000)
        
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
         
        ImGui.slider_float('light_x', self.light_x, 0, 100, '%.2f', 1)
        ImGui.slider_float('light_y', self.light_y, 0, 100, '%.2f', 1)
        ImGui.slider_float('light_z', self.light_z, 0, 100, '%.2f', 1)
       
        ImGui.end()

    def color2float(self,color): 
        c_precision = 128.0
        c_precisionp1 = c_precision + 1.0
        
        return math.floor(color[0] * c_precision + 0.5) + math.floor(color[1] * c_precision + 0.5) * c_precisionp1 + math.floor(color[2] * c_precision + 0.5) * c_precisionp1 * c_precisionp1

if __name__ == "__main__":
    textures = Textures(1280, 1280, "examples/textures")
    textures.run()
