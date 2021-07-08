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
        textures_coord_list = []
        self.faces_textures_ids = []

        #Carrega o bloco da pasta de objetos
        modelo = self.load_model_from_file('models/bloco.obj')
        for face in modelo['faces']:
            for vertice_id in face[0]:
                vertices_list.append( modelo['vertices'][vertice_id-1])
            for texture_id in face[1]:
                textures_coord_list.append( modelo['texture'][texture_id-1])

        print(vertices_list)
        print(textures_coord_list)

        #carrega as texturas das 6 faces do tipo de bloco dos arquivos .png e atribui aos ids de cada face
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

        glEnable(GL_TEXTURE_2D)

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
                self.faces_textures_ids.append(i+1)
        
    def load_model_from_file(self,filename):
        """Loads a Wavefront OBJ file. """
        objects = {}
        vertices = []
        texture_coords = []
        faces = []

        material = None

        # abre o arquivo obj para leitura
        for line in open(filename, "r"): ## para cada linha do arquivo .obj
            if line.startswith('#'): continue ## ignora comentarios
            values = line.split() # quebra a linha por espaço
            if not values: continue


            ### recuperando vertices
            if values[0] == 'v':
                vertices.append(values[1:4])


            ### recuperando coordenadas de textura
            elif values[0] == 'vt':
                texture_coords.append(values[1:3])

            ### recuperando faces 
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'f':
                face = []
                face_texture = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        face_texture.append(int(w[1]))
                    else:
                        face_texture.append(0)

                faces.append((face, face_texture, material))

        model = {}
        model['vertices'] = vertices
        model['texture'] = texture_coords
        model['faces'] = faces

        return model