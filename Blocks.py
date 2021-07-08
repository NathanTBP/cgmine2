import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math
import glm
from PIL import Image

# Lista de blocos e seus códigos (tipo do bloco,range de id de texturas):
# Grama 1 3
# Areia 2 1
# Terra 3 1
# Madeira processada de Carvalho 4 1
# Madeira processada Branca 5 1
# Tronco de Carvalho 6 2
# Folha de Carvalho 7 1
# Craft Table 8 3
# Fornalha 9 3
# Bau 10 1
# Grama com Carrinho 11 3
# Grama com Carrinho torto 12 3
# Ceu 13 3


class Block:

    def __init__ (self, x, y, z, rot, typeofblock, isFixed=True):

        self.x=x
        self.y=y
        self.z=z
        self.rot=rot
        self.type = typeofblock
        self.isFixed = isFixed
        self.wasSent = False

        cube_vertices_list = []
        cube_faces_list = []
        vertices_list = []
        list_of_vertices_list = []
        textures_coord_list = []
        list_of_textures_coord_list = []
        self.faces_textures_ids = []

        #Cria os 8 vértices do cubo
        cube_vertices_list.append((0+x, 0+y, 0+z))
        cube_vertices_list.append((0+x, 0+y, 1+z))
        cube_vertices_list.append((0+x, 1+y, 0+z))
        cube_vertices_list.append((0+x, 1+y, 1+z))
        cube_vertices_list.append((1+x, 0+y, 0+z))
        cube_vertices_list.append((1+x, 0+y, 1+z))
        cube_vertices_list.append((1+x, 1+y, 0+z))
        cube_vertices_list.append((1+x, 1+y, 1+z))

        # print(cube_vertices_list)

        #Cria as faces do cubo (inferior esquerdo, inferior direito, superior direito) (inferior esquerdo,superior direito,superior esquerdo)

        #top DHG DGC v
        cube_faces_list.append((3,7,6,3,6,2))
        #front BFH BHD v
        cube_faces_list.append((1,5,7,1,7,3)) 
        #behind EAC ECG v
        cube_faces_list.append((4,0,2,4,2,6)) 
        #right FEG FGH 
        cube_faces_list.append((5,4,6,5,6,7)) 
        #left ABD ADC
        cube_faces_list.append((0,1,3,0,3,2))
        #bottom AEF AFB v
        cube_faces_list.append((0,4,5,0,5,1))   

        # print(cube_faces_list)

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

        #carrega as texturas das 6 faces dos arquivos .png e atribui aos ids de cada face
        self.load_textures()


        #Cria os buffers para mostrar o bloco na tela 

        total_vertices = len(vertices_list) #É um cubo, mas tem 24 vértices (cada face compartilha o mesmo vértice com as duas vizinhas)
        total_textures = len(textures_coord_list)
        # print(total_textures)

        #Aloca buffers
        self.buffer = glGenBuffers(2) 

        #Prepara vertices
        self.vertices = np.zeros(total_vertices, [("position", np.float32, 3)]) # tres coordenadas de objeto
        self.vertices['position'] = np.array(vertices_list)
    
        #Prepara texturas
        self.textures = np.zeros(total_textures, [("position", np.float32, 2)]) # duas coordenadas de textura
        self.textures['position'] = textures_coord_list

        # print(len(self.vertices))

        #Binda vertices
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer[0])
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer[0])

        #Binda Texturas
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer[1]) 
        glBufferData(GL_ARRAY_BUFFER, self.textures.nbytes, self.textures, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer[1]) 

    def draw(self, program):

        # Mudar os valores de vértices da posição no GLSL (bind)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer[0])
        stride = (self.vertices).strides[0]
        offset = ctypes.c_void_p(0)
        loc_vertices = glGetAttribLocation(program, "position")
        glEnableVertexAttribArray(loc_vertices)
        glVertexAttribPointer(loc_vertices, 3, GL_FLOAT, False, stride, offset)

        # Mudar os valores de texturas no GLSL (bind)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer[1])
        stride = (self.textures).strides[0]
        offset = ctypes.c_void_p(0)
        loc_texture_coord = glGetAttribLocation(program, "texture_coord")
        glEnableVertexAttribArray(loc_texture_coord)
        glVertexAttribPointer(loc_texture_coord, 2, GL_FLOAT, False, stride, offset)


        # Atribui a posição usando a matriz model
        if self.isFixed == False:
            mat_model = self.model()
        else:
            mat_model = np.array(glm.mat4(1.0)).T

        loc_model = glGetUniformLocation(program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)    


        glBindTexture(GL_TEXTURE_2D, self.faces_textures_ids[0]) #Topo
        glMultiDrawArrays(GL_TRIANGLES,0,6,6)  

        glBindTexture(GL_TEXTURE_2D, self.faces_textures_ids[1]) #Laterais
        glMultiDrawArrays(GL_TRIANGLES,6,24,6) 

        glBindTexture(GL_TEXTURE_2D, self.faces_textures_ids[2]) #Baixo
        glMultiDrawArrays(GL_TRIANGLES,24,36,6)  


    def model(self):
    
        matrix_transform = glm.mat4(1.0)  # instanciando uma matriz identidade

        # aplicando translacao
        matrix_transform = glm.translate(matrix_transform, glm.vec3(self.x, self.y, self.z))

        # aplicando rotação em z
        matrix_transform = glm.rotate(matrix_transform, math.radians(self.rot), glm.vec3(0, 0, 1))

        if self.type == 13:
            matrix_transform = glm.translate(matrix_transform, glm.vec3(0, 0, -15))
            matrix_transform = glm.scale(matrix_transform, glm.vec3(35, 35, 35))

        matrix_transform = np.array(matrix_transform).T  # pegando a transposta da matriz (glm trabalha com ela invertida)
        
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
        #Topo, lateral e baixo

