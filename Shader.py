import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import glm

#Codigos GLSL, cada vértice representado por um vetor de x,y,z,1 para coordenadas homogêneas do objeto e suas respectivas matrizes
# de modew, view e projection e os fragmentos contendo apenas uma cor
vertex_code = """
        //Vertices
        attribute vec3 position;        //Coordenadas   
        attribute vec2 texture_coord;   //Texturas  
        attribute vec3 normals;         //Normais 
        
        //Texturas para iluminar
        varying vec2 out_texture;
        varying vec3 out_fragPos;
        varying vec3 out_normal;

        //Matrizes do Shader de Vertices
        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;        
        
        void main(){
            gl_Position = projection * view * model * vec4(position,1.0);
            out_texture = vec2(texture_coord);
            out_fragPos = vec3(position);
            out_normal = vec3( model *vec4(normals, 1.0));   
        }
        """

fragment_code = """

        // Iluminacao ambiente
        uniform float ka; // coeficiente de reflexao ambiente
        uniform float ia; // coeficiente da intensidade da luz ambiente

        // Cor da luz
        vec3 lightColor = vec3(1.0, 1.0, 1.0); // Branca

        // Parametros da reflexao difusa
        uniform vec3 lightPos; // define coordenadas de posicao da luz
        uniform float kd; // coeficiente de reflexao difusa
        uniform float id; // coeficiente da intensidade da luz difusa

        // Parametros da reflexao especular
        uniform vec3 viewPos; // Coordenadas do visualizador
        uniform float ks; // coeficiente de reflexao especular
        uniform float ns; // expoente de reflexao especular        

        // Imports
        varying vec2 out_texture; // Texturas vindas do vertex shader
        varying vec3 out_normal; // Normais vindas do vertex shader
        varying vec3 out_fragPos; // Coordenadas vindas do vertex shader
        uniform sampler2D samplerTexture; // Sampler de amostras de texturas
  
        void main(){
            
            // Luz ambiente
            vec3 ambient = ia * ka * lightColor; // Componente da iluminacao ambiente        
        
            // Reflexao difusa
            vec3 norm = normalize(out_normal); // normaliza vetores perpendiculares (N)
            vec3 lightDir = normalize(lightPos - out_fragPos); // direcao da luz normalizada (L)
            float diff = max(dot(norm, lightDir), 0.0); // verifica limite angular (entre 0 e 90 graus) (N.L)
            vec3 diffuse = id * kd * diff * lightColor; // Componente da iluminacao difusa 

            // Reflexao especular
            vec3 viewDir = normalize(viewPos - out_fragPos); // direcao do observador/camera normalizada (V)
            vec3 reflectDir = normalize(reflect(-lightDir, norm)); // direcao da reflexao normalizada (calculada pela lei de Snell) (R)
            float spec = pow(max(dot(viewDir, reflectDir), 0.0), ns); // (V.R)
            vec3 specular = ks * spec * lightColor;  //Componente de iluminacao especular
            
            vec4 texture = texture2D(samplerTexture, out_texture); //Aplica sample de textura
            vec4 result = vec4((ambient + diffuse + specular),1.0) * texture; // Aplica iluminacao (difusa + ambiente + especular)
            gl_FragColor = result;

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





