import pygame as pg
from . import Player, Command, Utils, Raton
from .Music import *
from .Lib import *
from .Utils import *
from .Command import *

class UpgradeButton():
    def __init__(self, image, command, cartel = None, msgCartel = "a", xpad = 0, cartelpad = 0):
        self.image = pg.image.load(image)
        self.image = pg.transform.scale(self.image, (Utils.BUTTON_W, Utils.BUTTON_H))
        if cartel != None:
            self.cartel = pg.image.load(cartel)
            self.cartel = pg.transform.scale(self.cartel, (self.cartel.get_width() * 1.5, self.cartel.get_height() * 1.5))
        else:
            self.cartel = None
        self.linea1 = msgCartel.split(";")[0]
        self.linea2 = msgCartel.split(";")[1]
        self.command = command
        self.click = False
        self.collide = False
        self.x = 0
        self.y = 0
        self.xpad = xpad
        self.costeMineral = 50
        self.costeGas = 50
        self.cartelPad = cartelpad
        self.nextLevel = 1
        
    def update(self, mineral, gas):
        self.costeMineral = mineral
        self.costeGas = gas
    
    def draw(self, screen, x, y):
        self.x = x
        self.y = y
        screen.blit(self.image, (x, y))
        if self.collide:
            if self.cartel != None:
                screen.blit(self.cartel, (x - self.cartelPad, y- 80))
                muestra_texto(screen, 'monotypecorsiva', str(self.linea1), GREEN2, 20, (self.x - self.cartelPad + self.xpad, self.y - 80))
                muestra_texto(screen, 'monotypecorsiva', str(self.linea2), GREEN2, 20, (self.x - self.cartelPad + self.xpad, self.y - 65))
                muestra_texto(screen, 'monotypecorsiva', "Nivel siguiente: " + str(self.nextLevel), GREEN2, 20, (self.x - self.cartelPad + self.xpad, self.y - 50))
                muestra_texto(screen, 'monotypecorsiva', str(self.costeMineral), GREEN2, 20, (self.x + 28 - self.cartelPad , self.y - 27))
                muestra_texto(screen, 'monotypecorsiva', str(self.costeGas), GREEN2, 20, (self.x + 78 - self.cartelPad , self.y - 27))
            else:
                pygame.draw.rect(screen, BLUE, pygame.Rect(self.x, self.y-15, 50, 20))
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
    
    
           
        