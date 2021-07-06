import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import glm

#Codigos GLSL, cada vértice representado por um vetor de x,y,z,1 para coordenadas homogêneas do objeto e suas respectivas matrizes
# de modew, view e projection e os fragmentos contendo apenas uma cor
vertex_code = """
        attribute vec3 position;
                
        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;        
        
        void main(){
            gl_Position = projection * view * model * vec4(position,1.0);
        }
        """

fragment_code = """
        uniform vec4 color;
        varying vec2 out_texture;
        uniform sampler2D samplerTexture;
        
        void main(){
            vec4 texture = texture2D(samplerTexture, out_texture);
            gl_FragColor = texture;
        }
        """

class Shader:
    def __init__ (self):
        #Inicialização dos shaders de vértice e de fragmentos
        self.program  = glCreateProgram()
        vertex   = glCreateShader(GL_VERTEX_SHADER)
        fragment = glCreateShader(GL_FRAGMENT_SHADER)

        #Recupera o código GLSL
        glShaderSource(vertex, vertex_code)
        glShaderSource(fragment, fragment_code)

        #Compila e Verifica Erros
        glCompileShader(vertex)
        if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(vertex).decode()
            print(error)
            raise RuntimeError("Erro de compilacao do Vertex Shader")

        glCompileShader(fragment)
        if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(fragment).decode()
            print(error)
            raise RuntimeError("Erro de compilacao do Fragment Shader")

        #Liga-os ao programa e verifica erros
        glAttachShader(self.program, vertex)
        glAttachShader(self.program, fragment)

        glLinkProgram(self.program)
        if not glGetProgramiv(self.program, GL_LINK_STATUS):
            print(glGetProgramInfoLog(self.program))
            raise RuntimeError('Linking error')
            
        glUseProgram(self.program)

    def getProgram (self):
        return self.program





