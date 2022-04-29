import pygame as pg
from . import Player, Command, Utils, Raton
from .Music import *
from .Lib import *
from .Utils import *
from .Command import *

class ButtonType(Enum):
    GENERAR_UNIDAD = auto()

class Button():
    def __init__(self, image, command):
        self.image = pg.image.load(image)
        self.image = pg.transform.scale(self.image, (Utils.BUTTON_W, Utils.BUTTON_H))
        self.command = command
        self.click = False
        self.collide = False
        self.x = 0
        self.y = 0
        
    def update(self):
        pass
        
    def draw(self, screen, x, y):
        self.x = x
        self.y = y
        screen.blit(self.image, (x, y))
        if self.collide:
            text = Utils.text[self.command] 
            muestra_texto(screen, times, text, BLACK, 30, (self.x, self.y-20))
            
    def getRect(self):
        return pg.Rect(self.x, self.y, Utils.BUTTON_W, Utils.BUTTON_H)
        
    def setClicked(self):
        self.click = True 
        
    def setCollide(self):
        self.collide = True  
        
    def getCommand(self):
        return self.command
           
        