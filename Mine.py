import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import glm

from Window import Window
from Shader import Shader
from Blocks import Block
from Player import Player
from MultiBlock import MultiBlock
from House import House

import math
import time
import random

class Mine:

    #Globais
    altura_janela = 900
    largura_janela  = 900

    
    #Inputs (game controller)
    lateralInt = 0  # Translação em X
    forwardInt = 0  # Translação em Z
    verticalInt = 0  # Translação em Y

    scrollXOffset = 0
    scrollYOffset = 0

    polygonal_mode = False  # Malha poligonal

    gameStep = 1/60

    boxSize = 100  # x e z
    heightSize = 60  # y

    def __init__(self):
        # Inicialização da Janela
        self.window = Window(self.altura_janela, self.largura_janela, "Trabalho 02")
        self.shader = Shader()

        # Atribuição de eventos
        self.window.setOnDraw(self.onDraw)
        self.window.setKeyEvent(self.onKeyEvent)
        self.window.setCursorEvent(self.onCursorEvent)
        self.window.setScrollEvent(self.onScrollEvent)
        self.window.invertCursorLocked()

        # Dados referentes ao jogo
        self.gameOver = False
        self.objects = []

        multiblock = MultiBlock(4)
        multiblock.generatePlane((0, 0, 0), (1, 0, 0), (0, 0, 1), 15, 15)
        self.objects += multiblock.placeBlocks()

        self.objects.append(House((3, 1, 3), 6, 7, 3))

        self.player = Player(self.altura_janela, self.largura_janela)
        self.player.setLimit(self.boxSize, self.heightSize)

        for i in range(12):
            block= Block(i+1,0,0,0,i+1)
            self.objects.append(block)
            block= Block(i+2,0,2,90,i+1)
            self.objects.append(block)
            block= Block(i+2,1,4,180,i+1)
            self.objects.append(block)
            block= Block(i+1,1,6,270,i+1)
            self.objects.append(block)

        print(len(self.objects))


        self.lastTime = time.time()

        self.mouseX = self.largura_janela/2
        self.mouseY = self.altura_janela/2

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

        for block in self.objects:
            block.draw(program)
       

    def onKeyEvent(self, window, key, scancode, action, mods):
        if action == 2:
            return

        mult = action*2-1

        # Andar para frente
        if key == glfw.KEY_W:
            self.forwardInt += mult

        # Andar para frente
        if key == glfw.KEY_S:
            self.forwardInt -= mult

        # Andar para a direita
        if key == glfw.KEY_D:
            self.lateralInt += mult

        # Andar para a esquerda
        if key == glfw.KEY_A:
            self.lateralInt -= mult

        # Subir
        if key == glfw.KEY_SPACE:
            self.verticalInt += mult

        # Descer
        if key == glfw.KEY_LEFT_SHIFT:
            self.verticalInt -= mult

        # Ativar e desativar a visão poligonal
        if key == glfw.KEY_P and action == 1:
            self.polygonal_mode = not self.polygonal_mode

        if key == glfw.KEY_ESCAPE and action == 1:
            self.window.invertCursorLocked()

    def onCursorEvent(self, window, xpos, ypos):
        # print(xpos, ypos)
        self.mouseX = xpos
        self.mouseY = ypos

    def onScrollEvent(self, window, xoffset, yoffset):
        self.scrollXOffset = xoffset
        self.scrollYOffset = yoffset

    def physicsTick(self):
        self.player.movePlayer(self.forwardInt, self.lateralInt, self.verticalInt)
        self.player.lookAround(self.mouseX, self.mouseY)
        self.player.zoom(self.scrollYOffset)

        self.scrollXOffset = 0.0
        self.scrollYOffset = 0.0

        # program = self.shader.getProgram()


