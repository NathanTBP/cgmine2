import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math
import glm

class Player:
    # O player atua como a camera que se move pelo cenario e usa as matrizes de view e projection
    cameraPos = glm.vec3(7.0, 0, 7.0)
    cameraFront = glm.vec3(1.0, 0.0, 0.0)
    cameraUp = glm.vec3(0.0, 1.0, 0.0)
    cameraSpeed = 0.4

    def __init__(self, altura, largura):
        self.altura = altura
        self.largura = largura
        self.fov = 45

        self.firstMouse = True
        self.lastX = 0
        self.lastY = 0
        self.yaw = -90.0
        self.pitch = 0

        self.boxHeight = 0
        self.boxSize = 0
        self.heightSize = 2.5
        self.cameraPos[1] = self.heightSize

        pass
    
    #Matriz view
    def getView(self):
        mat_view = glm.lookAt(self.cameraPos, self.cameraPos + self.cameraFront, self.cameraUp)
        mat_view = np.array(mat_view)
        return mat_view
    #Matriz Projection
    def getProjection(self):
        fov = glm.radians(self.fov)
        aspect = self.largura / self.altura
        znear = 0.1
        zfar = 50

        mat_projection = glm.perspective(fov, aspect, znear, zfar)
        mat_projection = np.array(mat_projection)
        return mat_projection
    # Draw da visão 
    def draw(self, program):
        # print(self.cameraPos)
        mat_view = self.getView()
        loc_view = glGetUniformLocation(program, "view")
        glUniformMatrix4fv(loc_view, 1, GL_FALSE, mat_view)

        mat_projection = self.getProjection()
        loc_projection = glGetUniformLocation(program, "projection")
        glUniformMatrix4fv(loc_projection, 1, GL_FALSE, mat_projection)

    #Movimentação do Personagem (com diferentes intensidades)
    def movePlayer(self, forwardIntensity, lateralIntensity, verticalIntensity):
        forwardVector = glm.normalize(glm.vec3(self.cameraFront[0], 0.0, self.cameraFront[2]))
        lateralVector = glm.normalize(glm.cross(self.cameraFront, self.cameraUp) * glm.vec3(1.0, 0.0, 1.0))

        self.cameraPos += forwardVector * forwardIntensity * self.cameraSpeed
        self.cameraPos += lateralVector * lateralIntensity * self.cameraSpeed
        self.cameraPos[1] += verticalIntensity * self.cameraSpeed

        self.cameraPos[0] = max(min(self.cameraPos[0], self.boxSize-0.5), 0.5)
        self.cameraPos[2] = max(min(self.cameraPos[2], self.boxSize-0.5), 0.5)
        self.cameraPos[1] = max(min(self.cameraPos[1], self.boxHeight-0.5), 0+self.heightSize)

    #Uso do mouse para controlar a angulação da camera
    def lookAround(self, xpos, ypos):
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

        if self.pitch >= 90.0:
            self.pitch = 90.0
        if self.pitch <= -90.0:
            self.pitch = -90.0

        front = glm.vec3()
        front.x = math.cos(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch))
        front.y = math.sin(glm.radians(self.pitch))
        front.z = math.sin(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch))
        self.cameraFront = glm.normalize(front)

    #Uso do fov para dsr xoom
    def zoom(self, yoffset):
        self.fov -= yoffset

        if self.fov < 20.0:
            self.fov = 20.0
        elif self.fov > 70.0:
            self.fov = 70.0

    def getPlayerPos(self):
        return self.cameraPos[0], self.cameraPos[1], self.cameraPos[2]

    def getPlayerHeight(self):
        return self.heightSize

    #Limitaçao do personagem baseado no tamabho do cenário 
    def setLimit(self, boxSize, heightSize):
        self.boxSize = boxSize
        self.boxHeight = heightSize

