import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math
import glm

class Player:
    cameraPos = glm.vec3(10.0, 10.0, 10.0)
    cameraFront = glm.vec3(0.0, 0.0, 1)
    cameraUp = glm.vec3(0.0, 1.0, 0.0)
    cameraSpeed = 0.5

    def __init__(self, altura, largura):
        self.altura = altura
        self.largura = largura
        self.fov = 45

        pass

    def getView(self):
        mat_view = glm.lookAt(self.cameraPos, self.cameraPos + self.cameraFront, self.cameraUp)
        mat_view = np.array(mat_view)
        return mat_view

    def getProjection(self):
        fov = glm.radians(self.fov)
        aspect = self.largura / self.altura
        znear = 0.1
        zfar = 1000

        mat_projection = glm.perspective(fov, aspect, znear, zfar)
        mat_projection = np.array(mat_projection)
        return mat_projection

    def draw(self, program):
        # atualiza as matrizes view e projection
        mat_view = self.getView()
        loc_view = glGetUniformLocation(program, "view")
        glUniformMatrix4fv(loc_view, 1, GL_FALSE, mat_view)

        mat_projection = self.getProjection()
        loc_projection = glGetUniformLocation(program, "projection")
        glUniformMatrix4fv(loc_projection, 1, GL_FALSE, mat_projection)

    def move(self, forwardIntensity, lateralIntensity):
        forwardVector = glm.normalize(glm.vec3(self.cameraFront[0], 0.0, self.cameraFront[2]))
        lateralVector = glm.normalize(glm.cross(self.cameraFront, self.cameraUp) * glm.vec3(1.0, 0.0, 1.0))

        self.cameraPos += forwardVector * forwardIntensity * self.cameraSpeed
        self.cameraPos += lateralVector * lateralIntensity * self.cameraSpeed
