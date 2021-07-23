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

#Inicializa a classe bloco atribuindo os dados do criador a ele
#x,y,z e rotação para a matriz model e typeofblock para selecionar a textura (lista acima)
#isFixed e wasSent são controles para melhorar a perfomance de renderização 
#buffers e texturas tambem são locais de cada bloco

        self.x=x
        self.y=y
        self.z=z
        self.rot=rot
        self.type = typeofblock
        self.ka = 0
        self.kd = 0
        self.ks = 0
        self.ns = 0
        self.isFixed = isFixed
        self.wasSent = False
        self.hour = 12

        #Listas de controle de coordenadas do bloco
        cube_vertices_list = []
        cube_faces_list = []
        cube_normals_list = []
        vertices_list = []
        textures_coord_list = []
        normals_list = []
        self.faces_textures_ids = []

        #Cria os 8 vértices do cubo
        cube_vertices_list.append((0, 0, 0)) #A
        cube_vertices_list.append((0, 0, 1)) #B
        cube_vertices_list.append((0, 1, 0)) #C
        cube_vertices_list.append((0, 1, 1)) #D
        cube_vertices_list.append((1, 0, 0)) #E
        cube_vertices_list.append((1, 0, 1)) #F
        cube_vertices_list.append((1, 1, 0)) #G
        cube_vertices_list.append((1, 1, 1)) #H

        #Cria as 6 normais do cubo
        cube_normals_list.append((0, 1, 0)) #Cima
        cube_normals_list.append((1, 0, 0)) #Frente
        cube_normals_list.append((-1, 0, 0)) #Atras
        cube_normals_list.append((0, 0, 1)) #Direita
        cube_normals_list.append((0, 0, -1)) #Esquerda
        cube_normals_list.append((0, -1, 0)) #Baixo


        #Cria as faces do cubo (inferior esquerdo, inferior direito, superior direito) (inferior esquerdo,superior direito,superior esquerdo)
        #faces sempre de mesma orientação para aplicação de texturas.
        #top DHG DGC
        cube_faces_list.append((3,7,6,3,6,2))
        #front BFH BHD
        cube_faces_list.append((1,5,7,1,7,3)) 
        #behind EAC ECG
        cube_faces_list.append((4,0,2,4,2,6)) 
        #right FEG FGH 
        cube_faces_list.append((5,4,6,5,6,7)) 
        #left ABD ADC
        cube_faces_list.append((0,1,3,0,3,2))
        #bottom AEF AFB v
        cube_faces_list.append((0,4,5,0,5,1))   

        #Para cada face do cubo 
        for face in cube_faces_list:
            #Adiciona, da lista de vértices do cubo, os 3 vértices correspondentes a aquela face, suas texturas (correspondem exatamente as pontas da textura) e suas normais
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

        for i in range(6):
            for j in range(6):
                normals_list.append(cube_normals_list[i])

        #carrega as texturas das 6 faces dos arquivos .png e atribui aos ids de cada face
        self.load_textures()

        #Cria os buffers para mostrar o bloco na tela 

        total_vertices = len(vertices_list) #É um cubo, mas tem 36 vértices (cada face compartilha o mesmo vértice com as tres vizinhas) (todos aqui dao 36)
        total_textures = len(textures_coord_list)
        total_normals = len(normals_list)
        # print(total_textures)

        #Aloca buffers
        self.buffer = glGenBuffers(3) #um buffer para vertices, um para texturas e um para iluminacao

        #Prepara vertices
        self.vertices = np.zeros(total_vertices, [("position", np.float32, 3)]) # tres coordenadas de objeto
        self.vertices['position'] = np.array(vertices_list)
    
        #Prepara texturas
        self.textures = np.zeros(total_textures, [("position", np.float32, 2)]) # duas coordenadas de textura
        self.textures['position'] = textures_coord_list

        self.normals = np.zeros(total_normals, [("position", np.float32, 3)]) # três coordenadas
        self.normals['position'] = normals_list
        
        #Binda vertices
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer[0])
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer[0])

        #Binda Texturas
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer[1]) 
        glBufferData(GL_ARRAY_BUFFER, self.textures.nbytes, self.textures, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer[1]) 

        #Binda Iluminacao
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer[2]) 
        glBufferData(GL_ARRAY_BUFFER, self.normals.nbytes, self.normals, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer[2]) 

    def draw(self, program):

        #Para cada chamada de desenho do objeto

        # Mudar os valores de vértices da posição no GLSL (bind com o buffer local)
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

        # Mudar os valores de iluminacao no GLSL (bind)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer[2])
        stride = (self.textures).strides[0]
        offset = ctypes.c_void_p(0)
        loc_normals_coord = glGetAttribLocation(program, "normals")
        glEnableVertexAttribArray(loc_normals_coord)
        glVertexAttribPointer(loc_normals_coord, 2, GL_FLOAT, False, stride, offset)

        # Atribui a posição usando a matriz model
        mat_model = self.model()

        # Recupera as localizacoes da GPU e envia as informacoes do bloco para GPU

        loc_model = glGetUniformLocation(program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)   

        loc_ka = glGetUniformLocation(program, "ka")
        glUniform1f(loc_ka, self.ka)
    
        loc_kd = glGetUniformLocation(program, "kd") 
        glUniform1f(loc_kd, self.kd)

        loc_ks = glGetUniformLocation(program, "ks") 
        glUniform1f(loc_ks, self.ks)

        loc_ns = glGetUniformLocation(program, "ns") 
        glUniform1f(loc_ns, self.ns)

        #Pega a textura do id, e desenha cada parte do cubo

        for face in range(6):
            if self.type==13:  
                self.update_textures()
            glBindTexture(GL_TEXTURE_2D, self.faces_textures_ids[face]) #Linka a textura da face
            glDrawArrays(GL_TRIANGLES,face*6,6)  #Desenha a face


    def model(self):
    
        matrix_transform = glm.mat4(1.0)  # instanciando uma matriz identidade

        # aplicando translacao
        matrix_transform = glm.translate(matrix_transform, glm.vec3(self.x, self.y, self.z))

        # aplicando rotação em z
        matrix_transform = glm.rotate(matrix_transform, math.radians(self.rot), glm.vec3(0, 0, 1))

       #caracteristicas para o céu 

        if self.type == 13:
            matrix_transform = glm.translate(matrix_transform, glm.vec3(0, 0, -15))
            matrix_transform = glm.scale(matrix_transform, glm.vec3(15, 15, 15))

        matrix_transform = np.array(matrix_transform).T  # pegando a transposta da matriz (glm trabalha com ela invertida)
        
        return matrix_transform

    def load_texture_from_file(self, texture_id, img_textura):

        #binda a textura de um arquivo em um id (a partir de uma imagem)

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
        #Topo, lateral [frente,tras,direita,esquerda] e baixo

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
        # valores padrão, podem ser alterados em cada bloco, se desejado
        self.ka = 0.5
        self.kd = 0
        self.ks = 0
        self.ns = 1
        
        if self.type==1: # Grama
            self.kd = 0.25
            self.qtd_texturas = 3
            texturas = glGenTextures(self.qtd_texturas)
            self.load_texture_from_file(0,'textures/dirt.png')
            self.load_texture_from_file(1,'textures/grass_side.png')
            self.load_texture_from_file(2,'textures/grass_top.png')

            self.faces_textures_ids.append(2)
            for face in range(4):
                self.faces_textures_ids.append(1)
            self.faces_textures_ids.append(0)

        if self.type==2: #Areia 
            self.kd = 0.4
            self.qtd_texturas = 1
            texturas = glGenTextures(self.qtd_texturas)
            self.load_texture_from_file(3,'textures/sand.png')
            for i in range(6):
                self.faces_textures_ids.append(3)

        if self.type==3: # Terra
            self.kd = 0.2
            self.qtd_texturas = 1
            texturas = glGenTextures(self.qtd_texturas)
            self.load_texture_from_file(4,'textures/dirt.png')
            for i in range(6):
                self.faces_textures_ids.append(4)  

        if self.type==4: # Carvalho
            self.kd = 0.15
            self.qtd_texturas = 1
            texturas = glGenTextures(self.qtd_texturas)
            self.load_texture_from_file(5,'textures/planks_oak.png')
            for i in range(6):
                self.faces_textures_ids.append(5)

        if self.type==5: # Branca
            self.kd = 0.3
            self.qtd_texturas = 1
            texturas = glGenTextures(self.qtd_texturas)
            self.load_texture_from_file(6,'textures/planks_birch.png')
            for i in range(6):
                self.faces_textures_ids.append(6)

        if self.type==6: #Tronco
            self.kd = 0.1
            self.qtd_texturas = 2
            texturas = glGenTextures(self.qtd_texturas)
            self.load_texture_from_file(7,'textures/log_oak.png')
            self.load_texture_from_file(8,'textures/log_oak_top.png')
            self.faces_textures_ids.append(8)
            for face in range(4):
                self.faces_textures_ids.append(7)
            self.faces_textures_ids.append(8)

        if self.type==7: #Folha
            self.kd = 0.3
            self.qtd_texturas = 1
            texturas = glGenTextures(self.qtd_texturas)
            self.load_texture_from_file(9,'textures/leaves_oak.png')
            for i in range(6):
                self.faces_textures_ids.append(9)

        if self.type==8: # Craft Table
            self.kd = 0.15
            self.qtd_texturas = 3
            texturas = glGenTextures(self.qtd_texturas)
            self.load_texture_from_file(10,'textures/crafting_table_top.png')
            self.load_texture_from_file(11,'textures/crafting_table_side.png')
            self.load_texture_from_file(5,'textures/planks_oak.png')
            self.faces_textures_ids.append(10)
            for face in range(4):
                self.faces_textures_ids.append(11)
            self.faces_textures_ids.append(5)

        if self.type==9: # Fornalha
            self.kd = 0.6
            self.qtd_texturas = 3
            texturas = glGenTextures(self.qtd_texturas)
            self.load_texture_from_file(12,'textures/furnace_top.png')
            self.load_texture_from_file(13,'textures/furnace_side.png')
            self.load_texture_from_file(14,'textures/furnace_front_off.png')
            self.faces_textures_ids.append(12)
            self.faces_textures_ids.append(14) # Frente
            for face in range(3):
                self.faces_textures_ids.append(13)
            self.faces_textures_ids.append(12) # baixo
        
        if self.type==10: #Folha
            self.kd = 0.3
            self.qtd_texturas = 1
            texturas = glGenTextures(self.qtd_texturas)
            self.load_texture_from_file(9,'textures/leaves_oak.png')
            for i in range(6):
                self.faces_textures_ids.append(9)

        if self.type==11: # Grama com carrinho reto
            self.kd = 0.25
            self.qtd_texturas = 3
            texturas = glGenTextures(self.qtd_texturas)
            self.load_texture_from_file(0,'textures/dirt.png')
            self.load_texture_from_file(1,'textures/grass_side.png')
            self.load_texture_from_file(15,'textures/grass_top_cart.png')
            self.faces_textures_ids.append(15)
            for face in range(4):
                self.faces_textures_ids.append(1)
            self.faces_textures_ids.append(0)

        if self.type==12: # Grama com carrinho reto
            self.kd = 0.25
            self.qtd_texturas = 3
            texturas = glGenTextures(self.qtd_texturas)
            self.load_texture_from_file(0,'textures/dirt.png')
            self.load_texture_from_file(1,'textures/grass_side.png')
            self.load_texture_from_file(16,'textures/grass_top_cart2.png')
            self.faces_textures_ids.append(16)
            for face in range(4):
                self.faces_textures_ids.append(1)
            self.faces_textures_ids.append(0)
        
        if self.type==13: # Ceu
            self.kd = 0.9
            self.qtd_texturas = 19
            texturas = glGenTextures(self.qtd_texturas)
            self.load_texture_from_file(17,'textures/sky_day.jpg')
            self.load_texture_from_file(18,'textures/sky_night.jpg')
            self.load_texture_from_file(19,'textures/sky_bottom.png')
            self.load_texture_from_file(20,'textures/sky_sun1.jpg')
            self.load_texture_from_file(21,'textures/sky_sun2.jpg')
            self.load_texture_from_file(22,'textures/sky_sun3.jpg')
            self.load_texture_from_file(23,'textures/sky_sun4.jpg')
            self.load_texture_from_file(24,'textures/sky_moon1.jpg')
            self.load_texture_from_file(25,'textures/sky_moon2.jpg')
            self.load_texture_from_file(26,'textures/sky_moon3.jpg')
            self.load_texture_from_file(27,'textures/sky_moon4.jpg')
            self.load_texture_from_file(28,'textures/sky_sunl1.jpg')
            self.load_texture_from_file(29,'textures/sky_sunl2.jpg')
            self.load_texture_from_file(30,'textures/sky_sunl3.jpg')
            self.load_texture_from_file(31,'textures/sky_sunl4.jpg')
            self.load_texture_from_file(32,'textures/sky_moonl1.jpg')
            self.load_texture_from_file(33,'textures/sky_moonl2.jpg')
            self.load_texture_from_file(34,'textures/sky_moonl3.jpg')
            self.load_texture_from_file(35,'textures/sky_moonl4.jpg')
            
    def update_textures(self):

        self.faces_textures_ids= []

        hour=math.floor(self.hour)

        #Lua na esquerda
        if(hour==3):       
            for i in range(4):
                self.faces_textures_ids.append(18)
            self.faces_textures_ids.append(32)
        elif(hour==4):       
            for i in range(4):
                self.faces_textures_ids.append(18)
            self.faces_textures_ids.append(33)
        elif(hour==5):       
            for i in range(4):
                self.faces_textures_ids.append(18)
            self.faces_textures_ids.append(34)
        elif(hour==6):       
            for i in range(4):
                self.faces_textures_ids.append(18)
            self.faces_textures_ids.append(35)

        #Lua acima
        elif(hour==23):
            self.faces_textures_ids.append(24)
            for i in range(4):
                self.faces_textures_ids.append(18)
        elif(hour==0):
            self.faces_textures_ids.append(25)
            for i in range(4):
                self.faces_textures_ids.append(18)
        elif(hour==1):
            self.faces_textures_ids.append(26)
            for i in range(4):
                self.faces_textures_ids.append(18)
        elif(hour==2):
            self.faces_textures_ids.append(27)
            for i in range(4):
                self.faces_textures_ids.append(18)

        #Lua na direita
        elif(hour==22):       
            for i in range(3):
                self.faces_textures_ids.append(18)
            self.faces_textures_ids.append(32)
            self.faces_textures_ids.append(18)
        elif(hour==21):       
            for i in range(3):
                self.faces_textures_ids.append(18)
            self.faces_textures_ids.append(33)
            self.faces_textures_ids.append(18)  
        elif(hour==20):       
            for i in range(3):
                self.faces_textures_ids.append(18)
            self.faces_textures_ids.append(34)
            self.faces_textures_ids.append(18)
        elif(hour==19):       
            for i in range(3):
                self.faces_textures_ids.append(18)
            self.faces_textures_ids.append(35)
            self.faces_textures_ids.append(18)        

        #Sol na direita
        elif(hour==10):       
            for i in range(3):
                self.faces_textures_ids.append(17)
            self.faces_textures_ids.append(28)
            self.faces_textures_ids.append(17)
        elif(hour==9):       
            for i in range(3):
                self.faces_textures_ids.append(17)
            self.faces_textures_ids.append(29)
            self.faces_textures_ids.append(17)  
        elif(hour==8):       
            for i in range(3):
                self.faces_textures_ids.append(17)
            self.faces_textures_ids.append(30)
            self.faces_textures_ids.append(17)
        elif(hour==7):       
            for i in range(3):
                self.faces_textures_ids.append(17)
            self.faces_textures_ids.append(31)
            self.faces_textures_ids.append(17)  


        #Sol acima
        elif(hour==11):
            self.faces_textures_ids.append(20)
            for i in range(4):
                self.faces_textures_ids.append(17)
        elif(hour==12):
            self.faces_textures_ids.append(21)
            for i in range(4):
                self.faces_textures_ids.append(17)
        elif(hour==13):
            self.faces_textures_ids.append(22)
            for i in range(4):
                self.faces_textures_ids.append(17)
        elif(hour==14):
            self.faces_textures_ids.append(23)
            for i in range(4):
                self.faces_textures_ids.append(17)


        #Sol na esquerda
        elif(hour==15):       
            for i in range(4):
                self.faces_textures_ids.append(17)
            self.faces_textures_ids.append(28)
        elif(hour==16):       
            for i in range(4):
                self.faces_textures_ids.append(17)
            self.faces_textures_ids.append(29)
        elif(hour==17):       
            for i in range(4):
                self.faces_textures_ids.append(17)
            self.faces_textures_ids.append(30)
        elif(hour==18):       
            for i in range(4):
                self.faces_textures_ids.append(17)
            self.faces_textures_ids.append(31)
        
        self.faces_textures_ids.append(19)

#getter e setters

    def getCoord(self):
        return (self.x, self.y, self.z)

    def setCoord(self, coord):
        self.x, self.y, self.z = coord
    
    def getHr(self):
        return self.hour

    def setHr(self,hour):
        self.hour=hour
