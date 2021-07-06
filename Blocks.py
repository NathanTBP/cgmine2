import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math
import glm

class Block:

    def __init__ (self, typeofblock):

        self.type = typeofblock
        vertices_list = []
        faces_list = []

        #Cria os 8 vértices do cubo
        vertices_list.append((0,0,0))
        vertices_list.append((0,0,1))
        vertices_list.append((0,1,0))
        vertices_list.append((0,1,1))
        vertices_list.append((1,0,0))
        vertices_list.append((1,0,1))
        vertices_list.append((1,1,0))
        vertices_list.append((1,1,1))

        #Cria as faces do cubo (com 2 triangulos cada)
        #behind
        faces_list.append((0,1,2))
        faces_list.append((3,1,2))
        #left
        faces_list.append((0,1,4))
        faces_list.append((5,1,4))
        #right
        faces_list.append((6,2,7))
        faces_list.append((3,2,7))
        #top
        faces_list.append((1,3,5))
        faces_list.append((7,3,5))
        #bottom
        faces_list.append((0,2,4))
        faces_list.append((6,2,4))
        #front
        faces_list.append((4,5,6))
        faces_list.append((7,5,6))


        #Cria os buffers para mostrar na tela todos os vértices de cada meteoro
        total_vertices = len(vertices_list)
        self.vertices = np.zeros(total_vertices, [("position", np.float32, 2)])
        self.vertices['position'] = np.array(vertices_list)

        self.buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer)

    def draw(self, program):
        #Para desenhar basta arrumar os buffers,
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer)
        stride = (self.vertices).strides[0]
        offset = ctypes.c_void_p(0)

        #Mudar os valores da posição no GLSL
        loc_pos = glGetAttribLocation(program, "position")
        glEnableVertexAttribArray(loc_pos)

        glVertexAttribPointer(loc_pos, 2, GL_FLOAT, False, stride, offset)

        mat_model = model()
        loc_model = glGetUniformLocation(program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)      
        
        #glBindTexture(GL_TEXTURE_2D, 3)

        for i in range(6):
            # desenha a face ;-;
            i=i+1


    def model(x,y,z):
    
        angle = math.radians(angle)
        
        matrix_transform = glm.mat4(1.0) # instanciando uma matriz identidade

        # aplicando translacao
        matrix_transform = glm.translate(matrix_transform, glm.vec3(x, y, z))    
        
        matrix_transform = np.array(matrix_transform).T # pegando a transposta da matriz (glm trabalha com ela invertida)
        
        return matrix_transform

