import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math
import glm
from PIL import Image

# Lista de blocos e seus códigos (tipo do bloco,range de id de texturas):
# Grama 1 1
# Areia 2 1
# Madeira processada de Carvalho 3 3
# Tronco de Carvalho 4 2

class Block:

    def __init__ (self,x,y,z,typeofblock):

        self.x=x
        self.y=y
        self.z=z

        self.type = typeofblock
        cube_vertices_list = []
        cube_faces_list = []
        vertices_list = []
        textures_coord_list = []
        self.faces_textures_ids = []

        #Cria os 8 vértices do cubo
        cube_vertices_list.append((0,0,0))
        cube_vertices_list.append((0,0,1))
        cube_vertices_list.append((0,1,0))
        cube_vertices_list.append((0,1,1))
        cube_vertices_list.append((1,0,0))
        cube_vertices_list.append((1,0,1))
        cube_vertices_list.append((1,1,0))
        cube_vertices_list.append((1,1,1))

        print(cube_vertices_list)

        #Cria as faces do cubo (inferior esquerdo, inferior direito, superior direito) (inferior esquerdo,superior direito,superior esquerdo)

        #top DHG DGC v
        cube_faces_list.append((3,7,6,3,6,2)) 
        #bottom AEF AFB v
        cube_faces_list.append((0,4,5,0,5,1)) 
        #front BFH BHD v
        cube_faces_list.append((1,5,7,1,7,3)) 
        #behind EAC ECG v
        cube_faces_list.append((4,0,2,4,2,6)) 
        #right FEG FGH 
        cube_faces_list.append((5,4,6,5,6,7)) 
        #left ABD ADC
        cube_faces_list.append((0,1,3,0,3,2))  

        print(cube_faces_list)

        #Para cada face do cubo 
        for face in cube_faces_list:
            #Adiciona, da lista de vértices do cubo, os 3 vértices correspondentes a aquela face e suas texturas (correspondem exatamente as pontas da textura)
            vertices_list.append(cube_vertices_list[face[0]])
            textures_coord_list.append((0,0)) #inf esquerdo
            vertices_list.append(cube_vertices_list[face[1]])
            textures_coord_list.append((0,1)) #inf direito
            vertices_list.append(cube_vertices_list[face[2]])
            textures_coord_list.append((1,1)) #sup direito

            vertices_list.append(cube_vertices_list[face[3]])
            textures_coord_list.append((0,0)) #inf esquerdo
            vertices_list.append(cube_vertices_list[face[4]])
            textures_coord_list.append((1,1)) #sup direito
            vertices_list.append(cube_vertices_list[face[5]])
            textures_coord_list.append((1,0)) #sup esquerdo
            
            

        print(vertices_list)
        print(textures_coord_list)

        #carrega as texturas das 6 faces dos arquivos .png e atribui aos ids de cada face
        self.load_textures()

        print(self.faces_textures_ids)

        #Cria os buffers para mostrar o bloco na tela 

        total_vertices = len(vertices_list) #É um cubo, mas tem 24 vértices (cada face compartilha o mesmo vértice com as duas vizinhas)
        total_textures = len(textures_coord_list)
        print(total_textures)

        #Aloca buffers
        self.buffer = glGenBuffers(2) 

        #Prepara vertices
        self.vertices = np.zeros(total_vertices, [("position", np.float32, 3)]) # tres coordenadas de objeto
        self.vertices['position'] = np.array(vertices_list)
    
        #Prepara texturas
        self.textures = np.zeros(total_textures, [("position", np.float32, 2)]) # duas coordenadas de textura
        self.textures['position'] = textures_coord_list

        print(len(self.vertices))

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
        glVertexAttribPointer(loc_vertices, 3, GL_FLOAT, False, stride, offset)

        #Mudar os valores de texturas no GLSL (bind)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer[1])
        stride = (self.textures).strides[0]
        offset = ctypes.c_void_p(0)
        loc_texture_coord = glGetAttribLocation(program, "texture_coord")
        glEnableVertexAttribArray(loc_texture_coord)
        glVertexAttribPointer(loc_texture_coord, 2, GL_FLOAT, False, stride, offset)

        #Atribui a posição usando a matriz model
        mat_model = self.model()
        loc_model = glGetUniformLocation(program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)      
      
        #Para cada face do cubo (cima,baixo,frente,tras,direita,esquerda)
        for face in range(6):
            #Define vértice inicial (2 triangulos por face = 6 vertices), binda a textura referente a face e desenha a face
            v_face=face*6
            glBindTexture(GL_TEXTURE_2D, self.faces_textures_ids[face])
            glDrawArrays(GL_TRIANGLES,v_face,v_face+6)

    def model(self):
    
        matrix_transform = glm.mat4(1.0) # instanciando uma matriz identidade

        # aplicando translacao
        matrix_transform = glm.translate(matrix_transform, glm.vec3(self.x, self.y, self.z))

        matrix_transform = glm.rotate(matrix_transform, math.radians(90), glm.vec3(0, 0, 1))

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
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_width, img_height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)

    def load_textures(self):

        #bloco de madeira processada de carvalho, 6 faces iguais com a textura de id 3
        if self.type==1:
            self.load_texture_from_file(1,'dirt.png')
        if self.type==3:
            self.qtd_texturas = 10
            glEnable(GL_TEXTURE_2D)
            texturas = glGenTextures(self.qtd_texturas)
            self.load_texture_from_file(1,'textures/dirt.png')
            self.load_texture_from_file(2,'textures/sand.png')
            self.load_texture_from_file(3,'textures/planks_oak.png')
            self.load_texture_from_file(4,'textures/planks_birch.png')
            self.load_texture_from_file(5,'textures/log_oak.png')
            self.load_texture_from_file(6,'textures/log_oak_top.png')
            for i in range(6):
                self.faces_textures_ids.append(5)

        if self.type==4:
            self.qtd_texturas = 10
            glEnable(GL_TEXTURE_2D)
            texturas = glGenTextures(self.qtd_texturas)
            self.load_texture_from_file(5,'textures/log_oak.png')
            self.load_texture_from_file(6,'textures/log_oak_top.png')
            for i in range(2):
                self.faces_textures_ids.append(6)
            for i in range(4):
                self.faces_textures_ids.append(5)
        
