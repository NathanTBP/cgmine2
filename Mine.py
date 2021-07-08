import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import glm

from Window import Window
from Shader import Shader
from Blocks import Block
from Player import Player

import math
import time
import random

class Mine:

    #Globais
    altura_janela = 900
    largura_janela  = 900



    #Ta copiado, não sei ainda
    firstMouse = True
    yaw = -90.0 
    pitch = 0.0
    lastX =  largura_janela/2
    lastY =  altura_janela/2

    
    #Inputs (game controller)
    lateralInt = 0  # Translação em X
    forwardInt = 0  # Translação em Y
    verticalInt = 0  # Pulo
    polygonal_mode = True  # Malha poligonal

    gameStep = 1/60

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

        self.player = Player(self.altura_janela, self.largura_janela)

        block= Block(0,0,0,3)
        self.blocks.append(block)

        self.lastTime = time.time()

    def run(self):
        self.window.loop()

    def onDraw(self):
        #Para desenhar, limpa o buffer de cores e pega o programa
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(1.0, 1.0, 1.0, 1.0)
        program=self.shader.getProgram()

        now = time.time()

        if (now-self.lastTime > self.gameStep):
            self.physicsTick()
            self.lastTime = now

        # verifica se deve usar o modo polygonal
        if self.polygonal_mode:
            glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)

        self.player.draw(program)

        # desenha o cenario
        for block in self.blocks:
            block.draw(program)
       

    def onKeyEvent(self, window, key, scancode, action, mods):
        if action == 2:
            return

        mult = action*2-1

        # cameraSpeed = 0.5
        #
        # #Andar para frente (+Y)
        # if key == ord('W') and (action==1 or action==2):
        #     self.cameraPos += cameraSpeed * self.cameraFront
        #
        # #Andar para frente (-Y)
        # if key == ord('S') and (action==1 or action==2):
        #     self.cameraPos -= cameraSpeed * self.cameraFront
        #
        # #Andar para a direita
        # if key == ord('D') and (action==1 or action==2):
        #     self.cameraPos += glm.normalize(glm.cross(self.cameraFront, self.cameraUp)) * cameraSpeed
        #
        # #Andar para a esquerda
        # if key == ord('A') and (action==1 or action==2):
        #     self.cameraPos -= glm.normalize(glm.cross(self.cameraFront, self.cameraUp)) * cameraSpeed

        #Pular
        #if key == ord(' ') and (action==1 or action==2):
            #vaiterqueterumafunção prapulo

        #Ativar e desativar a visão poligonal
        if key == ord('P') and (action==1):
            self.polygonal_mode = not self.polygonal_mode

    def onCursorEvent(self, window, xpos, ypos):

        if self.firstMouse:
            self.lastX = xpos
            self.lastY = ypos
            self.firstMouse = False

        xoffset = xpos - self.lastX
        yoffset = self.lastY - ypos
        self.lastX = xpos
        self.lastY = ypos

        sensitivity = 0.2 
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
        # self.cameraFront = glm.normalize(front)

    def physicsTick(self):
        pass
