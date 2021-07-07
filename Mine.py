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

class Mine:

    #Globais
    altura_janela = 900
    largura_janela  = 900
    cameraPos   = glm.vec3(0.0,  0.0,  1.0)
    cameraFront = glm.vec3(0.0,  0.0,  1.0)
    cameraUp    = glm.vec3(0.0,  1.0,  0.0)


    #Ta copiado, não sei ainda
    firstMouse = True
    yaw = -90.0 
    pitch = 0.0
    lastX =  largura_janela/2
    lastY =  altura_janela/2

    
    #Inputs (game controller)
    inpTx = 0 # Translação em X
    inpTy = 0 # Translação em Y
    inpTz = 0 # Pulo
    polygonal_mode = False #Malha poligonal

    def __init__(self):
        #Inicialização da Janela
        self.window = Window(self.altura_janela, self.largura_janela, "Trabalho 02")
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
        print(block.type)

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
            self.cameraPos += cameraSpeed * self.cameraFront

        #Andar para frente (-Y)
        if key == ord('S') and (action==1 or action==2):
            self.cameraPos -= cameraSpeed * self.cameraFront
        
        #Andar para a direita
        if key == ord('D') and (action==1 or action==2):
            self.cameraPos += glm.normalize(glm.cross(self.cameraFront, self.cameraUp)) * cameraSpeed

        #Andar para a esquerda
        if key == ord('A') and (action==1 or action==2):
            self.cameraPos -= glm.normalize(glm.cross(self.cameraFront, self.cameraUp)) * cameraSpeed

        #Pular
        #if key == ord(' ') and (action==1 or action==2):
            #vaiterqueterumafunção prapulo

        #Ativar a visão poligonal
        if key == ord('P') and (action==1 or action==2) and self.polygonal_mode == False:
            self.polygonal_mode = True

        #Desativar a visão poligonal
        if key == ord('P') and (action==1 or action==2) and self.polygonal_mode == True:
           self.polygonal_mode = False   

    def onCursorEvent(self,window, xpos, ypos):

        if self.firstMouse:
            self.lastX = xpos
            self.lastY = ypos
            self.firstMouse = False

        xoffset = xpos - self.lastX
        yoffset = self.lastY - ypos
        self.lastX = xpos
        self.lastY = ypos

        sensitivity = 0.3 
        xoffset *= sensitivity
        yoffset *= sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        if self.pitch >= 90.0: self.pitch = 90.0
        if self.pitch <= -90.0: self.pitch = -90.0

        front = glm.vec3()
        front.x = math.cos(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch))
        front.y = math.sin(glm.radians(self.pitch))
        front.z = math.sin(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch))
        self.cameraFront = glm.normalize(front)

        def view(self):

            mat_view = glm.lookAt(self.cameraPos, self.cameraPos + self.cameraFront, self.cameraUp)
            mat_view = np.array(mat_view)
            return mat_view

        def projection(self):

            fov = glm.radians(45.0)
            aspect = self.largura_janela/self.altura_janela
            znear = 0.1
            zfar = 500

            mat_projection = glm.perspective(fov,aspect, znear, zfar)
            mat_projection = np.array(mat_projection)    
            return mat_projection