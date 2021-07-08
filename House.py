import OpenGL.GL.shaders
import numpy as np
import glm

from Blocks import Block
from MultiBlock import MultiBlock


class House:
    def __init__(self, start, xSize, zSize, ySize):
        self.blocks = []
        self.build(start, xSize, ySize, zSize)

    def build(self, start, xSize, ySize, zSize):
        x, y, z = start

        # Parede 1
        multiblock = MultiBlock(4)
        multiblock.generatePlane((x, y, z), (0, 1, 0), (1, 0, 0), ySize, xSize)
        self.blocks += multiblock.placeBlocks()

        # Parede 2
        multiblock = MultiBlock(4)
        multiblock.generatePlane((x, y, z+zSize), (0, 1, 0), (1, 0, 0), ySize, xSize)
        self.blocks += multiblock.placeBlocks()

        # Teto
        multiblock = MultiBlock(4)
        multiblock.generatePlane((x, y+ySize, z), (1, 0, 0), (0, 0, 1), xSize, zSize+1)
        self.blocks += multiblock.placeBlocks()

        # Parede fundo
        multiblock = MultiBlock(4)
        multiblock.generateLine((x, y, z+1), (0, 0, 1), zSize-1)
        self.blocks += multiblock.placeBlocks()

        multiblock = MultiBlock(4)
        multiblock.generateLine((x, y+ySize-1, z + 1), (0, 0, 1), zSize - 1)
        self.blocks += multiblock.placeBlocks()

        self.blocks.append(Block(x, y+1, z+1, 4))
        self.blocks.append(Block(x, y+1, z+zSize-1, 4))




    def draw(self, program):
        for block in self.blocks:
            block.draw(program)