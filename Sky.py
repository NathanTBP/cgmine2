import OpenGL.GL.shaders
import numpy as np
import glm
import math

from Blocks import Block

class Sky:
    def __init__(self, hour):
        self.hour=hour
        self.block =  Block(0, 0, 15, 0, 13)
        self.block.setHr(self.hour)

    def animate(self):
        hour=self.block.getHr()
        hour=hour+0.1
        if(hour>=24):
            hour=0
        self.block.setHr(hour)

    def draw(self, program):
        self.block.draw(program)

    def getHr(self):
        return math.floor(self.block.getHr())  

    def updateSunpos(self):

        hour=math.floor(self.block.getHr())  
    
        if(hour==0):
            x=9
            y=15
            
        elif(hour==1):
            x=6
            y=15
            
        elif(hour==2):
            x=3
            y=15
            
        elif(hour==3):
            x=0
            y=12
            
        elif(hour==4):
            x=0
            y=9
            
        elif(hour==5):
            x=0
            y=6
            
        elif(hour==6):
            x=0
            y=3

        elif(hour==7):
            x=15
            y=3
            
        elif(hour==8):
            x=15
            y=6
            
        elif(hour==9):
            x=15
            y=9
            
        elif(hour==10):
            x=15
            y=12
            
        elif(hour==11):
            x=12
            y=15
            
        elif(hour==12):
            x=9
            y=15
            
        elif(hour==13):
            x=6
            y=15
            
        elif(hour==14):
            x=3
            y=15
            
        elif(hour==15):
            x=0
            y=12
            
        elif(hour==16):
            x=0
            y=9
            
        elif(hour==17):
            x=0
            y=6
            
        elif(hour==18):
            x=0
            y=3
            
        elif(hour==19):
            x=15
            y=3
            
        elif(hour==20):
            x=15
            y=6
            
        elif(hour==21):
            x=15
            y=9
            
        elif(hour==22):
            x=15
            y=12
            
        elif(hour==23):
            x=12
            y=15

        return (x,y,7)

    def updateLight(self):

        hour=math.floor(self.block.getHr())  

        if(hour>=7 and hour<=18):
            return 1.8
        
        else:
            return 0.8
