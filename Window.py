import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders

class Window:
    def __init__ (self, width, height, title):
        #Inicialização de uma janela usando o glfw, cria uma janela com o título e a torna o contexto principal
        glfw.init()

        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        self.window = glfw.create_window(width, height, title, None, None)
        glfw.make_context_current(self.window)
        self.onDraw = None
        self.cursorLocked = False
        glEnable(GL_DEPTH_TEST) ### importante para 3D
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)

    def setKeyEvent (self, onKeyEvent):
        glfw.set_key_callback(self.window, onKeyEvent)

    def setCursorEvent (self, onCursorEvent):
        glfw.set_cursor_pos_callback(self.window, onCursorEvent)

    def setScrollEvent (self, onScrollEvent):
        glfw.set_scroll_callback(self.window, onScrollEvent)

    def invertCursorLocked (self):
        if self.cursorLocked:
            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_NORMAL)
        else:
            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

        self.cursorLocked = not self.cursorLocked

    def setOnDraw (self, onDraw):
        self.onDraw = onDraw

    def loop (self):
        #Loop Principal de uma Janela: a exibe e se ela não deve fechar , ela recebe as atualizações/eventos
        glfw.show_window(self.window)
        
        while not glfw.window_should_close(self.window):
            # glFlush()
            glfw.poll_events()

            if (self.onDraw is not None):
                self.onDraw()

            glfw.swap_buffers(self.window)

        glfw.terminate()
        
    def close (self):
        glfw.set_window_should_close(self.window, True)

