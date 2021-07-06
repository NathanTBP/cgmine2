import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import glm

from Window import Window
from Shader import Shader
from Blocks import Block

import math
import time
import random

altura_janela = 900;
largura_janela  = 900;
cameraPos   = glm.vec3(0.0,  0.0,  1.0);
cameraFront = glm.vec3(0.0,  0.0,  1.0);
cameraUp    = glm.vec3(0.0,  1.0,  0.0);
polygonal_mode = False

#Ta copiado, não sei ainda
firstMouse = True
yaw = -90.0 
pitch = 0.0
lastX =  largura_janela/2
lastY =  altura_janela/2

class Mine:
    
    #Inputs (game controller)
    inpTx = 0 # Translação em X
    inpTy = 0 # Translação em Y
    inpTz = 0 # Pulo
    inpMesh = False # Ativar a malha poligonal
    

    def __init__(self):
        #Inicialização da Janela
        self.window = Window(altura_janela, largura_janela, "Trabalho 02")
        self.shader = Shader()

        #Atribuição de eventos
        self.window.setOnDraw(self.onDraw)
        self.window.setKeyEvent(self.onKeyEvent)
        self.window.setCursorEvent(self.onCursorEvent)

        #Dados referentes ao jogo
        self.gameOver = False
        self.blocks = []

        block= Block(1,1,1,3)
        self.blocks.append(block)

        block.draw(self.shader.getProgram())

    def run(self):
        self.window.loop()

    def onDraw(self):
        #Para desenhar, limpa o buffer de cores
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(1.0, 1.0, 1.0, 1.0)
      
        #tem que desenhar os blocos

    def onKeyEvent(self, window, key, scancode, action, mods):
       
        cameraSpeed = 0.3

        #Andar para frente (+Y)
        if key == ord('W') and (action==1 or action==2):
            cameraPos += cameraSpeed * cameraFront

        #Andar para frente (-Y)
        if key == ord('S') and (action==1 or action==2):
            cameraPos -= cameraSpeed * cameraFront
        
        #Andar para a direita
        if key == ord('D') and (action==1 or action==2):
            cameraPos += glm.normalize(glm.cross(cameraFront, cameraUp)) * cameraSpeed

        #Andar para a esquerda
        if key == ord('A') and (action==1 or action==2):
            cameraPos -= glm.normalize(glm.cross(cameraFront, cameraUp)) * cameraSpeed

        #Pular
        #if key == ord(' ') and (action==1 or action==2):
            #vaiterqueterumafunção prapulo

        #Ativar a visão poligonal
        if key == ord('P') and (action==1 or action==2) and polygonal_mode == False:
            self.inpMesh = True

        #Desativar a visão poligonal
        if key == ord('P') and (action==1 or action==2) and polygonal_mode == True:
            self.inpMesh = False   

    def onCursorEvent(window, xpos, ypos):
        global firstMouse, cameraFront, yaw, pitch, lastX, lastY
        if firstMouse:
            lastX = xpos
            lastY = ypos
            firstMouse = False

        xoffset = xpos - lastX
        yoffset = lastY - ypos
        lastX = xpos
        lastY = ypos

        sensitivity = 0.3 
        xoffset *= sensitivity
        yoffset *= sensitivity

        yaw += xoffset
        pitch += yoffset

        if pitch >= 90.0: pitch = 90.0
        if pitch <= -90.0: pitch = -90.0

        front = glm.vec3()
        front.x = math.cos(glm.radians(yaw)) * math.cos(glm.radians(pitch))
        front.y = math.sin(glm.radians(pitch))
        front.z = math.sin(glm.radians(yaw)) * math.cos(glm.radians(pitch))
        cameraFront = glm.normalize(front)

        def view():
            global cameraPos, cameraFront, cameraUp
            mat_view = glm.lookAt(cameraPos, cameraPos + cameraFront, cameraUp);
            mat_view = np.array(mat_view)
            return mat_view

        def projection():
            global altura_janela, largura_janela 

            fov = glm.radians(45.0)
            aspect = largura_janela/altura_janela
            znear = 0.1
            zfar = 500

            mat_projection = glm.perspective(fov,aspect, znear, zfar)
            mat_projection = np.array(mat_projection)    
            return mat_projection