# Lista de blocos e seus códigos (tipo do bloco,range de id de texturas):
# Grama 1 3
# Areia 2 1
# Terra 3 1
# Madeira processada de Carvalho 4 1
# Madeira processada Branca 5 1
# Tronco de Carvalho 6 2
# Folha de Carvalho 7 1
# Craft Table 8 3
# Fornalha 9 3
# Bau 10 1
# Grama com Carrinho 11 3
# Grama com Carrinho torto 12 3

        glEnable(GL_TEXTURE_2D) # Liga a textura
        self.load_texture_from_file(1,'textures/grass_side.png')
        if self.type==1: # Grama
            self.qtd_texturas = 3
            texturas = glGenTextures(self.qtd_texturas)
            self.load_texture_from_file(0,'textures/dirt.png')
            self.load_texture_from_file(1,'textures/grass_side.png')
            self.load_texture_from_file(2,'textures/grass_top.png')

            self.faces_textures_ids.append(2)
            self.faces_textures_ids.append(1)
            self.faces_textures_ids.append(0)

        if self.type==2: #Areia 
            self.qtd_texturas = 1
            texturas = glGenTextures(self.qtd_texturas)
            self.load_texture_from_file(3,'textures/sand.png')
            for i in range(3):
                self.faces_textures_ids.append(3)

        if self.type==3: # Terra
            self.qtd_texturas = 1
            texturas = glGenTextures(self.qtd_texturas)
            self.load_texture_from_file(4,'textures/dirt.png')
            for i in range(3):
                self.faces_textures_ids.append(4)  

        if self.type==4: # Carvalho
            self.qtd_texturas = 1
            texturas = glGenTextures(self.qtd_texturas)
            self.load_texture_from_file(5,'textures/planks_oak.png')
            for i in range(3):
                self.faces_textures_ids.append(5)

        if self.type==5: # Branca
            self.qtd_texturas = 1
            texturas = glGenTextures(self.qtd_texturas)
            self.load_texture_from_file(6,'textures/planks_birch.png')
            for i in range(3):
                self.faces_textures_ids.append(6)

        if self.type==6: #Tronco
            self.qtd_texturas = 2
            texturas = glGenTextures(self.qtd_texturas)
            self.load_texture_from_file(7,'textures/log_oak.png')
            self.load_texture_from_file(8,'textures/log_oak_top.png')
            self.faces_textures_ids.append(8)
            self.faces_textures_ids.append(7)
            self.faces_textures_ids.append(8)

        if self.type==7: #Folha
            self.qtd_texturas = 1
            texturas = glGenTextures(self.qtd_texturas)
            self.load_texture_from_file(9,'textures/leaves_oak.png')
            for i in range(3):
                self.faces_textures_ids.append(9)

        if self.type==8: # Craft Table
            self.qtd_texturas = 3
            texturas = glGenTextures(self.qtd_texturas)
            self.load_texture_from_file(10,'textures/crafting_table_top.png')
            self.load_texture_from_file(11,'textures/crafting_table_side.png')
            self.load_texture_from_file(5,'textures/planks_oak.png')
            self.faces_textures_ids.append(10)
            self.faces_textures_ids.append(11)
            self.faces_textures_ids.append(5)

        if self.type==9: # Fornalha
            self.qtd_texturas = 3
            texturas = glGenTextures(self.qtd_texturas)
            self.load_texture_from_file(12,'textures/furnace_top.png')
            self.load_texture_from_file(13,'textures/furnace_side.png')
            self.load_texture_from_file(14,'textures/furnace_front_off.png')
            self.faces_textures_ids.append(12)
            self.faces_textures_ids.append(13)
            self.faces_textures_ids.append(14)
        
        if self.type==10: #Folha
            self.qtd_texturas = 1
            texturas = glGenTextures(self.qtd_texturas)
            self.load_texture_from_file(9,'textures/leaves_oak.png')
            for i in range(3):
                self.faces_textures_ids.append(9)

        if self.type==11: # Grama com carrinho reto
            self.qtd_texturas = 3
            texturas = glGenTextures(self.qtd_texturas)
            self.load_texture_from_file(0,'textures/dirt.png')
            self.load_texture_from_file(1,'textures/grass_side.png')
            self.load_texture_from_file(15,'textures/grass_top_cart.png')
            self.faces_textures_ids.append(15)
            self.faces_textures_ids.append(1)
            self.faces_textures_ids.append(0)

        if self.type==12: # Grama com carrinho reto
            self.qtd_texturas = 3
            texturas = glGenTextures(self.qtd_texturas)
            self.load_texture_from_file(0,'textures/dirt.png')
            self.load_texture_from_file(1,'textures/grass_side.png')
            self.load_texture_from_file(16,'textures/grass_top_cart2.png')
            self.faces_textures_ids.append(16)
            self.faces_textures_ids.append(1)
            self.faces_textures_ids.append(0)
        
        if self.type==13: # Ceu
            self.qtd_texturas = 3
            texturas = glGenTextures(self.qtd_texturas)
            self.load_texture_from_file(17,'textures/sky_top.png')
            self.load_texture_from_file(18,'textures/sky_side.png')
            self.load_texture_from_file(19,'textures/sky_bottom.png')
            self.faces_textures_ids.append(17)
            self.faces_textures_ids.append(18)
            self.faces_textures_ids.append(19)
            self.isFixed = False
