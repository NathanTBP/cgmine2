import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math
import glm
from PIL import Image

# Lista de blocos e seus códigos (tipo do bloco,range de id de texturas):
# Grama 1 1
# Areia 2 2
# Madeira processada de Carvalho 3 3
# Tronco de Carvalho 4 4-5

class Block:

    def __init__ (self,x,y,z,typeofblock):

        self.x=x
        self.y=y
        self.z=z

        self.type = typeofblock
        vertices_list = []
        faces_list = []
        textures_coord_list = []

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

        #top
        faces_list.append((1,3,5))
        faces_list.append((7,3,5))
        #bottom
        faces_list.append((0,2,4))
        faces_list.append((6,2,4))
        #front
        faces_list.append((4,5,6))
        faces_list.append((7,5,6))
        #behind
        faces_list.append((0,1,2))
        faces_list.append((3,1,2))
        #right
        faces_list.append((6,2,7))
        faces_list.append((3,2,7))
        #left
        faces_list.append((0,1,4))
        faces_list.append((5,1,4))

        #Todos triangulos retangulos bonitinhos de mesma orientação
        textures_coord_list.append((1,0))
        textures_coord_list.append((0,1))
        textures_coord_list.append((0,0))

        #Cria os buffers para mostrar o bloco na tela 

        total_vertices = 8 #É um cubo

        #Aloca buffers
        self.buffer = glGenBuffers(2) 

        #Prepara vertices
        self.vertices = np.zeros(total_vertices, [("position", np.float32, 3)])
        self.vertices['position'] = np.array(vertices_list)
        
        #Prepara texturas
        self.textures = np.zeros(len(textures_coord_list), [("position", np.float32, 2)]) # duas coordenadas
        self.textures['position'] = textures_coord_list

        #Binda vertices
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer[0])
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer[0])

        #Binda Texturas
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer[1]) 
        glBufferData(GL_ARRAY_BUFFER, self.textures.nbytes, self.textures, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer[1]) 

    def draw(self, program):

        #Mudar os valores de vértices da posição no GLSL (bind)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer[0])
        stride = (self.vertices).strides[0]
        offset = ctypes.c_void_p(0)
        loc_vertices = glGetAttribLocation(program, "position")
        glEnableVertexAttribArray(loc_vertices)
        glVertexAttribPointer(loc_vertices, 2, GL_FLOAT, False, stride, offset)

        #Mudar os valores de texturas no GLSL (bind)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer[1])
        stride = (self.textures).strides[0]
        offset = ctypes.c_void_p(0)
        loc_texture_coord = glGetAttribLocation(program, "texture_coord")
        glEnableVertexAttribArray(loc_texture_coord)
        glVertexAttribPointer(loc_texture_coord, 2, GL_FLOAT, False, stride, offset)

        #Atribui a posição
        mat_model = model()
        loc_model = glGetUniformLocation(program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)      
        
        for face in range(6):
            load_texture_from_block(face)


    def model(self):
    
        angle = math.radians(angle)
        
        matrix_transform = glm.mat4(1.0) # instanciando uma matriz identidade

        # aplicando translacao
        matrix_transform = glm.translate(matrix_transform, glm.vec3(self.x, self.y, self.z))    
        
        matrix_transform = np.array(matrix_transform).T # pegando a transposta da matriz (glm trabalha com ela invertida)
        
        return matrix_transform

    def load_texture_from_file(self,texture_id, img_textura):

        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        img = Image.open(img_textura)
        img_width = img.size[0]
        img_height = img.size[1]
        image_data = img.tobytes("raw", "RGB", 0, -1)
        #image_data = np.array(list(img.getdata()), np.uint8)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_width, img_height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)

    def load_texture_from_block(self,face):

        if face==0:
            #desenha topo
            if(self.type==3):
                load_texture_from_file(3,'text/planks_oak.png')
        elif face==1:
            #desenha baixo
            if(self.type==3):
                load_texture_from_file(3,'text/planks_oak.png')
        elif face==2:    
            #desenha frente
            if(self.type==3):
                load_texture_from_file(3,'text/planks_oak.png')
        elif face==3:
            #desenha tras
            if(self.type==3):
                load_texture_from_file(3,'text/planks_oak.png')
        elif face==4:  
            #desenha direita
            if(self.type==3):
                load_texture_from_file(3,'text/planks_oak.png')
        elif face==5:
            #desenha esquerda
            if(self.type==3):
                load_texture_from_file(3,'text/planks_oak.png')
        
