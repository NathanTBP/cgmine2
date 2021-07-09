import OpenGL.GL.shaders
import numpy as np
import glm

from Blocks import Block
from MultiBlock import MultiBlock

class Tree:
    def __init__(self, start, height):
        self.blocks = []
        self.build(start, height)

    def build(self, start, height):
        x, y, z = start

        # Tronco
        multiblock = MultiBlock(6)
        multiblock.generateLine((x, y, z), (0, 1, 0), height)
        self.blocks += multiblock.placeBlocks()

        # Folha
        multiblock = MultiBlock(7)
        multiblock.generatePlane((x-2, y+height, z-2), (1, 0, 0), (0, 0, 1), 5, 5)
        multiblock.generatePlane((x-1, y+height+1, z-1), (1, 0, 0), (0, 0, 1), 3, 3)
        multiblock.generatePlane((x, y+height+2, z), (1, 0, 0), (0, 0, 1), 1, 1)
        self.blocks += multiblock.placeBlocks()



    def draw(self, program):
        for block in self.blocks:
            block.draw(program)