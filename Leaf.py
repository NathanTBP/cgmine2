import OpenGL.GL.shaders
import numpy as np
import glm

from Blocks import Block
from MultiBlock import MultiBlock


class Leaf:
    def __init__(self, start):
        self.x, self.y, self.z = start
        self.initialY = self.y
        self.block = Block(self.x, self.y, self.z, 0, 7)

    def animate(self):
        x, y, z = self.block.getCoord()
        y -= 0.3
        if y <= 0.5:
            y = self.initialY
        self.block.setCoord((x, y, z))

    def draw(self, program):
        self.block.draw(program)
