import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math
import glm

from Blocks import Block

class MultiBlock:
    def __init__(self, type):
        self.blocks = []
        self.type = type

    #Diferentes métodos  para auxiliar a criação de cenários (nomes autoexplicativos)
    def generateLine(self, start, direction, length):
        x, y, z = start
        for i in range(length):
            self.blocks.append(Block(x, y, z, 0, self.type))
            print(x, y, z)

            x += direction[0]
            y += direction[1]
            z += direction[2]

    def generatePlane(self, start, direction1, direction2, length1, length2):
        x, y, z = start

        for i in range(length1):
            tmpX = x
            tmpY = y
            tmpZ = z

            for j in range(length2):
                self.blocks.append(Block(tmpX, tmpY, tmpZ, 0, self.type))

                tmpX += direction2[0]
                tmpY += direction2[1]
                tmpZ += direction2[2]

            x += direction1[0]
            y += direction1[1]
            z += direction1[2]

    def placeBlocks(self):
        return self.blocks
