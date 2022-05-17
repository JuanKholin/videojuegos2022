import pygame as pg
from . import Player, Command, Utils, Raton
from .Music import *
from .Lib import *
from .Utils import *
from .Command import *

class Upgrade():
    def __init__(self, image):
        self.image = pg.image.load(image)
        self.image = pg.transform.scale(self.image, (Utils.BUTTON_W, Utils.BUTTON_H))
        self.click = False
        self.collide = False
        self.x = 0
        self.y = 0
        self.cantidad = 0
        
    def update(self):
        pass
        
    def draw(self, screen, x, y):
        self.x = x
        self.y = y
        screen.blit(self.image, (x, y))
        muestra_texto(screen, 'monotypecorsiva', str(self.cantidad), GREEN2, 15, (self.x + 40, self.y + 40))
        if self.collide:
            pass
            #pygame.draw.rect(screen, BLUE, pygame.Rect(self.x, self.y-15, 50, 20))
            #text = Utils.text[self.option] 
            #muestra_texto(screen, times, text, BLACK, 30, (self.x, self.y-20))
        if Utils.DEBBUG:
            pygame.draw.rect(screen, PINK, pygame.Rect(self.x, self.y, Utils.BUTTON_W, Utils.BUTTON_H), 1)
            
    def getRect(self):
        return pg.Rect(self.x, self.y, Utils.BUTTON_W, Utils.BUTTON_H)
        
    def setClicked(self):
        self.click = True 
        
    def setCollide(self, collide):
        self.collide = collide 
        
    def getCommand(self):
        return Command(self.command)