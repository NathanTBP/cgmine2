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
from Tree import Tree
from Leaf import Leaf
from Sky import Sky

import math
import time
import random

#Classe responsável

class Mine:
    # Globais
    altura_janela = 900
    largura_janela = 900

    # Inputs (game controller)
    lateralInt = 0  # Translação em X
    forwardInt = 0  # Translação em Z
    verticalInt = 0  # Translação em Y
    currentLight = 0.5 # Iluminacao ambiente

    scrollXOffset = 0
    scrollYOffset = 0

    polygonal_mode = False  # Malha poligonal

    gameStep = 1 / 60

    boxSize = 15  # x e z
    heightSize = 15  # y

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
        self.animatedObjects = []

        #Criacão do cenário estático 
        self.generateGround()
        self.objects.append(House((3, 1, 3), 6, 7, 3))
        self.objects.append(Tree((12, 1, 12), 3))
        self.objects.append(Block(12, 1, 7, 0, 11))

        #Criação do cenário dinâmico, jogador e céu 

        self.animatedObjects.append(Sky(19))
        self.animatedObjects.append(Leaf((11, 4, 11)))
        self.animatedObjects.append(Leaf((14, 4, 13)))


        self.player = Player(self.altura_janela, self.largura_janela)
        self.player.setLimit(self.boxSize, self.heightSize)

        self.sunPos=self.animatedObjects[0].updateSunpos()
        self.playerPos=self.player.getPlayerPos()
        self.light=self.animatedObjects[0].updateLight()


        self.lastTime = time.time()

        self.mouseX = self.largura_janela / 2
        self.mouseY = self.altura_janela / 2

    #Loop principal da janela 3D
    def run(self):
        self.window.loop()

    def onDraw(self):
        # Para desenhar, limpa o buffer de cores e pega o programa
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(1.0, 1.0, 1.0, 1.0)
        program = self.shader.getProgram()

        #Atualiza k tempo

        now = time.time()

        if (now - self.lastTime > self.gameStep):
            self.physicsTick()
            self.lastTime = now

        # verifica se deve usar o modo polygonal
        if self.polygonal_mode:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # Atualiza a posicao da luz

        loc_light_pos = glGetUniformLocation(program, "lightPos") # recuperando localizacao da variavel lightPos na GPU
        glUniform3f(loc_light_pos, self.sunPos[0],self.sunPos[1],self.sunPos[2]) ### posicao da fonte de luz

        loc_ia = glGetUniformLocation(program, "ia")
        glUniform1f(loc_ia, self.currentLight)

        loc_id = glGetUniformLocation(program, "id")
        glUniform1f(loc_id, self.light)

        loc_viewPos = glGetUniformLocation(program, "viewPos")
        glUniform3f(loc_viewPos, self.playerPos[0],self.playerPos[1],self.playerPos[2])

        #print(self.playerPos)

        #Desenha os objetos

        self.player.draw(program)

        for block in self.objects:
            block.draw(program)

        for animated in self.animatedObjects:
            animated.draw(program)


    #Funçoes para capturar eventos de mouse e teclado como inputs

    def onKeyEvent(self, window, key, scancode, action, mods):
        if action == 2:
            return

        mult = action * 2 - 1

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

        # Aumentar a intensidade da luz ambiente
        if key == glfw.KEY_P:
            self.currentLight += 0.1

        # Diminuir a intensidade da luz ambiente
        if key == glfw.KEY_U:
            self.currentLight -= 0.1

        # Subir
        if key == glfw.KEY_SPACE:
            self.verticalInt += mult

        # Descer
        if key == glfw.KEY_LEFT_SHIFT:
            self.verticalInt -= mult

        # Ativar e desativar a visão poligonal
        if key == glfw.KEY_O and action == 1:
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

        #print(self.sunPos)

        self.scrollXOffset = 0.0
        self.scrollYOffset = 0.0

        for obj in self.animatedObjects:
            obj.animate()

        self.sunPos=self.animatedObjects[0].updateSunpos()
        self.light=self.animatedObjects[0].updateLight()
        self.playerPos=self.player.getPlayerPos()

        # program = self.shader.getProgram()

    #Funcao para gerar ls blocos de chão 
    def generateGround(self):
        multiblock = MultiBlock(2)
        multiblock.generatePlane((10, 0, 6), (1, 0, 0), (0, 0, 1), 2, 8)
        multiblock.generatePlane((9, 0, 6), (1, 0, 0), (0, 0, 1), 2, 2)
        multiblock.generatePlane((0, 0, 12), (1, 0, 0), (0, 0, 1), 10, 2)
        self.objects += multiblock.placeBlocks()

        multiblock = MultiBlock(1)
        multiblock.generatePlane((12, 0, 0), (1, 0, 0), (0, 0, 1), 3, 15)
        multiblock.generatePlane((0, 0, 0), (1, 0, 0), (0, 0, 1), 12, 3)
        multiblock.generatePlane((9, 0, 3), (1, 0, 0), (0, 0, 1), 3, 3)
        multiblock.generatePlane((0, 0, 3), (1, 0, 0), (0, 0, 1), 3, 8)
        multiblock.generateLine((0, 0, 14), (1, 0, 0), 12)
        multiblock.generateLine((0, 0, 11), (1, 0, 0), 10)
        multiblock.generateLine((9, 0, 8), (0, 0, 1), 3)
        self.objects += multiblock.placeBlocks()

        multiblock = MultiBlock(1)
        self.objects += multiblock.placeBlocks()



